import io
from typing import List

import pandas as pd
import plotly.express as px
import streamlit as st

from i18n import t, translate_indicator, translate_risk_level
from src.cleaner import clean_dataframe
from src.risk_scoring import calculate_risk_score


LANG = "ru"


st.set_page_config(
    page_title=t("page_title", LANG),
    page_icon="⚠️",
    layout="wide",
)


RECOMMENDED_COLUMNS = [
    "tender_id",
    "year",
    "buyer_id",
    "supplier_id",
    "procurement_method",
    "main_procurement_category",
    "tender_value",
    "award_value",
    "number_of_tenderers",
    "number_of_bids",
    "is_single_bidder",
    "is_competitive",
    "has_cancelled_awards",
    "has_unsuccessful_awards",
    "price_change_pct",
    "award_concentration",
]


RISK_COLUMNS = [
    "single_bidder_risk",
    "low_competition_risk",
    "high_value_risk",
    "cancelled_awards_risk",
    "unsuccessful_awards_risk",
    "price_change_risk",
    "award_concentration_risk",
]


def format_usd(value: float | int) -> str:
    if pd.isna(value):
        return "$0"

    return f"${value:,.0f}"


def get_currency_column_config() -> dict:
    return {
        "tender_value": st.column_config.NumberColumn(
            t("tender_value", LANG),
            format="$%d",
        ),
        "award_value": st.column_config.NumberColumn(
            t("award_value", LANG),
            format="$%d",
        ),
    }


def get_table_column_config() -> dict:
    return {
        **get_currency_column_config(),
        "tender_id": st.column_config.TextColumn(t("tender_id", LANG)),
        "year": st.column_config.NumberColumn(t("year", LANG), format="%d"),
        "buyer_id": st.column_config.TextColumn(t("buyer_id", LANG)),
        "supplier_id": st.column_config.TextColumn(t("supplier_id", LANG)),
        "procurement_method": st.column_config.TextColumn(
            t("procurement_method", LANG)
        ),
        "main_procurement_category": st.column_config.TextColumn(
            t("procurement_category", LANG)
        ),
        "number_of_tenderers": st.column_config.NumberColumn(
            t("number_of_tenderers", LANG),
            format="%d",
        ),
        "number_of_bids": st.column_config.NumberColumn(
            t("number_of_bids", LANG),
            format="%d",
        ),
        "risk_score": st.column_config.NumberColumn(
            t("risk_score", LANG),
            format="%d",
        ),
        "risk_level": st.column_config.TextColumn(t("risk_level", LANG)),
        "risk_reasons": st.column_config.TextColumn(t("risk_reasons", LANG)),
    }


def localize_dataframe_for_display(df: pd.DataFrame) -> pd.DataFrame:
    display_df = df.copy()

    if "risk_level" in display_df.columns:
        display_df["risk_level"] = display_df["risk_level"].apply(
            lambda value: translate_risk_level(value, LANG)
        )

    return display_df


def show_header() -> None:
    st.title(t("header_title", LANG))
    st.write(t("header_description", LANG))


@st.cache_data(show_spinner=False)
def read_csv_file(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes), low_memory=False)


@st.cache_data(show_spinner=False)
def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = clean_dataframe(df)
    scored_df = calculate_risk_score(cleaned_df)
    return scored_df


def get_missing_columns(df: pd.DataFrame, columns: List[str]) -> List[str]:
    return [column for column in columns if column not in df.columns]


def show_upload_block() -> pd.DataFrame | None:
    uploaded_file = st.file_uploader(
        t("upload_label", LANG),
        type=["csv"],
        help=t("upload_help", LANG),
    )

    if uploaded_file is None:
        st.info(t("upload_empty", LANG))
        return None

    try:
        file_bytes = uploaded_file.getvalue()
        df = read_csv_file(file_bytes)

        if df.empty:
            st.error(t("uploaded_csv_empty", LANG))
            return None

        st.success(t("upload_success", LANG))

        col1, col2, col3 = st.columns(3)
        col1.metric(t("uploaded_rows", LANG), f"{len(df):,}")
        col2.metric(t("uploaded_columns", LANG), f"{len(df.columns):,}")
        col3.metric(
            t("uploaded_file_size", LANG),
            f"{len(file_bytes) / 1024 / 1024:.2f} MB",
        )

        with st.expander(t("preview_uploaded_data", LANG), expanded=False):
            st.dataframe(
                df.head(20),
                use_container_width=True,
                hide_index=True,
                column_config=get_currency_column_config(),
            )

        return df

    except UnicodeDecodeError:
        st.error(t("csv_encoding_error", LANG))
        return None

    except pd.errors.ParserError:
        st.error(t("csv_parsing_error", LANG))
        return None

    except Exception as error:
        st.error(f"{t('unexpected_read_error', LANG)}: {error}")
        return None


