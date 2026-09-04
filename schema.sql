-- Skema Database Relasional (schema.sql) untuk PostgreSQL
-- (Revisi: Penambahan Fitur Cuaca, Harga, dan RESTRICT Constraint)

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
    masa_simpan_hari INTEGER -- Fitur baru untuk alert penurunan mutu mikroba
);

CREATE TABLE Permintaan_Poktan (
    id_permintaan SERIAL PRIMARY KEY,
    id_poktan INTEGER NOT NULL REFERENCES Poktan(id_poktan) ON DELETE RESTRICT,
    id_komoditas INTEGER NOT NULL REFERENCES Komoditas(id_komoditas) ON DELETE RESTRICT,
    tanggal_permintaan DATE NOT NULL,
    volume_permintaan DECIMAL(10,2) NOT NULL,
    harga_satuan_transaksi DECIMAL(10,2) NOT NULL, -- Revisi: Harga fluktuatif
    fase_musim VARCHAR(50) NOT NULL,               -- Revisi: Faktor Musim
    curah_hujan_mm DECIMAL(10,2) NOT NULL,         -- Revisi: Faktor Cuaca
    status_data VARCHAR(20) DEFAULT 'Cleaned'
);

CREATE TABLE Stok_Gudang (
    id_stok SERIAL PRIMARY KEY,
    id_komoditas INTEGER NOT NULL REFERENCES Komoditas(id_komoditas) ON DELETE RESTRICT,
    tanggal_catat DATE NOT NULL,
    volume_stok_aktual DECIMAL(10,2) NOT NULL,
    threshold_minimum DECIMAL(10,2) NOT NULL,
    tgl_kadaluarsa DATE -- Sinkron dengan masa_simpan_hari di komoditas
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
