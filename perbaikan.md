# 📋 Perbaikan Tubes DKA — Instruksi Implementasi Detail

> [!IMPORTANT]
> File ini berisi instruksi perbaikan yang harus dikerjakan **secara berurutan** dari Task 1 hingga Task 7.
> Setiap task memiliki file target, baris yang harus diubah, kode sebelum/sesudah, dan cara verifikasi.
> **JANGAN skip task** — beberapa task bergantung pada task sebelumnya.

## Lokasi File Project

Semua file berada di dalam folder:
```
c:\Users\ASUS\Documents\SIR Tel-U\SEMESTER 4\DKA\SIRDRF_DKA\
```

File yang akan dimodifikasi:
- `TubesDKA.ipynb` — Notebook utama
- `app.py` — Aplikasi web Streamlit  
- `README.md` — Dokumentasi project

---

## TASK 1: Sinkronkan Parameter Output Fuzzy (KRITIS)

### Masalah
Parameter fungsi keanggotaan output (Mamdani) dan singleton Sugeno **berbeda** di 3 file. Ini harus diseragamkan.

### Keputusan: Gunakan Parameter dari Notebook sebagai Sumber Kebenaran

Parameter yang benar (dari notebook) adalah:
- **Mamdani Output Murah**: `(0, 12000, 22000)`
- **Mamdani Output Standar**: `(18000, 28000, 38000)`
- **Mamdani Output Premium**: `(32000, 42000, 52000)`
- **Mamdani Output Mewah**: `(48000, 75000, 120000)`
- **Sugeno Singletons** (20 nilai, satu per rule): `[75000, 12000, 28000, 42000, 75000, 12000, 28000, 75000, 28000, 12000, 75000, 12000, 12000, 42000, 28000, 28000, 28000, 42000, 42000, 12000]`

---

### TASK 1A: Perbaiki `app.py` — Fungsi `defuzzify_mamdani`

**File**: `app.py`
**Baris**: sekitar baris 104-135

**CARI kode ini** (fungsi `defuzzify_mamdani` di bagian Python, BUKAN di dalam string HTML):

```python
def defuzzify_mamdani(output_fuzzy):
    w_murah = output_fuzzy["Murah"]
    w_standar = output_fuzzy["Standar"]
    w_premium = output_fuzzy["Premium"]
    w_mewah = output_fuzzy["Mewah"]

    # Diskritisasi harga dari $0 s.d. $100,000 dengan langkah 500
    y_vals = np.arange(0, 100001, 500)
    numerator = 0
    denominator = 0

    for y in y_vals:
        # Optimized Mamdani peak centers (aligned with Sugeno optimized singletons)
        mu_murah = triangle_member(y, 0, 3500, 13500)
        mu_standar = triangle_member(y, 14400, 24400, 34400)
        mu_premium = triangle_member(y, 15400, 25400, 35400)
        mu_mewah = triangle_member(y, 41100, 68300, 120000)
```

**GANTI 4 baris `mu_*` di atas** menjadi:

```python
        mu_murah = triangle_member(y, 0, 12000, 22000)
        mu_standar = triangle_member(y, 18000, 28000, 38000)
        mu_premium = triangle_member(y, 32000, 42000, 52000)
        mu_mewah = triangle_member(y, 48000, 75000, 120000)
```

Juga **ganti komentar** di atasnya dari:
```python
        # Optimized Mamdani peak centers (aligned with Sugeno optimized singletons)
```
menjadi:
```python
        # Himpunan fuzzy output harga (segitiga) — sinkron dengan notebook
```

---

### TASK 1B: Perbaiki `app.py` — Fungsi `defuzzify_sugeno`

**File**: `app.py`
**Baris**: sekitar baris 138-150

**CARI kode ini**:

```python
def defuzzify_sugeno(rules):
    # Mathematically optimized singleton (constant) output values for the 20 rules
    z = [
        68300, 3500, 24400, 25400, 68300, 3500, 24400, 68300, 24400, 3500,
        68300, 3500, 3500, 25400, 24400, 24400, 24400, 25400, 25400, 3500
    ]
```

