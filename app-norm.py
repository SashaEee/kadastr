"""
Скрипт для нормализации адресов с помощью Pullenti Address SDK.

Скрипт обрабатывает Excel файл с адресами и нормализует их, извлекая:
- Структурированные данные (город, улица, дом, квартира)
- GUID из ГАР (если доступен)
- Полный нормализованный адрес

Использует Pullenti Address SDK без индекса ГАР для базовой нормализации.
"""

import sys
import os
from typing import Dict, List, Any

import pandas as pd
from tqdm import tqdm

# Добавление пути к Pullenti Address SDK
# ВАЖНО: Укажите корректный путь к распакованному SDK
sys.path.append("pullenti_address")

from pullenti.address.AddressService import AddressService
from pullenti.address.ProcessTextParams import ProcessTextParams

# ===== КОНСТАНТЫ =====
# Файлы ввода/вывода
INPUT_XLSX = "Кадастровые_номера_с_данными_f.xlsx"
OUTPUT_CSV = "normalized_pullenti_no_gar1.csv"
OUTPUT_XLSX = "normalized_32ТБ.xlsx"

# Колонки для результатов нормализации
NORMALIZED_COLUMNS = [
    "Нормализованный адрес",
    "Город",
    "Улица",
    "Дом",
    "Квартира",
    "GUID (если есть)",
    "Статус"
]

# Уровни адресных объектов Pullenti
LEVEL_CITY = 3      # Город
LEVEL_STREET = 10   # Улица
LEVEL_HOUSE = 12    # Дом
LEVEL_FLAT = 13     # Квартира


def initialize_address_service() -> ProcessTextParams:
    """
    Инициализирует Pullenti Address SDK и возвращает параметры обработки.

    Returns:
        ProcessTextParams: Параметры для обработки адресов
    """
    print("Инициализация Pullenti Address...")
    AddressService.initialize()
    print("OK")

    # Создание параметров обработки
    params = ProcessTextParams()
    # При необходимости можно указать регион по умолчанию:
    # params.default_regions.append(20)  # Например, код региона

    return params


def normalize_address(text: str, params: ProcessTextParams) -> Dict[str, Any]:
    """
    Нормализует адрес с помощью Pullenti Address SDK.

    Args:
        text: Исходный текст адреса
        params: Параметры обработки Pullenti

    Returns:
        Словарь с нормализованными данными адреса
    """
    # Пустой результат по умолчанию
    empty_result = {
        "normalized": "",
        "full_path": "",
        "city": "",
        "street": "",
        "house": "",
        "flat": "",
        "gar_guids": []
    }

    # Проверка входных данных
    if not isinstance(text, str) or not text.strip():
        return empty_result

    try:
        # Обработка адреса
        result = AddressService.process_single_address_text(text, params)

        if result is None or not result.items:
            return empty_result

        # Получение полного пути адреса
        full_path = result.get_full_path(", ", False)

        # Инициализация переменных для компонентов адреса
        city = ""
        street = ""
        house = ""
        flat = ""
        guids: List[str] = []

        # Извлечение компонентов адреса по уровням
        for item in result.items:
            # Сбор GUID из ГАР
            if item.gars:
                for gar in item.gars:
                    guids.append(gar.guid)

            # Определение компонента по уровню
            level = item.level
            name = str(item)

            if level == LEVEL_CITY:
                city = name
            elif level == LEVEL_STREET:
                street = name
            elif level == LEVEL_HOUSE:
                house = name
            elif level == LEVEL_FLAT:
                flat = name

        return {
            "normalized": full_path,
            "full_path": full_path,
            "city": city,
            "street": street,
            "house": house,
            "flat": flat,
            "gar_guids": guids
        }

    except Exception as e:
        # В случае ошибки возвращаем пустой результат с информацией об ошибке
        error_result = empty_result.copy()
        error_result["error"] = str(e)
        return error_result


def process_addresses(df: pd.DataFrame, params: ProcessTextParams) -> pd.DataFrame:
    """
    Обрабатывает все адреса в DataFrame.

    Args:
        df: DataFrame с исходными данными
        params: Параметры обработки Pullenti

    Returns:
        DataFrame с добавленными нормализованными данными
    """
    if "Адрес" not in df.columns:
        raise ValueError("Столбец 'Адрес' не найден в файле!")

    total = len(df)
    print(f"Обработка {total} адресов...")

    # Подготовка списка всех исходных колонок
    original_columns = df.columns.tolist()

    # Полный список колонок для итогового DataFrame
    final_columns = original_columns + NORMALIZED_COLUMNS

    # Список для накопления обработанных строк
    all_rows = []

    # Обработка каждой строки с прогресс-баром
    for i, row in tqdm(
        df.iterrows(),
        total=total,
        desc="Нормализация адресов",
        unit="адрес"
    ):
        raw_addr = row["Адрес"]
        result = normalize_address(raw_addr, params)

        # Формирование строки с GUID
        guid_str = "; ".join(result["gar_guids"]) if result["gar_guids"] else "—"

        # Определение статуса обработки
        status = "ОК" if result["full_path"] else "Не распознан"

        # Создание новой строки с исходными данными и результатами нормализации
        new_row = row.to_dict()
        new_row["Исходный адрес"] = raw_addr
        new_row["Нормализованный адрес"] = result["full_path"]
        new_row["Город"] = result["city"]
        new_row["Улица"] = result["street"]
        new_row["Дом"] = result["house"]
        new_row["Квартира"] = result["flat"]
        new_row["GUID (если есть)"] = guid_str
        new_row["Статус"] = status

        all_rows.append(new_row)

    # Создание итогового DataFrame
    result_df = pd.DataFrame(all_rows, columns=final_columns)

    return result_df


def save_results(df: pd.DataFrame, csv_path: str, xlsx_path: str) -> None:
    """
    Сохраняет результаты в CSV и Excel файлы.

    Args:
        df: DataFrame с результатами
        csv_path: Путь для сохранения CSV
        xlsx_path: Путь для сохранения Excel
    """
    df.to_csv(csv_path, index=False, encoding='utf-8')
    df.to_excel(xlsx_path, index=False)

    print(f"\n✅ Готово! Результаты сохранены в:")
    print(f"  - {csv_path}")
    print(f"  - {xlsx_path}")


def main() -> None:
    """
    Основная функция для нормализации адресов.
    """
    # Инициализация Pullenti Address SDK
    params = initialize_address_service()

    # Загрузка входных данных
    df = pd.read_excel(INPUT_XLSX)

    # Обработка адресов
    result_df = process_addresses(df, params)

    # Сохранение результатов
    save_results(result_df, OUTPUT_CSV, OUTPUT_XLSX)


if __name__ == "__main__":
    main()
