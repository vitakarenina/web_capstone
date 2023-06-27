-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 22 Jan 2023 pada 00.42
-- Versi server: 10.4.24-MariaDB
-- Versi PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_capstone`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `log_admin`
--

CREATE TABLE `log_admin` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `log_admin`
--

INSERT INTO `log_admin` (`id`, `username`, `email`, `password`) VALUES
(1, 'admin', 'admin@gmail.com', 'admin'),
(2, 'fiqih', 'fiqih@gmail.com', '12345');

-- --------------------------------------------------------

--
-- Struktur dari tabel `log_tilang`
--

CREATE TABLE `log_tilang` (
  `id` int(11) NOT NULL,
  `no_plat` varchar(50) NOT NULL,
  `filename` varchar(200) NOT NULL,
  `filename_pelanggaran` varchar(200) NOT NULL,
  `pelanggaran` varchar(50) NOT NULL,
  `akurasi` varchar(100) NOT NULL,
  `tanggal` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `log_users`
--

CREATE TABLE `log_users` (
  `nomor_plat` varchar(100) NOT NULL,
  `nomor_bpkb` varchar(100) NOT NULL,
  `pemilik` varchar(100) NOT NULL,
  `jenis_kendaraan` enum('Sepeda Motor') NOT NULL,
  `merk` enum('Honda','Yamaha','Suzuki','Kawasaki','Viar','Ducati','Harley') NOT NULL,
  `warna` varchar(20) NOT NULL,
  `alamat` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `log_admin`
--
ALTER TABLE `log_admin`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `log_tilang`
--
ALTER TABLE `log_tilang`
  ADD PRIMARY KEY (`id`),
  ADD KEY `no_plat` (`no_plat`);

--
-- Indeks untuk tabel `log_users`
--
ALTER TABLE `log_users`
  ADD PRIMARY KEY (`nomor_plat`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `log_admin`
--
ALTER TABLE `log_admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `log_tilang`
--
ALTER TABLE `log_tilang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
