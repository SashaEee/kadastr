"""
Скрипт для получения данных из Росреестра по кадастровым номерам.

Скрипт обрабатывает Excel файл с кадастровыми номерами и получает для каждого номера:
- Геометрию (координаты границ участка)
- Адрес, площадь, категорию земли
- Разрешенное использование, кадастровую стоимость
- Дату регистрации, тип собственности

Результаты сохраняются каждые 10 строк для возможности возобновления работы.
"""

import json
import logging
import os
import random
import time
from typing import Dict, Any, Optional

import pandas as pd
from rosreestr2coord.parser import Area
from tqdm import tqdm

# Настройка логирования
logging.getLogger("rosreestr2coord").setLevel(logging.WARNING)

# ===== КОНСТАНТЫ =====
# Файлы ввода/вывода
INPUT_FILE = "40ТБ.xlsx"
OUTPUT_FILE_XLSX = "Кадастровые_номера_с_данными_f.xlsx"
OUTPUT_FILE_CSV = "Кадастровые_номера_с_данными_f.csv"

# Имена колонок
CADASTRAL_COL = "Кадастровый №"
NEW_COLUMNS = [
    "Тип геометрии",
    "Координаты (GeoJSON)",
    "Площадь",
    "Категория",
    "Использование",
    "Адрес",
    "Статус",
    "Собственность",
    "Кад. стоимость",
    "Дата рег.",
    "Источник"
]

# Параметры обработки
SAVE_INTERVAL = 10  # Сохранять каждые N строк
MIN_DELAY = 1.0  # Минимальная задержка между запросами (секунды)
MAX_DELAY = 1.6  # Максимальная задержка между запросами (секунды)

# Точка возобновления
# ВНИМАНИЕ: Укажите индекс строки, с которой начинать обработку (0-based!)
# Если вы остановились "на 17385 строке", и это была последняя обработанная — начинайте с 17385.
# Если вы остановились ДО обработки 17385 — начинайте с 17384.
# Обычно: если скрипт упал на idx=17384 — начинайте с 17384.
START_FROM_ROW = 0


def load_input_data(file_path: str, cadastral_column: str) -> pd.DataFrame:
    """
    Загружает входной Excel файл с кадастровыми номерами.

    Args:
        file_path: Путь к Excel файлу
        cadastral_column: Название колонки с кадастровыми номерами

    Returns:
        DataFrame с данными из Excel

    Raises:
        ValueError: Если колонка с кадастровыми номерами не найдена
    """
    print("Чтение Excel-файла...")
    df = pd.read_excel(file_path, dtype={cadastral_column: str})

    if cadastral_column not in df.columns:
        raise ValueError(
            f"Столбец '{cadastral_column}' не найден. "
            f"Доступные колонки: {list(df.columns)}"
        )

    total_rows = len(df)
    print(f"Всего записей в Excel: {total_rows}")

    return df


def prepare_dataframe(df: pd.DataFrame, new_columns: list) -> pd.DataFrame:
    """
    Подготавливает DataFrame, добавляя новые пустые колонки.

    Args:
        df: Исходный DataFrame
        new_columns: Список новых колонок для добавления

    Returns:
        DataFrame с добавленными колонками
    """
    df_result = df.copy()
    for col in new_columns:
        if col not in df_result.columns:
            df_result[col] = ""
    return df_result


def load_previous_results(
    df: pd.DataFrame,
    csv_path: str,
    new_columns: list,
    cadastral_column: str
) -> pd.DataFrame:
    """
    Загружает ранее сохраненные результаты из CSV файла.

    Args:
        df: Текущий DataFrame
        csv_path: Путь к CSV файлу с сохраненными результатами
        new_columns: Список колонок с результатами
        cadastral_column: Название колонки с кадастровыми номерами

    Returns:
        DataFrame с восстановленными данными
    """
    if not os.path.exists(csv_path):
        return df

    print(f"Загружаем частично обработанные данные из {csv_path}...")
    try:
        df_saved = pd.read_csv(csv_path, dtype={cadastral_column: str})
        min_len = min(len(df), len(df_saved))

        for col in new_columns:
            if col in df_saved.columns:
                df.iloc[:min_len, df.columns.get_loc(col)] = \
                    df_saved[col].iloc[:min_len].values

        print(f"Успешно загружено данных для {min_len} строк.")
    except Exception as e:
        print(f"⚠️ Не удалось загрузить CSV: {e}. Продолжаем с пустыми данными.")

    return df