**GANTI** seluruh array `z` dan komentar menjadi:

```python
def defuzzify_sugeno(rules):
    # Singleton output values per rule — sinkron dengan notebook
    z = [
        75000, 12000, 28000, 42000, 75000, 12000, 28000, 75000, 28000, 12000,
        75000, 12000, 12000, 42000, 28000, 28000, 28000, 42000, 42000, 12000
    ]
```

---

### TASK 1C: Perbaiki `app.py` — Fungsi JavaScript di dalam string `BENTO_GRID_HTML`

Ini bagian yang rumit. Di dalam `app.py`, ada string Python multi-line raksasa bernama `BENTO_GRID_HTML` (dimulai dari sekitar baris 185). Di dalam string ini ada kode JavaScript yang **juga** berisi fungsi fuzzy. Kamu harus mencari dan mengganti parameter di sana juga.

**File**: `app.py`
**Lokasi**: Di dalam string `BENTO_GRID_HTML`, di bagian `<script>`, cari fungsi JavaScript berikut.

**Cara menemukan**: Gunakan fitur pencarian/grep untuk mencari teks berikut di dalam `app.py`:

#### 1C-i: Cari fungsi JavaScript `defuzzifyMamdani`

Cari teks ini di dalam app.py (akan berada di dalam string BENTO_GRID_HTML):
```
function defuzzifyMamdani
```

Di dalam fungsi tersebut, akan ada baris-baris seperti:
```javascript
const muMurah = triangleMember(y, 0, 3500, 13500);
const muStandar = triangleMember(y, 14400, 24400, 34400);
const muPremium = triangleMember(y, 15400, 25400, 35400);
const muMewah = triangleMember(y, 41100, 68300, 120000);
```

**GANTI** menjadi:
```javascript
const muMurah = triangleMember(y, 0, 12000, 22000);
const muStandar = triangleMember(y, 18000, 28000, 38000);
const muPremium = triangleMember(y, 32000, 42000, 52000);
const muMewah = triangleMember(y, 48000, 75000, 120000);
```

#### 1C-ii: Cari fungsi JavaScript `defuzzifySugeno`

Cari teks ini di dalam app.py:
```
function defuzzifySugeno
```

Di dalam fungsi tersebut, akan ada array `z` seperti:
```javascript
const z = [68300, 3500, 24400, 25400, 68300, 3500, 24400, 68300, 24400, 3500, 68300, 3500, 3500, 25400, 24400, 24400, 24400, 25400, 25400, 3500];
```

**GANTI** menjadi:
```javascript
const z = [75000, 12000, 28000, 42000, 75000, 12000, 28000, 75000, 28000, 12000, 75000, 12000, 12000, 42000, 28000, 28000, 28000, 42000, 42000, 12000];
```

---

### TASK 1D: Perbaiki `README.md` — Bagian Output Fuzzy

**File**: `README.md`
**Baris**: sekitar baris 33-41

**CARI blok ini**:

```markdown
### 2. Variabel Output (Price)
* **Fuzzy Mamdani (Output berupa Himpunan Fuzzy Kontinu)**:
  * *Murah*: Himpunan segitiga (0, 15.000, 30.000)
  * *Standar*: Himpunan segitiga (20.000, 35.000, 50.000)
  * *Mewah*: Himpunan segitiga (40.000, 50.000, 100.000)
* **Fuzzy Sugeno Orde Nol (Output berupa Nilai Tunggal / Singleton)**:
  * *Murah*: $z = 15.000$
  * *Standar*: $z = 35.000$
  * *Mewah*: $z = 50.000$
```

**GANTI SELURUHNYA** menjadi:

```markdown
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
```

### TASK 1E: Perbarui README.md — Bagian Rule Base Konsekuen

**File**: `README.md`
**Baris**: sekitar baris 43-64

