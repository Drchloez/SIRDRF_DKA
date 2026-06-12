# 🚗 Prediksi Harga Mobil Bekas Mercedes-Benz — Logika Fuzzy Mamdani & Sugeno (From Scratch)

Project ini merupakan implementasi sistem kecerdasan buatan untuk mengestimasi/memprediksi harga mobil bekas Mercedes-Benz menggunakan metode **Fuzzy Mamdani** dan **Fuzzy Sugeno** secara *from scratch* (tanpa menggunakan library fuzzy eksternal). Project ini disusun untuk memenuhi **Tugas Besar Dasar Kecerdasan Buatan (DKA)**, Universitas Telkom.

---

## 📂 Struktur Project

```text
SIRDRF_DKA/
│
├── data/
│   └── merc.csv              # Dataset nyata mobil bekas Mercedes-Benz (13.119 baris)
│
├── TubesDKA.ipynb            # Notebook analisis data (EDA), pemodelan fuzzy, dan evaluasi
├── app.py                    # Aplikasi web interaktif berbasis Streamlit
└── README.md                 # Dokumentasi lengkap project
```

---

## 📝 Detail Himpunan & Aturan Fuzzy

Sistem fuzzy ini dirancang dengan **5 variabel input** dan **1 variabel output**:

### 1. Variabel Input (Linguistic Variables)
* **Tahun Mobil (`year`)**: Himpunan Fuzzy: *Old* (2010–2018), *Medium* (2015–2021), *New* (2018–2023).
* **Mileage / Jarak Tempuh (`mileage`)**: Himpunan Fuzzy: *Low* (0–40.000), *Medium* (30.000–70.000), *High* (60.000–100.000+).
* **Kapasitas Mesin (`engineSize`)**: Himpunan Fuzzy: *Kecil* (0–2.0), *Sedang* (1.5–3.5), *Besar* (3.0–6.0+).
* **Konsumsi Bahan Bakar (`mpg`)**: Himpunan Fuzzy: *Boros* (0–40), *Standar* (30–70), *Irit* (60–80+).
* **Pajak (`tax`)**: Himpunan Fuzzy: *Murah* (0–200), *Standar* (150–450), *Mahal* (400–600+).

### 2. Variabel Output (Price)
* **Fuzzy Mamdani (Output berupa Himpunan Fuzzy Kontinu — 4 Kelas)**:
  * *Murah*: Himpunan segitiga (0, 12.000, 22.000)
  * *Standar*: Himpunan segitiga (18.000, 28.000, 38.000)
  * *Premium*: Himpunan segitiga (32.000, 42.000, 52.000)
  * *Mewah*: Himpunan segitiga (48.000, 75.000, 120.000)
* **Fuzzy Sugeno Orde Nol (Output berupa Nilai Tunggal / Singleton per Rule)**:
  * Rule yang mengarah ke *Murah*: $z = 12.000$
  * Rule yang mengarah ke *Standar*: $z = 28.000$
  * Rule yang mengarah ke *Premium*: $z = 42.000$
  * Rule yang mengarah ke *Mewah*: $z = 75.000$

### 3. Rule Base (20 Aturan Inferensi)
Aturan logika fuzzy didefinisikan secara komprehensif menggunakan operator `AND` (diwakili oleh fungsi `min`) sebagai berikut:
1. `Rule 1`: IF year is **New** AND mileage is **Low** AND engine is **Besar** THEN price is **Mewah**
2. `Rule 2`: IF year is **Old** AND mileage is **High** THEN price is **Murah**
3. `Rule 3`: IF mpg is **Irit** AND tax is **Murah** THEN price is **Standar**
4. `Rule 4`: IF year is **New** AND mileage is **Low** AND mpg is **Irit** THEN price is **Premium**
5. `Rule 5`: IF engine is **Besar** AND tax is **Mahal** THEN price is **Mewah**
6. `Rule 6`: IF year is **Old** AND mileage is **High** AND mpg is **Boros** THEN price is **Murah**
7. `Rule 7`: IF engine is **Kecil** AND mpg is **Irit** THEN price is **Standar**
8. `Rule 8`: IF tax is **Mahal** AND mileage is **Low** THEN price is **Mewah**
9. `Rule 9`: IF year is **Medium** AND mileage is **Medium** THEN price is **Standar**
10. `Rule 10`: IF engine is **Kecil** AND mileage is **High** THEN price is **Murah**
11. `Rule 11`: IF year is **New** AND engine is **Besar** THEN price is **Mewah**
12. `Rule 12`: IF year is **Old** AND tax is **Murah** THEN price is **Murah**
13. `Rule 13`: IF mpg is **Boros** AND tax is **Mahal** THEN price is **Murah**
14. `Rule 14`: IF mileage is **Low** AND mpg is **Irit** THEN price is **Premium**
15. `Rule 15`: IF engine is **Sedang** AND year is **Medium** THEN price is **Standar**
16. `Rule 16`: IF year is **Medium** AND mpg is **Standar** THEN price is **Standar**
17. `Rule 17`: IF mileage is **Medium** AND tax is **Standar** THEN price is **Standar**
18. `Rule 18`: IF engine is **Sedang** AND mileage is **Medium** THEN price is **Premium**
19. `Rule 19`: IF year is **New** AND engine is **Sedang** THEN price is **Premium**
20. `Rule 20`: IF year is **Old** AND engine is **Kecil** THEN price is **Murah**

