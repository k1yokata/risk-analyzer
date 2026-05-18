TRANSLATIONS = {
    "ru": {
        # Page
        "page_title": "Анализатор рисков закупок",
        "header_title": "Анализатор рисков государственных закупок",
        "header_description": (
            "Streamlit-приложение для анализа данных ProZorro и выявления тендеров "
            "с потенциально повышенным коррупционным риском."
        ),

        # Upload
        "upload_label": "Загрузите CSV-файл с тендерами ProZorro",
        "upload_help": "Лучше загружать sample-файл, например data/processed/tenders_2025_sample.csv",
        "upload_empty": "Загрузите CSV-файл, чтобы начать анализ рисков.",
        "upload_success": "CSV-файл успешно загружен.",
        "uploaded_rows": "Строки",
        "uploaded_columns": "Колонки",
        "uploaded_file_size": "Размер файла",
        "preview_uploaded_data": "Предпросмотр загруженных данных",
        "uploaded_csv_empty": "Загруженный CSV-файл пустой.",
        "csv_encoding_error": "Ошибка кодировки CSV. Сохраните файл в UTF-8 и загрузите снова.",
        "csv_parsing_error": "Ошибка чтения CSV. Проверьте формат файла, разделители и повреждённые строки.",
        "unexpected_read_error": "Непредвиденная ошибка при чтении CSV",

        # Validation
        "all_columns_ok": "Датасет содержит все рекомендуемые колонки для анализа рисков.",
        "missing_columns_warning": (
            "Некоторые рекомендуемые колонки отсутствуют. "
            "Приложение продолжит работу, но часть индикаторов риска может быть рассчитана как 0."
        ),
        "missing_columns": "Отсутствующие рекомендуемые колонки",

        # Sidebar
        "filters": "Фильтры",
        "risk_level": "Уровень риска",
        "year": "Год",
        "procurement_method": "Метод закупки",
        "procurement_category": "Категория закупки",
        "tender_value_range": "Диапазон стоимости тендера",
        "search_buyer_id": "Поиск по buyer_id",
        "search_supplier_id": "Поиск по supplier_id",

        # Metrics
        "risk_summary": "Сводная статистика по рискам",
        "analyzed_tenders": "Проанализировано тендеров",
        "high_risk": "Высокий риск",
        "medium_risk": "Средний риск",
        "low_risk": "Низкий риск",
        "average_score": "Средний риск-балл",
        "total_tender_value": "Общая стоимость тендеров",
        "total_award_value": "Общая сумма контрактов",

        # Charts
        "visual_analytics": "Визуальная аналитика",
        "risk_level_distribution": "Распределение тендеров по уровню риска",
        "risk_score_distribution": "Распределение риск-баллов",
        "average_risk_by_year": "Средний риск-балл по годам",
        "top_methods_by_average_risk": "Методы закупки с самым высоким средним риском",
        "activated_risk_indicators_chart": "Активированные индикаторы риска",
        "risk_level_axis": "Уровень риска",
        "count_axis": "Количество",
        "risk_score_axis": "Риск-балл",
        "year_axis": "Год",
        "procurement_method_axis": "Метод закупки",
        "average_risk_score_axis": "Средний риск-балл",
        "tenders_count": "Количество тендеров",

        # Tables
        "top_high_risk_tenders": "Топ тендеров с высоким риском",
        "risk_indicator_breakdown": "Разбор индикаторов риска",
        "analyzed_dataset": "Проанализированный датасет",
        "showing_first_rows": "Показаны первые 300 строк из отфильтрованного датасета. Всего строк",
        "download_analyzed_csv": "Скачать проанализированный CSV",

        # Table columns
        "tender_id": "ID тендера",
        "buyer_id": "ID заказчика",
        "supplier_id": "ID поставщика",
        "tender_value": "Стоимость тендера",
        "award_value": "Сумма контракта",
        "number_of_tenderers": "Количество участников",
        "number_of_bids": "Количество ставок",
        "risk_score": "Риск-балл",
        "risk_reasons": "Причины риска",
        "indicator": "Индикатор",
        "active_tenders": "Активных тендеров",
        "share_percent": "Доля, %",
        "file_name": "Имя файла",

        # Status
        "column_not_available": "Колонка недоступна",
        "no_data_matches": "Нет данных, соответствующих выбранным фильтрам.",
        "cleaning_spinner": "Очистка данных и расчёт риск-баллов...",
        "missing_required_column": "Отсутствует обязательная колонка",
        "data_validation_error": "Ошибка валидации данных",
        "unexpected_analysis_error": "Непредвиденная ошибка во время анализа",

        # Risk levels
        "High": "Высокий",
        "Medium": "Средний",
        "Low": "Низкий",

        # Risk indicators
        "single_bidder_risk": "Один участник",
        "low_competition_risk": "Низкая конкуренция",
        "high_value_risk": "Высокая стоимость",
        "cancelled_awards_risk": "Отменённые контракты",
        "unsuccessful_awards_risk": "Неуспешные контракты",
        "price_change_risk": "Изменение цены",
        "award_concentration_risk": "Концентрация контрактов",
    }
}


def t(key: str, lang: str = "ru") -> str:
    return TRANSLATIONS.get(lang, {}).get(key, key)


def translate_risk_level(value: object, lang: str = "ru") -> str:
    value_str = str(value)
    return TRANSLATIONS.get(lang, {}).get(value_str, value_str)


def translate_indicator(value: object, lang: str = "ru") -> str:
    value_str = str(value)
    return TRANSLATIONS.get(lang, {}).get(value_str, value_str)