Di README, beberapa rule punya konsekuen yang hanya 3 kelas (Murah/Standar/Mewah). Harus disesuaikan agar konsisten dengan notebook yang punya 4 kelas. 

**CARI dan GANTI** baris-baris rule berikut satu per satu:

| Rule | SEBELUM (konsekuen lama) | SESUDAH (konsekuen baru, sesuai notebook) |
|------|--------------------------|-------------------------------------------|
| Rule 1 | `THEN price is **Mewah**` | `THEN price is **Mewah**` (tetap) |
| Rule 4 | `THEN price is **Mewah**` | `THEN price is **Premium**` |
| Rule 14 | `THEN price is **Mewah**` | `THEN price is **Premium**` |
| Rule 18 | `THEN price is **Standar**` | `THEN price is **Premium**` |
| Rule 19 | `THEN price is **Mewah**` | `THEN price is **Premium**` |

Konsekuen rule lainnya TIDAK BERUBAH. Verifikasi mapping dari notebook (`rule_evaluation_all` di TubesDKA.ipynb baris 565-571):
- **Murah** ← rule 2, 6, 10, 12, 13, 20
- **Standar** ← rule 3, 7, 9, 15, 16, 17
- **Premium** ← rule 4, 14, 18, 19
- **Mewah** ← rule 1, 5, 8, 11

### Verifikasi TASK 1

Setelah selesai, buka file `app.py` dan cari angka `3500`, `24400`, `25400`, `68300`, `13500`, `14400`, `15400`, `34400`, `35400`, `41100`. **Tidak boleh ada satupun angka tersebut** yang muncul sebagai parameter membership function atau singleton. Jika masih ada, berarti ada yang terlewat — cari dan ganti.

---

## TASK 2: Isi Data Kelompok di Notebook (KRITIS)

### Masalah
Cell pertama notebook masih berisi placeholder.

### Instruksi

**File**: `TubesDKA.ipynb`  
**Cell**: Cell markdown pertama (cell_type: "markdown", baris notebook sekitar baris 7-22)

**CARI teks ini** di dalam array `source` cell pertama:

```
"1. **Nama Lengkap 1** - NIM: **NIM Anggota 1**\n",
"2. **Nama Lengkap 2** - NIM: **NIM Anggota 2**\n",
"3. **Nama Lengkap 3** - NIM: **NIM Anggota 3**\n",
"\n",
"**KELAS:** [Masukkan Kelas Anda, misal: IF-44-01]\n",
```

**INSTRUKSI**: Tampilkan pesan kepada user bahwa mereka HARUS mengisi sendiri data berikut:
- Nama lengkap dan NIM setiap anggota kelompok
- Kelas (misal IF-44-01)

Jangan isi dengan data sembarang. Cukup **beri tahu user** bahwa ini harus diisi manual karena kamu tidak tahu informasinya. Tanyakan ke user apakah mereka ingin memberikan datanya sekarang.

---

## TASK 3: Perluas Evaluasi ke Seluruh Test Set (PENTING)

### Masalah
Evaluasi hanya dilakukan pada 25 sampel. Harus diperluas ke seluruh test set.

### Instruksi

**File**: `TubesDKA.ipynb`

#### TASK 3A: Ubah cell sampling

**Cari cell** yang berisi kode berikut (sekitar baris notebook 742-747):

```python
harga_asli = []
harga_prediksi_mamdani = []
harga_prediksi_sugeno = []
sample_data = test_data.head(25)
```

**GANTI** menjadi:

```python
harga_asli = []
harga_prediksi_mamdani = []
harga_prediksi_sugeno = []
sample_data = test_data  # Evaluasi pada SELURUH test set
```

#### TASK 3B: Ubah cell loop prediksi

**Cari cell** yang berisi kode berikut (sekitar baris notebook 756-762):