---

## 🔬 Perbedaan Implementasi (From Scratch)

### 1. Fuzzy Mamdani (Centroid / Center of Area)
* Nilai implikasi untuk setiap aturan dievaluasi menggunakan metode *clipping* (`min`).
* Nilai luaran di-agregasi menggunakan fungsi `max`.
* Defuzzifikasi dilakukan dengan menghitung pusat gravitasi wilayah fuzzy output secara numerik melalui diskritisasi semesta output dari \$0 s.d. \$100.000 dengan langkah \$500:
  $$Y_{COA} = \frac{\sum_{y} y \cdot \mu_{comb}(y)}{\sum_{y} \mu_{comb}(y)}$$

### 2. Fuzzy Sugeno Orde Nol
* Luaran aturan berupa nilai tegas (*singleton/konstanta*).
* Defuzzifikasi dihitung menggunakan rata-rata terbobot (*weighted average*) dari kekuatan aktif (*firing strength*) dari 20 aturan secara langsung:
  $$Z = \frac{\sum_{i=1}^{20} w_i \cdot z_i}{\sum_{i=1}^{20} w_i}$$

---

## 📊 Hasil Evaluasi Performa (Mamdani vs Sugeno)

Pengujian performa dilakukan pada **seluruh data uji (20% test set, 2.572 sampel)** dari dataset nyata [merc.csv](data/merc.csv), menghasilkan evaluasi berikut (Setelah *Fine-Tuning*):

* **Mean Absolute Error (MAE)**:
  * **Fuzzy Mamdani**: `6,817.37`
  * **Fuzzy Sugeno**: `6,574.06` *(Sugeno lebih rendah sebesar ~3.5%)*
* **Mean Squared Error (MSE)**:
  * **Fuzzy Mamdani**: `100,336,508.85`
  * **Fuzzy Sugeno**: `96,956,988.47` *(Sugeno lebih rendah sebesar ~3.3%)*
* **Root Mean Squared Error (RMSE)**:
  * **Fuzzy Mamdani**: `10,016.81`
  * **Fuzzy Sugeno**: `9,846.67` *(Sugeno lebih rendah sebesar ~1.7%)*
* **Akurasi Klasifikasi Kategori (Classification Accuracy)**:
  * **Fuzzy Mamdani**: `57.85%` (1.488 dari 2.572 benar)
  * **Fuzzy Sugeno**: `63.30%` (1.628 dari 2.572 benar) *(Sugeno lebih tinggi sebesar ~5.45% akurasi)*

### Analisis Kualitatif & Interpretasi:
1. **Fuzzy Mamdani** lebih unggul pada nilai MSE dan RMSE yang berarti metode ini lebih tangguh terhadap lonjakan kesalahan (*outlier*), karena sifat daerah keanggotaan kontinu pada output memperhalus perubahan harga.
2. **Fuzzy Sugeno** lebih unggul pada MAE, yang berarti rata-rata penyimpangan prediksinya sedikit lebih dekat dengan harga aslinya secara linier.
3. **Efisiensi Komputasi**: Fuzzy Sugeno jauh lebih cepat secara komputasi karena proses defuzzifikasinya hanya berupa operasi aritmatika pembagian langsung, sementara Mamdani membutuhkan iterasi diskrit (integrasi numerik) di sepanjang semesta output.

---

## 🚀 Panduan Instalasi & Menjalankan

### 📦 Prasyarat & Instalasi Dependency
Pastikan Python 3.x telah terinstal. Pasang seluruh pustaka yang dibutuhkan dengan perintah:
```bash
pip install streamlit numpy pandas matplotlib scikit-learn
```

### 💻 Menjalankan Web App Streamlit
Untuk mencoba kalkulator estimasi harga secara real-time dan interaktif dengan hasil Mamdani & Sugeno yang ditampilkan berdampingan, jalankan:
```bash
streamlit run app.py
```

### 🌐 Menjalankan Web App Bento Grid (HTML/CSS/JS)
Project ini juga dilengkapi dengan aplikasi web interaktif berbasis HTML/CSS/JS statis dengan desain **Bento Grid** yang modern dan responsif. Aplikasi ini menjalankan seluruh perhitungan logika fuzzy di sisi klien secara real-time.
Untuk membukanya:
* Cukup klik dua kali berkas [index.html](file:///c:/Users/ASUS/Documents/SIR%20Tel-U/SEMESTER%204/DKA/SIRDRF_DKA/index.html) untuk membukanya langsung di peramban web pilihan Anda.
* Pilihan tipe model mobil yang dipilih akan menampilkan contoh visualisasi mobil Mercedes-Benz secara dinamis yang dimuat langsung dari berkas lokal di folder `assets/` (sehingga web dapat dijalankan 100% offline).

### 📓 Menjalankan Notebook Jupyter
Untuk meninjau proses analisis data (EDA) serta pembuktian rumus/perbandingan matematis:
```bash
jupyter notebook TubesDKA.ipynb
```

---

## 📂 Informasi Dataset & Pembagian Kelompok
* **Dataset nyata**: [Kaggle Mercedes Used Car Dataset](https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes?select=merc.csv&hl=id-IDJ)
* **Jumlah baris**: 13.119 data baris
* **Variabel input**: 5 kolom input (`year`, `mileage`, `engineSize`, `mpg`, `tax`)
* **Variabel output**: 1 kolom output (`price` - harga mobil bekas dalam USD)
