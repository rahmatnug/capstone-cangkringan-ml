import pandas as pd
import numpy as np

df = pd.read_csv('synthetic_demand_data.csv')
mask = df['id_komoditas'] == 6
np.random.seed(42)
df.loc[mask, 'harga_satuan_transaksi'] = np.random.randint(140000, 150000, size=mask.sum())
df.to_csv('synthetic_demand_data.csv', index=False)
print("✅ DONE! Harga Agen Hayati berhasil di-update.")