```python
for index, row in sample_data.iterrows():
    pred_mamdani = prediksi_harga(row["year"], row["mileage"], row["engineSize"], row["mpg"], row["tax"], method="Mamdani")
    pred_sugeno = prediksi_harga(row["year"], row["mileage"], row["engineSize"], row["mpg"], row["tax"], method="Sugeno")
    
    harga_prediksi_mamdani.append(pred_mamdani)
    harga_prediksi_sugeno.append(pred_sugeno)
    harga_asli.append(row["price"])
```

**GANTI** menjadi (tambahkan progress print):

```python
total = len(sample_data)
for idx, (index, row) in enumerate(sample_data.iterrows()):
    pred_mamdani = prediksi_harga(row["year"], row["mileage"], row["engineSize"], row["mpg"], row["tax"], method="Mamdani")
    pred_sugeno = prediksi_harga(row["year"], row["mileage"], row["engineSize"], row["mpg"], row["tax"], method="Sugeno")
    
    harga_prediksi_mamdani.append(pred_mamdani)
    harga_prediksi_sugeno.append(pred_sugeno)
    harga_asli.append(row["price"])
    
    if (idx + 1) % 500 == 0 or (idx + 1) == total:
        print(f"Progress: {idx + 1}/{total} data selesai dievaluasi...")

print(f"\nTotal data yang dievaluasi: {total}")
```

#### TASK 3C: Ubah cell print perbandingan

**Cari cell** yang berisi kode ini (sekitar baris notebook 772-779):

```python
print("Perbandingan Prediksi Harga Mobil Bekas (Mamdani vs Sugeno):\n")
for i in range(len(harga_asli)):
    kat_mamdani = kategori_mobil(harga_prediksi_mamdani[i])
    kat_sugeno = kategori_mobil(harga_prediksi_sugeno[i])
    print(f"Data ke-{i+1:02d} | Harga Asli: ${harga_asli[i]:,.2f}")
    print(f"        -> Mamdani : ${harga_prediksi_mamdani[i]:,.2f} ({kat_mamdani})")
    print(f"        -> Sugeno  : ${harga_prediksi_sugeno[i]:,.2f} ({kat_sugeno})")
    print("-" * 50)
```

**GANTI SELURUHNYA** menjadi (hanya print 10 sampel pertama + ringkasan):

```python
print("Perbandingan Prediksi Harga Mobil Bekas (Mamdani vs Sugeno):")
print(f"Menampilkan 10 sampel pertama dari {len(harga_asli)} data uji:\n")

for i in range(min(10, len(harga_asli))):
    kat_asli = kategori_mobil(harga_asli[i])
    kat_mamdani = kategori_mobil(harga_prediksi_mamdani[i])
    kat_sugeno = kategori_mobil(harga_prediksi_sugeno[i])
    print(f"Data ke-{i+1:02d} | Asli: ${harga_asli[i]:>10,.2f} ({kat_asli})")
    print(f"           | Mamdani: ${harga_prediksi_mamdani[i]:>10,.2f} ({kat_mamdani})")
    print(f"           | Sugeno:  ${harga_prediksi_sugeno[i]:>10,.2f} ({kat_sugeno})")
    print("-" * 55)

print(f"\n... dan {len(harga_asli) - 10} data lainnya (total {len(harga_asli)} data)")
```

#### TASK 3D: Update markdown cell tentang evaluasi

**Cari cell markdown** yang berisi teks (sekitar baris notebook 731-733):

```
Kita membandingkan hasil prediksi kedua model fuzzy *from scratch* ini dengan harga riil pada **25 data teratas dari Test Set**
```

**GANTI** teks `**25 data teratas dari Test Set**` menjadi `**seluruh Test Set**`

Dan ganti:
```
untuk menghitung metrik error
```
menjadi:
```
untuk menghitung metrik error secara komprehensif
```

### Verifikasi TASK 3

Setelah dijalankan, cell metrik MAE/MSE/RMSE dan Confusion Matrix akan otomatis menggunakan seluruh test set karena variabel `harga_asli`, `harga_prediksi_mamdani`, dan `harga_prediksi_sugeno` sekarang berisi seluruh data. Tidak perlu mengubah cell metrik.

