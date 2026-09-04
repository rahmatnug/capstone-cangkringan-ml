import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def generate_cangkringan_data(
    start_date: str = "2024-01-01",
    end_date: str = "2026-08-31",
    random_seed: int = 42,
) -> pd.DataFrame:
    """Menghasilkan data sintetis kebutuhan pupuk tingkat desa berbasis deret waktu

    dengan mempertimbangkan siklus musim tanam lokal Cangkringan.
    """
    np.random.seed(random_seed)

    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    records = []

    # Master data produk pupuk
    products = [
        {"id": "P01", "nama": "Pupuk Organik Cair (POC)", "satuan": "Liter", "base_price": 25000, "shelf_life": 90},
        {"id": "P02", "nama": "Pupuk Organik Padat", "satuan": "Kg", "base_price": 15000, "shelf_life": 180},
        {"id": "P03", "nama": "Formula Starter Mikroba", "satuan": "Liter", "base_price": 35000, "shelf_life": 60},
    ]

    # Kelompok tani perwakilan dusun di Cangkringan
    poktan_list = ["Poktan Merapi Makmur", "Poktan Sumber Subur", "Poktan Tani Mandiri", "Poktan Hijau Lestari"]

    for current_date in date_range:
        month = current_date.month

        # Penentuan fase musim lokal Cangkringan
        if month in [11, 12, 1, 2, 3]:
            musim = "Rendeng"  # Musim Hujan / Tanam Utama
            curah_hujan = np.random.uniform(150, 350)
            demand_multiplier = 1.8
        elif month in [4, 5, 6, 7]:
            musim = "Gadu"  # Musim Kemarau / Tanam Kedua
            curah_hujan = np.random.uniform(50, 120)
            demand_multiplier = 1.2
        else:
            musim = "Bera"  # Masa Istirahat Lahan
            curah_hujan = np.random.uniform(10, 40)
            demand_multiplier = 0.5

        for prod in products:
            for poktan in poktan_list:
                # Variasi harga wajar (+/- 10%)
                price_noise = np.random.uniform(-0.1, 0.1)
                harga_satuan = round(prod["base_price"] * (1 + price_noise), -2)

                # Base volume berdasarkan tipe produk
                if prod["id"] == "P01":
                    base_volume = 40
                elif prod["id"] == "P02":
                    base_volume = 120
                else:
                    base_volume = 15

                # Elastisitas harga sederhana: harga naik -> demand turun tipis
                price_elasticity = 1 - (price_noise * 0.5)

                # Kalkulasi estimasi demand aktual dengan noise
                noise = np.random.normal(1.0, 0.15)
                volume_demand = int(base_volume * demand_multiplier * price_elasticity * noise)
                volume_demand = max(0, volume_demand)

                # Simulasi kapasitas stok gudang komunal
                stok_awal = int(base_volume * demand_multiplier * np.random.uniform(0.7, 1.4))

                # Penjualan aktual dibatasi ketersediaan stok fisik
                volume_terjual = min(volume_demand, stok_awal)
                stok_akhir = max(0, stok_awal - volume_terjual)

                records.append(
                    {
                        "tanggal": current_date.strftime("%Y-%m-%d"),
                        "poktan": poktan,
                        "produk_id": prod["id"],
                        "nama_produk": prod["nama"],
                        "satuan": prod["satuan"],
                        "fase_musim": musim,
                        "curah_hujan_mm": round(curah_hujan, 1),
                        "harga_satuan": int(harga_satuan),
                        "volume_permintaan_aktual": volume_demand,
                        "volume_terjual": volume_terjual,
                        "stok_akhir": stok_akhir,
                    }
                )

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "synthetic_demand_cangkringan.csv")

    df_synthetic = generate_cangkringan_data()
    df_synthetic.to_csv(file_path, index=False)
    print(f"Dataset berhasil digenerate: {file_path}")
    print(f"Total baris: {len(df_synthetic)}")
    print(f"Rentang tanggal: {df_synthetic['tanggal'].min()} s/d {df_synthetic['tanggal'].max()}")