def get_cadastral_data(cadastral_code: str) -> Optional[Dict[str, Any]]:
    """
    Получает данные из Росреестра по кадастровому номеру.

    Args:
        cadastral_code: Кадастровый номер участка

    Returns:
        Словарь с данными участка или None в случае ошибки
    """
    try:
        area = Area(cadastral_code)
        feature = area.get_geometry()

        if not feature or "geometry" not in feature:
            return None

        geom_type = feature["geometry"]["type"]
        coords = feature["geometry"]["coordinates"]
        props = feature.get("properties", {})
        opts = props.get("options", {})
        source = "API"

        # Попытка улучшить полигон через изображение
        if geom_type == "Polygon":
            try:
                geojson_poly = area.to_geojson_poly(dumps=False)
                if (geojson_poly and
                    geojson_poly.get("geometry", {}).get("type") == "Polygon"):
                    coords = geojson_poly["geometry"]["coordinates"]
                    source = "Изображение (улучшенный полигон)"
            except Exception:
                pass

        return {
            "geometry_type": geom_type,
            "coordinates": coords,
            "area": opts.get("land_record_area_verified") or opts.get("specified_area"),
            "category": opts.get("land_record_category_type"),
            "usage": opts.get("permitted_use_established_by_document"),
            "address": opts.get("readable_address"),
            "status": opts.get("status"),
            "ownership": opts.get("ownership_type"),
            "cost": opts.get("cost_value"),
            "registration_date": opts.get("registration_date"),
            "source": source
        }

    except Exception:
        return None


def process_cadastral_row(
    df: pd.DataFrame,
    idx: int,
    cadastral_column: str,
    pbar: tqdm
) -> None:
    """
    Обрабатывает одну строку с кадастровым номером.

    Args:
        df: DataFrame для обновления
        idx: Индекс строки
        cadastral_column: Название колонки с кадастровыми номерами
        pbar: Объект прогресс-бара
    """
    code = str(df.iloc[idx][cadastral_column]).strip()

    # Пропуск пустых значений
    if not code or code.lower() in ["nan", "none", "", "–"]:
        pbar.set_postfix({"Статус": "Пропуск"})
        return

    pbar.set_description(f"Обработка: {code}")

    data = get_cadastral_data(code)

    if data:
        df.at[idx, "Тип геометрии"] = data["geometry_type"]
        df.at[idx, "Координаты (GeoJSON)"] = json.dumps(
            data["coordinates"],
            ensure_ascii=False
        )
        df.at[idx, "Площадь"] = data["area"]
        df.at[idx, "Категория"] = data["category"]
        df.at[idx, "Использование"] = data["usage"]
        df.at[idx, "Адрес"] = data["address"]
        df.at[idx, "Статус"] = data["status"]
        df.at[idx, "Собственность"] = data["ownership"]
        df.at[idx, "Кад. стоимость"] = data["cost"]
        df.at[idx, "Дата рег."] = data["registration_date"]
        df.at[idx, "Источник"] = data["source"]

        pbar.set_postfix({
            "Результат": f"✅ {data['geometry_type']} ({data['source']})"
        })
    else:
        pbar.set_postfix({"Результат": "❌ Данных нет"})


def save_results(df: pd.DataFrame, csv_path: str, xlsx_path: str) -> None:
    """
    Сохраняет результаты в CSV и Excel файлы.

    Args:
        df: DataFrame с результатами
        csv_path: Путь для сохранения CSV
        xlsx_path: Путь для сохранения Excel
    """
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    df.to_excel(xlsx_path, index=False)


def main() -> None:
    """
    Основная функция для обработки кадастровых номеров.
    """
    # Загрузка и подготовка данных
    df = load_input_data(INPUT_FILE, CADASTRAL_COL)
    df = prepare_dataframe(df, NEW_COLUMNS)
    df = load_previous_results(df, OUTPUT_FILE_CSV, NEW_COLUMNS, CADASTRAL_COL)

    total_rows = len(df)

    # Проверка START_FROM_ROW
    if START_FROM_ROW > total_rows:
        raise ValueError(
            f"START_FROM_ROW ({START_FROM_ROW}) больше общего числа строк "
            f"({total_rows})"
        )

    print(f"Начинаем обработку с индекса {START_FROM_ROW} "
          f"(всего строк: {total_rows})...")

    # Прогресс-бар
    pbar = tqdm(
        total=total_rows,
        initial=START_FROM_ROW,
        desc="Обработка записей",
        unit="запись"
    )

    # Основной цикл обработки
    for idx in range(START_FROM_ROW, total_rows):
        process_cadastral_row(df, idx, CADASTRAL_COL, pbar)

        # Периодическое сохранение
        if (idx + 1) % SAVE_INTERVAL == 0:
            df.to_csv(OUTPUT_FILE_CSV, index=False, encoding='utf-8-sig')
            pbar.set_postfix({"Сохранено": f"до строки {idx + 1}"})

        # Задержка между запросами
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)

        pbar.update(1)

    pbar.close()

    # Финальное сохранение
    save_results(df, OUTPUT_FILE_CSV, OUTPUT_FILE_XLSX)
    print(f"✅ Готово! Обработано {total_rows} записей.")


if __name__ == "__main__":
    main()