---

## TASK 4: Fix Bug `triangleMember` di Notebook (PENTING)

### Masalah
Fungsi `triangleMember` di notebook tidak punya `return 0` di akhir sebagai fallback. Jika tidak ada kondisi terpenuhi, Python mengembalikan `None`.

### Instruksi

**File**: `TubesDKA.ipynb`

**Cari cell** yang berisi kode ini (sekitar baris notebook 194-200):

```python
def triangleMember(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
```

**GANTI SELURUHNYA** menjadi:

```python
def triangleMember(x, a, b, c):
    """Fungsi keanggotaan segitiga (triangular membership function).
    Parameter: x = nilai input, a = batas kiri, b = puncak, c = batas kanan.
    """
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0
```

Perubahan:
1. Tambah docstring
2. `return 0` → `return 0.0` (konsisten float)
3. Tambah `return 0.0` di akhir sebagai safety fallback

### Verifikasi TASK 4

Jalankan cell pengujian yang sudah ada:
```python
triangleMember(20000, 0, 20000, 40000)
```
Hasilnya harus `1.0`.

---

## TASK 5: Tambahkan Scatter Plot Perbandingan (PENTING)

### Masalah
Tidak ada visualisasi scatter plot harga asli vs prediksi.

### Instruksi

**File**: `TubesDKA.ipynb`

**Tambahkan cell baru** SETELAH cell Confusion Matrix (setelah cell yang berisi `plt.tight_layout()` dan `plt.show()` untuk confusion matrix, sekitar baris notebook 870).

**Sisipkan cell markdown baru**:
```markdown
#### 7.2. Visualisasi Scatter Plot — Harga Asli vs Prediksi
Scatter plot menunjukkan seberapa dekat prediksi fuzzy dengan harga asli. Garis merah putus-putus menunjukkan prediksi ideal (prediksi = asli). Semakin dekat titik-titik ke garis, semakin akurat model.
```

**Sisipkan cell code baru** tepat setelah cell markdown di atas:

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot Mamdani
axes[0].scatter(harga_asli, harga_prediksi_mamdani, alpha=0.3, s=10, color='#1f77b4')
axes[0].plot([0, max(harga_asli)], [0, max(harga_asli)], 'r--', linewidth=1, label='Prediksi Ideal')
axes[0].set_xlabel('Harga Asli ($)')
axes[0].set_ylabel('Harga Prediksi Mamdani ($)')
axes[0].set_title('Scatter Plot — Fuzzy Mamdani')
axes[0].legend()
axes[0].set_xlim(0, max(harga_asli) * 1.05)
axes[0].set_ylim(0, max(harga_prediksi_mamdani) * 1.05)

# Plot Sugeno
axes[1].scatter(harga_asli, harga_prediksi_sugeno, alpha=0.3, s=10, color='#2ca02c')
axes[1].plot([0, max(harga_asli)], [0, max(harga_asli)], 'r--', linewidth=1, label='Prediksi Ideal')
axes[1].set_xlabel('Harga Asli ($)')
axes[1].set_ylabel('Harga Prediksi Sugeno ($)')
axes[1].set_title('Scatter Plot — Fuzzy Sugeno')
axes[1].legend()
axes[1].set_xlim(0, max(harga_asli) * 1.05)
axes[1].set_ylim(0, max(harga_prediksi_sugeno) * 1.05)

