import streamlit as st
import pandas as pd
import plotly.express as px

from src.cleaner import clean_dataframe
from src.risk_scoring import calculate_risk_score


st.set_page_config(
    page_title="Risk Analyzer",
    layout="wide"
)


st.title("Public Procurement Corruption Risk Analyzer")

st.write(
    """
    This platform analyzes public procurement data and identifies tenders 
    with potential corruption risk based on transparent rule-based indicators.
    """
)


uploaded_file = st.file_uploader(
    "Upload ProZorro tenders CSV file",
    type=["csv"]
)


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, low_memory=False)

    st.subheader("1. Uploaded Data")

    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.dataframe(df.head(20), use_container_width=True)

    cleaned_df = clean_dataframe(df)

    analyzed_df = calculate_risk_score(cleaned_df)

    st.subheader("2. Risk Analysis Summary")

    total_count = len(analyzed_df)
    high_count = len(analyzed_df[analyzed_df["risk_level"] == "High"])
    medium_count = len(analyzed_df[analyzed_df["risk_level"] == "Medium"])
    low_count = len(analyzed_df[analyzed_df["risk_level"] == "Low"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tenders", total_count)
    col2.metric("High Risk", high_count)
    col3.metric("Medium Risk", medium_count)
    col4.metric("Low Risk", low_count)

    st.subheader("3. Risk Level Distribution")

    risk_distribution = (
        analyzed_df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk_distribution.columns = ["risk_level", "count"]

    fig = px.bar(
        risk_distribution,
        x="risk_level",
        y="count",
        title="Risk Level Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("4. Risk Score Distribution")

    fig_score = px.histogram(
        analyzed_df,
        x="risk_score",
        nbins=20,
        title="Risk Score Distribution"
    )

    st.plotly_chart(fig_score, use_container_width=True)

    st.subheader("5. Top High-Risk Tenders")

    display_columns = [
        "tender_id",
        "published_date",
        "buyer_id",
        "supplier_id",
        "procurement_method",
        "tender_value",
        "award_value",
        "number_of_tenderers",
        "number_of_bids",
        "is_single_bidder",
        "is_competitive",
        "risk_score",
        "risk_level",
        "risk_reasons",
    ]

    existing_columns = [
        column for column in display_columns
        if column in analyzed_df.columns
    ]

    high_risk_df = (
        analyzed_df[analyzed_df["risk_level"] == "High"]
        .sort_values(by="risk_score", ascending=False)
    )

    st.dataframe(
        high_risk_df[existing_columns].head(100),
        use_container_width=True
    )

    st.subheader("6. Full Analyzed Dataset")

    st.dataframe(
        analyzed_df[existing_columns].head(300),
        use_container_width=True
    )

    csv = analyzed_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download analyzed data as CSV",
        data=csv,
        file_name="risk_analyzed_prozorro.csv",
        mime="text/csv"
    )

else:
    st.info("Upload a CSV file to start risk analysis.")