import joblib
import pandas as pd
import numpy as np
import os

class DemandPredictor:
    def __init__(self, model_path='model_demand.pkl', pipeline_path='pipeline.pkl'):
        """Load artefak model dan pipeline fitur saat class diinisialisasi."""
        # Pastikan path file benar saat dijalankan dari app.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.model = joblib.load(os.path.join(base_dir, model_path))
        self.pipeline = joblib.load(os.path.join(base_dir, pipeline_path))
        self.expected_features = self.pipeline['fitur_input']

    def predict(self, raw_input_dict):
        """
        Fungsi untuk menerima input dari Streamlit, memprosesnya, dan mengembalikan prediksi.
        raw_input_dict harus berupa dictionary dengan list, contoh:
        {'id_poktan': [1], 'id_komoditas': [1], 'harga_satuan_transaksi': [30000], ...}
        """
        # 1. Konversi ke DataFrame
        df = pd.DataFrame(raw_input_dict)
        
        # 2. One-Hot Encoding fitur fase_musim (Rendeng/Gadu/Bera)
        if 'fase_musim' in df.columns:
            df_encoded = pd.get_dummies(df, columns=['fase_musim'])
        else:
            df_encoded = df
            
        # 3. Alignment Fitur (Crucial! Mencegah error kalau kolom musim nggak lengkap)
        # reindex akan mengisi kolom yang hilang dengan 0 sesuai saat model ditraining
        df_ready = df_encoded.reindex(columns=self.expected_features, fill_value=0)
        
        # 4. Prediksi Volume (pastikan tidak ada minus)
        prediction = self.model.predict(df_ready)
        return np.maximum(0, prediction)[0] # Kembalikan nilai tunggal positif