plt.tight_layout()
plt.show()
```

### Verifikasi TASK 5

Setelah menjalankan cell, harus muncul 2 scatter plot berdampingan. Titik-titik harus tersebar, dan garis merah putus-putus diagonal harus terlihat.

---

## TASK 6: Tambahkan Implementasi MAE/MSE Manual (BAGUS)

### Masalah
Saat ini metrik menggunakan `sklearn`. Menambahkan versi manual lebih meyakinkan bahwa implementasi benar-benar "from scratch".

### Instruksi

**File**: `TubesDKA.ipynb`

**Tambahkan cell markdown baru** SEBELUM cell MAE (sebelum cell yang berisi `mae_mamdani = mean_absolute_error(...)`, sekitar baris notebook 789).

**Sisipkan cell markdown**:
```markdown
#### 7.0. Implementasi Metrik Evaluasi From Scratch
Sebelum menggunakan pustaka `sklearn` sebagai validasi, kita menghitung metrik MAE, MSE, dan RMSE secara manual untuk membuktikan pemahaman rumus.
```

**Sisipkan cell code baru** tepat setelah markdown di atas:

```python
# === IMPLEMENTASI METRIK FROM SCRATCH ===

# MAE (Mean Absolute Error) = (1/n) * Σ|actual - predicted|
def hitung_mae(actual, predicted):
    n = len(actual)
    total_error = 0
    for i in range(n):
        total_error += abs(actual[i] - predicted[i])
    return total_error / n

# MSE (Mean Squared Error) = (1/n) * Σ(actual - predicted)²
def hitung_mse(actual, predicted):
    n = len(actual)
    total_error = 0
    for i in range(n):
        total_error += (actual[i] - predicted[i]) ** 2
    return total_error / n

# RMSE (Root Mean Squared Error) = √MSE
def hitung_rmse(actual, predicted):
    return hitung_mse(actual, predicted) ** 0.5

# Hitung metrik manual
mae_mamdani_manual = hitung_mae(harga_asli, harga_prediksi_mamdani)
mae_sugeno_manual = hitung_mae(harga_asli, harga_prediksi_sugeno)
mse_mamdani_manual = hitung_mse(harga_asli, harga_prediksi_mamdani)
mse_sugeno_manual = hitung_mse(harga_asli, harga_prediksi_sugeno)
rmse_mamdani_manual = hitung_rmse(harga_asli, harga_prediksi_mamdani)
rmse_sugeno_manual = hitung_rmse(harga_asli, harga_prediksi_sugeno)

print("=== EVALUASI METRIK (IMPLEMENTASI FROM SCRATCH) ===")
print(f"MAE  Mamdani : {mae_mamdani_manual:>12,.2f}    |  MAE  Sugeno : {mae_sugeno_manual:>12,.2f}")
print(f"MSE  Mamdani : {mse_mamdani_manual:>16,.2f}  |  MSE  Sugeno : {mse_sugeno_manual:>16,.2f}")
print(f"RMSE Mamdani : {rmse_mamdani_manual:>12,.2f}    |  RMSE Sugeno : {rmse_sugeno_manual:>12,.2f}")
```

Cell-cell `sklearn` yang sudah ada (MAE, MSE, RMSE) **JANGAN dihapus** — biarkan sebagai validasi silang. Hasilnya harus identik.

### Verifikasi TASK 6

Bandingkan output metrik manual dengan output metrik sklearn. Nilai MAE, MSE, dan RMSE harus **sama persis** (atau berbeda di angka desimal terakhir karena floating point).

---

## TASK 7: Update Analisis Markdown di Notebook (PENTING)

### Masalah
Analisis perbandingan di cell markdown terakhir masih menyebut "25 data uji" dan angka lama.

### Instruksi

**File**: `TubesDKA.ipynb`

**Cari cell markdown terakhir** (sekitar baris notebook 876-896) yang berisi teks analisis perbandingan.

**CARI teks**:
```
Dari 25 data uji Test Set, kedua metode menghasilkan **Akurasi Kategori sebesar 48.00%** (12 dari 25 sampel benar)
```

**GANTI** menjadi:
```
Dari seluruh data uji Test Set (~2.600 sampel), akurasi kategori dihitung berdasarkan hasil prediksi kedua metode
```

**CARI teks**:
```
Nilai akurasi ini naik dramatis (sebelumnya 20%) berkat penalaan parameter keanggonaan input-output (4 kelas harga) dan penghilangan celah *No Rule Active*.
```

**GANTI** menjadi:
```
Nilai akurasi dipengaruhi oleh penalaan parameter keanggotaan input-output (4 kelas harga). Evaluasi pada seluruh test set memberikan gambaran performa yang lebih representatif.
```

**CARI teks**:
```
| **Akurasi Kategori (25 Data)** | **48.00%** (12 dari 25 benar) | **48.00%** (12 dari 25 benar) |
```

**GANTI** menjadi:
```
| **Akurasi Kategori (Full Test Set)** | Dihitung pada seluruh data uji | Dihitung pada seluruh data uji |
```

> [!NOTE]
> Angka akurasi baru akan muncul setelah notebook dijalankan ulang. Setelah dijalankan, update baris ini dengan angka akurasi yang benar dari output cell `acc_mamdani` dan `acc_sugeno`.

### Verifikasi TASK 7

Pastikan TIDAK ada lagi teks "25 data" atau "25 sampel" di cell markdown analisis.

---

## TASK 8: Update README.md — Bagian Hasil Evaluasi (PENTING)

### Instruksi

**File**: `README.md`  
**Baris**: sekitar baris 83-100

**CARI blok ini**:

```markdown
## 📊 Hasil Evaluasi Performa (Mamdani vs Sugeno)

