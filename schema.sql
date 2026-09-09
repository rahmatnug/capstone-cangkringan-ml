-- Skema Database Relasional (schema.sql) untuk PostgreSQL
-- Revisi Final Sprint 1 (Sesuai SRS v1.1: CV Pandawa Kencana Multifarm)

DROP TABLE IF EXISTS Batch_Produksi CASCADE;
DROP TABLE IF EXISTS Hasil_Prediksi CASCADE;
DROP TABLE IF EXISTS Stok_Gudang CASCADE;
DROP TABLE IF EXISTS Permintaan_Poktan CASCADE;
DROP TABLE IF EXISTS Komoditas CASCADE;
DROP TABLE IF EXISTS Poktan CASCADE;
DROP TABLE IF EXISTS Pengguna CASCADE;

CREATE TABLE Poktan (
    id_poktan SERIAL PRIMARY KEY,
    nama_poktan VARCHAR(100) NOT NULL,
    wilayah_dusun VARCHAR(100) NOT NULL
);

CREATE TABLE Komoditas (
    id_komoditas SERIAL PRIMARY KEY,
    nama_komoditas VARCHAR(100) NOT NULL,
    satuan VARCHAR(20) NOT NULL,
    harga_satuan_estimasi DECIMAL(10,2),
    masa_simpan_hari INTEGER -- Untuk fitur alert EWS viabilitas mikroba (60-240 hari)
);

CREATE TABLE Permintaan_Poktan (
    id_permintaan SERIAL PRIMARY KEY,
    id_poktan INTEGER REFERENCES Poktan(id_poktan) ON DELETE RESTRICT, -- Dibuat bisa NULL untuk menampung transaksi Shopee yang tidak punya Poktan
    id_komoditas INTEGER NOT NULL REFERENCES Komoditas(id_komoditas) ON DELETE RESTRICT,
    kanal_distribusi VARCHAR(50) DEFAULT 'Offline Poktan', -- Fitur Omnichannel (Offline Poktan / Online Shopee)
    tanggal_permintaan DATE NOT NULL,
    volume_permintaan DECIMAL(10,2) NOT NULL,
    harga_satuan_transaksi DECIMAL(10,2) NOT NULL, 
    fase_musim VARCHAR(50) NOT NULL,               
    curah_hujan_mm DECIMAL(10,2) NOT NULL,         
    status_data VARCHAR(20) DEFAULT 'Cleaned'
);

CREATE TABLE Stok_Gudang (
    id_stok SERIAL PRIMARY KEY,
    id_komoditas INTEGER NOT NULL REFERENCES Komoditas(id_komoditas) ON DELETE RESTRICT,
    tanggal_catat DATE NOT NULL,
    volume_stok_aktual DECIMAL(10,2) NOT NULL,
    threshold_minimum DECIMAL(10,2) NOT NULL,
    tgl_kadaluarsa DATE 
);

CREATE TABLE Hasil_Prediksi (
    id_prediksi SERIAL PRIMARY KEY,
    id_komoditas INTEGER NOT NULL REFERENCES Komoditas(id_komoditas) ON DELETE RESTRICT,
    periode_t_plus_1 DATE NOT NULL,
    volume_prediksi DECIMAL(10,2) NOT NULL,
    confidence_interval DECIMAL(5,2),
    tanggal_inferensi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Batch_Produksi (
    id_batch SERIAL PRIMARY KEY,
    id_prediksi INTEGER NOT NULL REFERENCES Hasil_Prediksi(id_prediksi) ON DELETE RESTRICT,
    safety_buffer DECIMAL(10,2) NOT NULL,
    rekomendasi_sistem DECIMAL(10,2) NOT NULL,
    keputusan_final DECIMAL(10,2),
    status_batch VARCHAR(50)
);

CREATE TABLE Pengguna (
    id_pengguna SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    peran VARCHAR(50) NOT NULL
);

-- Seed Data / Master Produk CV Pandawa Kencana Multifarm
INSERT INTO Komoditas (nama_komoditas, satuan, harga_satuan_estimasi, masa_simpan_hari) VALUES
('GB Propunic', 'Liter', 30000, 90),
('GB Profeed', 'Liter', 30000, 180),
('GB Proquatic', 'Liter', 30000, 180),
('Pendawa Subur POC', 'Liter', 35000, 120),
('Agen Hayati', 'Saset/Kg', 25000, 60),
('Compossap', 'Zak', 25000, 240);
