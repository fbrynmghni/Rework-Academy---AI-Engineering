"""
Sesi 3 — 3.4 Data Pipeline 

Isi bagian TODO sesuai instruksi. Setelah lengkap, jalankan script dengan:

    python pipeline.py

Input:  orders_dirty.csv
Output: orders_processed.csv
"""
from __future__ import annotations
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def load_data(filepath: str) -> pd.DataFrame:
    """Baca CSV lokal ke DataFrame."""
    # TODO: pakai pd.read_csv(filepath), return DataFrame-nya
    df = pd.read_csv(filepath)
    print(f'[load] {filepath} --> {len(df)} baris')
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Missing values + duplicates + format + noisy values."""
    
    before = len(df)

    # TODO: fill rating dengan mean
    df['rating'] = df['rating'].fillna(df['rating'].mean())

    # TODO: dropna subset=["city"]
    df = df.dropna(subset=['city'])

    # TODO: fill product_review yang null dengan ""
    df['product_review'] = df['product_review'].fillna("")

    # TODO: drop_duplicates()
    df = df.drop_duplicates()

    # TODO: category.str.lower().str.strip()
    df['category'] = df['category'].str.lower().str.strip()

    # TODO: pd.to_datetime(order_date, errors="coerce", format="mixed")
    df['order_date'] = pd.to_datetime(
        df['order_date'], errors='coerce', format='mixed'
    )

    # TODO: filter noisy values (price_idr > 0, quantity 1-100, rating 0-5)
    mask_bad = (
        (df['price_idr'] <= 0)
        | (df['quantity'] <= 0)
        | (df['quantity'] > 100)
        | (df['rating'] < 0)
        | (df['rating'] > 5)
    )
    df = df[~mask_bad.copy()]
    print(f'[clean] {before} --> {len(df)} baris ({before - len(df)} dibuang )')
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Scaling + encoding + text cleaning."""
    # TODO: MinMaxScaler untuk [price_idr, rating] -> [price_norm, rating_norm]
    scaler = MinMaxScaler()
    df[['price_idr', 'rating']] = scaler.fit_transform(df[['price_idr', 'rating']])
    
    # TODO: pd.get_dummies untuk kolom "category" dengan prefix "cat"
    df = pd.get_dummies(df, columns=['category'], prefix=['cat'])

    # TODO: buat review_clean (lowercase, hapus tanda baca, strip)
    df['review_clean'] = (
        df['product_review']
        .astype(str)
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.strip()
    )
    print(f"[transform] {df.shape[1]} kolom setelah transformasi")
    return df


def save_data(df: pd.DataFrame, filepath: str) -> None:
    """Simpan ke CSV."""
    # TODO: df.to_csv(filepath, index=False)
    df.to_csv(filepath, index=False)
    print(f"[save] {filepath}")


def main() -> None:
    print("Mulai jalankan pipeline...")
    df = load_data("../orders_dirty.csv")
    df = clean_data(df)
    df = transform_data(df)
    save_data(df, "orders_processed.csv")
    print("Pipeline selesai...")


if __name__ == "__main__":
    main()