def show_column_validation(df: pd.DataFrame) -> None:
    missing_columns = get_missing_columns(df, RECOMMENDED_COLUMNS)

    if not missing_columns:
        st.success(t("all_columns_ok", LANG))
        return

    st.warning(t("missing_columns_warning", LANG))

    with st.expander(t("missing_columns", LANG), expanded=False):
        st.write(missing_columns)


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header(t("filters", LANG))

    filtered_df = df.copy()

    if "risk_level" in filtered_df.columns:
        levels = sorted(
            filtered_df["risk_level"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_levels = st.sidebar.multiselect(
            t("risk_level", LANG),
            options=levels,
            default=levels,
            format_func=lambda value: translate_risk_level(value, LANG),
        )

        if selected_levels:
            filtered_df = filtered_df[
                filtered_df["risk_level"].astype(str).isin(selected_levels)
            ]

    if "year" in filtered_df.columns:
        years = sorted(filtered_df["year"].dropna().unique().tolist())

        selected_years = st.sidebar.multiselect(
            t("year", LANG),
            options=years,
            default=years,
        )

        if selected_years:
            filtered_df = filtered_df[
                filtered_df["year"].isin(selected_years)
            ]

    if "procurement_method" in filtered_df.columns:
        methods = sorted(
            filtered_df["procurement_method"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_methods = st.sidebar.multiselect(
            t("procurement_method", LANG),
            options=methods,
            default=methods,
        )

        if selected_methods:
            filtered_df = filtered_df[
                filtered_df["procurement_method"]
                .astype(str)
                .isin(selected_methods)
            ]

    if "main_procurement_category" in filtered_df.columns:
        categories = sorted(
            filtered_df["main_procurement_category"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_categories = st.sidebar.multiselect(
            t("procurement_category", LANG),
            options=categories,
            default=categories,
        )

        if selected_categories:
            filtered_df = filtered_df[
                filtered_df["main_procurement_category"]
                .astype(str)
                .isin(selected_categories)
            ]

    if "tender_value" in filtered_df.columns:
        tender_value = (
            pd.to_numeric(filtered_df["tender_value"], errors="coerce")
            .fillna(0)
        )

        min_value = int(tender_value.min())
        max_value = int(tender_value.max())

        if max_value > min_value:
            selected_range = st.sidebar.slider(
                t("tender_value_range", LANG),
                min_value=min_value,
                max_value=max_value,
                value=(min_value, max_value),
                format="$%d",
            )

            st.sidebar.caption(
                f"{format_usd(selected_range[0])} — {format_usd(selected_range[1])}"
            )

            filtered_df = filtered_df[
                pd.to_numeric(filtered_df["tender_value"], errors="coerce")
                .fillna(0)
                .between(selected_range[0], selected_range[1])
            ]

    if "buyer_id" in filtered_df.columns:
        buyer_search = st.sidebar.text_input(t("search_buyer_id", LANG))

        if buyer_search.strip():
            filtered_df = filtered_df[
                filtered_df["buyer_id"]
                .astype(str)
                .str.contains(buyer_search.strip(), case=False, na=False)
            ]

    if "supplier_id" in filtered_df.columns:
        supplier_search = st.sidebar.text_input(t("search_supplier_id", LANG))

        if supplier_search.strip():
            filtered_df = filtered_df[
                filtered_df["supplier_id"]
                .astype(str)
                .str.contains(supplier_search.strip(), case=False, na=False)
            ]

    return filtered_df


def show_summary_metrics(df: pd.DataFrame) -> None:
    st.subheader(t("risk_summary", LANG))

    total_rows = len(df)

    high_count = 0
    medium_count = 0
    low_count = 0

    if "risk_level" in df.columns:
        risk_level_series = df["risk_level"].astype(str)

        high_count = int((risk_level_series == "High").sum())
        medium_count = int((risk_level_series == "Medium").sum())
        low_count = int((risk_level_series == "Low").sum())

    average_score = 0

    if "risk_score" in df.columns and not df.empty:
        average_score = (
            pd.to_numeric(df["risk_score"], errors="coerce")
            .fillna(0)
            .mean()
        )

    total_tender_value = 0

    if "tender_value" in df.columns and not df.empty:
        total_tender_value = (
            pd.to_numeric(df["tender_value"], errors="coerce")
            .fillna(0)
            .sum()
        )

    total_award_value = 0

    if "award_value" in df.columns and not df.empty:
        total_award_value = (
            pd.to_numeric(df["award_value"], errors="coerce")
            .fillna(0)
            .sum()
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(t("analyzed_tenders", LANG), f"{total_rows:,}")
    col2.metric(t("high_risk", LANG), f"{high_count:,}")
    col3.metric(t("medium_risk", LANG), f"{medium_count:,}")
    col4.metric(t("low_risk", LANG), f"{low_count:,}")

    col5, col6, col7 = st.columns(3)

    col5.metric(t("average_score", LANG), f"{average_score:.2f}")
    col6.metric(t("total_tender_value", LANG), format_usd(total_tender_value))
    col7.metric(t("total_award_value", LANG), format_usd(total_award_value))


def show_charts(df: pd.DataFrame) -> None:
    st.subheader(t("visual_analytics", LANG))

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if "risk_level" in df.columns:
            risk_counts = (
                df["risk_level"]
                .astype(str)
                .value_counts()
                .reset_index()
            )
            risk_counts.columns = ["risk_level", "count"]
            risk_counts["risk_level_ru"] = risk_counts["risk_level"].apply(
                lambda value: translate_risk_level(value, LANG)
            )

            fig = px.bar(
                risk_counts,
                x="risk_level_ru",
                y="count",
                title=t("risk_level_distribution", LANG),
                text="count",
                labels={
                    "risk_level_ru": t("risk_level_axis", LANG),
                    "count": t("count_axis", LANG),
                },
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"{t('column_not_available', LANG)}: risk_level")

    with chart_col2:
        if "risk_score" in df.columns:
            fig = px.histogram(
                df,
                x="risk_score",
                nbins=30,
                title=t("risk_score_distribution", LANG),
                labels={
                    "risk_score": t("risk_score_axis", LANG),
                    "count": t("count_axis", LANG),
                },
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"{t('column_not_available', LANG)}: risk_score")

    if "year" in df.columns and "risk_score" in df.columns:
        yearly_risk = (
            df.assign(
                risk_score=pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)
            )
            .groupby("year", as_index=False)["risk_score"]
            .mean()
            .sort_values("year")
        )

        fig = px.line(
            yearly_risk,
            x="year",
            y="risk_score",
            markers=True,
            title=t("average_risk_by_year", LANG),
            labels={
                "year": t("year_axis", LANG),
                "risk_score": t("average_risk_score_axis", LANG),
            },
        )

        st.plotly_chart(fig, use_container_width=True)

    if "procurement_method" in df.columns and "risk_score" in df.columns:
        method_risk = (
            df.assign(
                risk_score=pd.to_numeric(df["risk_score"], errors="coerce").fillna(0)
            )
            .groupby("procurement_method", as_index=False)
            .agg(
                average_risk_score=("risk_score", "mean"),
                tenders_count=("risk_score", "count"),
            )
            .sort_values("average_risk_score", ascending=False)
            .head(15)
        )

        fig = px.bar(
            method_risk,
            x="procurement_method",
            y="average_risk_score",
            title=t("top_methods_by_average_risk", LANG),
            hover_data=["tenders_count"],
            labels={
                "procurement_method": t("procurement_method_axis", LANG),
                "average_risk_score": t("average_risk_score_axis", LANG),
                "tenders_count": t("tenders_count", LANG),
            },
        )

        st.plotly_chart(fig, use_container_width=True)


def show_high_risk_table(df: pd.DataFrame) -> None:
    st.subheader(t("top_high_risk_tenders", LANG))

    if "risk_score" not in df.columns:
        st.info(f"{t('column_not_available', LANG)}: risk_score")
        return

    display_columns = [
        "tender_id",
        "year",
        "buyer_id",
        "supplier_id",
        "procurement_method",
        "main_procurement_category",
        "tender_value",
        "award_value",
        "number_of_tenderers",
        "number_of_bids",
        "risk_score",
        "risk_level",
        "risk_reasons",
    ]

    existing_columns = [
        column for column in display_columns
        if column in df.columns
    ]

    top_df = (
        df.sort_values("risk_score", ascending=False)
        .loc[:, existing_columns]
        .head(100)
    )

    top_df = localize_dataframe_for_display(top_df)

    st.dataframe(
        top_df,
        use_container_width=True,
        hide_index=True,
        column_config=get_table_column_config(),
    )


def show_risk_indicator_breakdown(df: pd.DataFrame) -> None:
    existing_risk_columns = [
        column for column in RISK_COLUMNS
        if column in df.columns
    ]

    if not existing_risk_columns:
        return

    st.subheader(t("risk_indicator_breakdown", LANG))

    breakdown = []

    for column in existing_risk_columns:
        active_count = int(
            (
                pd.to_numeric(df[column], errors="coerce")
                .fillna(0) > 0
            ).sum()
        )

        breakdown.append(
            {
                "indicator": column,
                "indicator_ru": translate_indicator(column, LANG),
                "active_tenders": active_count,
                "share_percent": round(active_count / len(df) * 100, 2)
                if len(df)
                else 0,
            }
        )

    breakdown_df = pd.DataFrame(breakdown).sort_values(
        "active_tenders",
        ascending=False,
    )

    display_breakdown_df = breakdown_df[
        ["indicator_ru", "active_tenders", "share_percent"]
    ].rename(
        columns={
            "indicator_ru": "indicator",
        }
    )

    st.dataframe(
        display_breakdown_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "indicator": st.column_config.TextColumn(t("indicator", LANG)),
            "active_tenders": st.column_config.NumberColumn(
                t("active_tenders", LANG),
                format="%d",
            ),
            "share_percent": st.column_config.NumberColumn(
                t("share_percent", LANG),
                format="%.2f%%",
            ),
        },
    )

    fig = px.bar(
        display_breakdown_df,
        x="indicator",
        y="active_tenders",
        title=t("activated_risk_indicators_chart", LANG),
        text="active_tenders",
        labels={
            "indicator": t("indicator", LANG),
            "active_tenders": t("active_tenders", LANG),
        },
    )

    st.plotly_chart(fig, use_container_width=True)


def show_full_dataset(df: pd.DataFrame) -> None:
    st.subheader(t("analyzed_dataset", LANG))

    display_df = localize_dataframe_for_display(df.head(300))

    st.write(
        f"{t('showing_first_rows', LANG)}: {len(df):,}"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config=get_table_column_config(),
    )


def show_download_button(df: pd.DataFrame) -> None:
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=t("download_analyzed_csv", LANG),
        data=csv_data,
        file_name="risk_analyzed_prozorro.csv",
        mime="text/csv",
    )


def main() -> None:
    show_header()

    uploaded_df = show_upload_block()

    if uploaded_df is None:
        return

    try:
        with st.spinner(t("cleaning_spinner", LANG)):
            analyzed_df = prepare_dataframe(uploaded_df)

        show_column_validation(analyzed_df)

        filtered_df = apply_sidebar_filters(analyzed_df)

        if filtered_df.empty:
            st.warning(t("no_data_matches", LANG))
            return

        show_summary_metrics(filtered_df)
        show_charts(filtered_df)
        show_high_risk_table(filtered_df)
        show_risk_indicator_breakdown(filtered_df)
        show_full_dataset(filtered_df)
        show_download_button(filtered_df)

    except KeyError as error:
        st.error(f"{t('missing_required_column', LANG)}: {error}")

    except ValueError as error:
        st.error(f"{t('data_validation_error', LANG)}: {error}")

    except Exception as error:
        st.error(f"{t('unexpected_analysis_error', LANG)}: {error}")


if __name__ == "__main__":
    main()