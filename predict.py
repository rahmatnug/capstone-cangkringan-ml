import joblib
import pandas as pd
import numpy as np
import os

class DemandPredictor:
    def __init__(self, model_path='model_demand.pkl', pipeline_path='pipeline.pkl'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model = joblib.load(os.path.join(base_dir, model_path))
        self.pipeline = joblib.load(os.path.join(base_dir, pipeline_path))
        self.expected_features = self.pipeline['fitur_input']

    def _validate_and_clean_input(self, df):
        """Handling edge-cases: Missing, Outliers, Negative Values dari UI"""
        df_clean = df.copy()
        
        # 1. HARGA TRANSAKSI: Gak boleh minus/nol (kalo aneh, paksa cap di 1000)
        if 'harga_satuan_transaksi' in df_clean.columns:
            df_clean['harga_satuan_transaksi'] = np.maximum(1000.0, df_clean['harga_satuan_transaksi'])
            
        # 2. CURAH HUJAN: Batasi 0 s.d 600 mm (Batas logis cuaca ekstrem, sisanya outlier)
        if 'curah_hujan_mm' in df_clean.columns:
            df_clean['curah_hujan_mm'] = np.clip(df_clean['curah_hujan_mm'], 0.0, 600.0)
            
        # 3. HISTORICAL DEMAND: Lag dan Rolling tidak mungkin negatif
        hist_cols = ['lag_1w', 'lag_4w', 'lag_7w', 'rolling_mean_4w']
        for col in hist_cols:
            if col in df_clean.columns:
                df_clean[col] = np.maximum(0.0, df_clean[col])
                
        # 4. MISSING VALUES: Isi dengan 0 kalau UI nggak sengaja ngirim null
        df_clean = df_clean.fillna(0)
        
        return df_clean

    def predict(self, raw_input_dict):
        df = pd.DataFrame(raw_input_dict)
        
        # Bersihkan data sebelum masuk ke pemrosesan!
        df = self._validate_and_clean_input(df)
        
        if 'fase_musim' in df.columns:
            df_encoded = pd.get_dummies(df, columns=['fase_musim'])
        else:
            df_encoded = df
            
        df_ready = df_encoded.reindex(columns=self.expected_features, fill_value=0)
        prediction = self.model.predict(df_ready)
        
        return np.maximum(0, prediction)[0]