Pengujian performa dilakukan pada **25 sampel data uji acak** dari dataset nyata [merc.csv](...), menghasilkan evaluasi berikut:

* **Mean Absolute Error (MAE)**:
  * **Fuzzy Mamdani**: `25,101.33`
  * **Fuzzy Sugeno**: `23,405.47` *(Sugeno lebih rendah sebesar ~6.7%)*
* **Mean Squared Error (MSE)**:
  * **Fuzzy Mamdani**: `1,175,925,987.53` *(Mamdani lebih rendah sebesar ~5.6%)*
  * **Fuzzy Sugeno**: `1,245,296,935.93`
* **Root Mean Squared Error (RMSE)**:
  * **Fuzzy Mamdani**: `34,291.78` *(Mamdani lebih rendah)*
  * **Fuzzy Sugeno**: `35,288.77`
```

**GANTI SELURUHNYA** menjadi:

```markdown
## 📊 Hasil Evaluasi Performa (Mamdani vs Sugeno)

Pengujian performa dilakukan pada **seluruh data uji (20% test set, ~2.600 sampel)** dari dataset nyata [merc.csv](data/merc.csv), dengan metrik MAE, MSE, RMSE, dan Akurasi Klasifikasi Kategori (Confusion Matrix).

> **Catatan**: Angka metrik evaluasi di bawah ini akan diperbarui setelah notebook dijalankan ulang dengan parameter yang telah disinkronkan.
```

> [!IMPORTANT]
> Setelah notebook dijalankan ulang sepenuhnya, ambil angka MAE/MSE/RMSE yang baru dari output notebook dan masukkan ke README. Jangan biarkan README berisi angka evaluasi yang sudah tidak valid.

---

## Urutan Pelaksanaan

```
1. TASK 1A-1E → Sinkronkan parameter (KRITIS)
2. TASK 2     → Ingatkan user isi data kelompok (KRITIS)
3. TASK 4     → Fix bug triangleMember (CEPAT)
4. TASK 3A-3D → Perluas evaluasi (PENTING)
5. TASK 6     → Tambah metrik manual (CEPAT)
6. TASK 5     → Tambah scatter plot (CEPAT)
7. TASK 7     → Update analisis markdown (TEKS)
8. TASK 8     → Update README evaluasi (TEKS)
```

Setelah semua task selesai:
1. **Jalankan ulang seluruh notebook** dari awal (Kernel → Restart & Run All)
2. Ambil angka metrik terbaru dari output
3. Update README.md dan cell markdown analisis dengan angka terbaru
4. Test `streamlit run app.py` — pastikan web berjalan tanpa error
5. Commit ke git
