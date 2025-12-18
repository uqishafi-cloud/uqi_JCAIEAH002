## Project Overview
Proyek ini bertujuan untuk membangun model **Machine Learning (Regression)** yang dapat memprediksi nilai **Customer Lifetime Value (CLV)** pada perusahaan asuransi kendaraan.

Dengan memprediksi CLV secara akurat, perusahaan dapat mengidentifikasi segmen pelanggan yang paling berharga, mengoptimalkan biaya pemasaran (*Customer Acquisition Cost*), dan merancang strategi retensi yang lebih efektif.

## Business Understanding

### Latar Belakang Masalah
Perusahaan saat ini memiliki kesulitan dalam menentukan strategi marketing dan retensi yang tepat sasaran karena belum memiliki metode otomatis untuk memprediksi nilai masa depan (future value) dari seorang pelanggan.

Jika perusahaan memperlakukan semua pelanggan secara sama:

- Risiko Kehilangan Pelanggan Premium: Pelanggan bernilai tinggi mungkin pindah ke kompetitor karena kurangnya insentif atau penawaran khusus.
- Inefisiensi Biaya: Perusahaan mungkin membuang anggaran marketing untuk mempertahankan pelanggan yang sebenarnya merugikan (klaim tinggi, CLV rendah).

Oleh karena itu, perusahaan membutuhkan sebuah model Machine Learning yang dapat memprediksi nilai Customer Lifetime Value berdasarkan profil dan riwayat polis pelanggan.

### Tujuan Proyek
1.  Membangun model Regresi yang akurat untuk memprediksi angka Customer Lifetime Value (CLV) dari setiap pelanggan.
2.  Mengetahui faktor-faktor atau fitur apa saja yang paling mempengaruhi tinggi rendahnya CLV seorang pelanggan.
3.  Memberikan wawasan bisnis kepada tim marketing untuk merancang strategi promosi yang lebih efektif berdasarkan segmen nilai pelanggan.

---

## Methodology & Tech Stack

* **Bahasa Pemrograman:** Python
* **Libraries:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, XGBoost.
* **Pendekatan Machine Learning:** Supervised Learning (Regression).
* **Evaluation Metrics:** MAPE (Mean Absolute Percentage Error), MAE, RMSE.

### Alur Pengerjaan:
1.  **Data Preprocessing:** Handling missing values, One-Hot Encoding untuk fitur kategori, dan Scaling fitur numerik.
2.  **Model Benchmarking:** Membandingkan 5 algoritma (Linear Regression, KNN, Decision Tree, Random Forest, XGBoost).
3.  **Hyperparameter Tuning:** Mengoptimalkan model terbaik menggunakan `RandomizedSearchCV`.
4.  **Evaluation:** Menguji model pada *Unseen Data* (Data Test).
5.  **Interpretation:** Analisis *Feature Importance* untuk wawasan bisnis.

---

## Key Results

Setelah melalui proses eksperimen dan tuning, model **Decision Tree Regressor** terpilih sebagai model terbaik dengan performa sebagai berikut:

| Metric | Score (Data Test) | Interpretasi |
| :--- | :--- | :--- |
| **MAPE** | **9.53%** | Rata-rata prediksi meleset hanya sekitar 9.5% dari nilai asli. |
| **MAE** | **1,500.74** | Rata-rata deviasi prediksi dalam satuan mata uang. |
| **RMSE** | **4,532.87** | Indikasi error pada outlier. |

### Feature Importance (Faktor Penentu CLV)
Model menemukan bahwa **Demografi Pelanggan (Pendidikan, Status Pernikahan)** memiliki dampak minimal. Dua faktor utama yang mendominasi prediksi adalah:
1.  **Number of Policies (46.7%):** Jumlah polis yang dimiliki pelanggan.
2.  **Monthly Premium Auto (41.5%):** Besaran premi bulanan yang dibayarkan.

---

## Business Recommendations

Berdasarkan hasil analisis data, berikut adalah rekomendasi strategi untuk tim bisnis:

1.  **Fokus pada Cross-Selling (Bundling):**
    Karena *Number of Policies* adalah faktor terkuat, strategi utama haruslah mendorong pelanggan untuk memiliki lebih dari 1 polis (misal: Asuransi Mobil + Kesehatan). Berikan insentif diskon untuk pembelian *bundling*.

2.  **Segmentasi Layanan:**
    Gunakan model ini untuk men-*scoring* pelanggan baru. Pelanggan dengan prediksi CLV tinggi harus diprioritaskan dalam layanan (*VIP Service*) untuk mencegah *Churn*.

3.  **Optimalisasi Up-Selling:**
    Dorong pelanggan untuk mengambil paket proteksi tambahan (*Add-ons*) guna meningkatkan *Monthly Premium*, yang secara langsung akan meningkatkan CLV jangka panjang.

---

## Future Work
* Menambahkan data perilaku interaksi pelanggan (jumlah komplain, durasi panggilan CS).
* Mengimplementasikan teknik **Ensemble Stacking** untuk meningkatkan stabilitas prediksi.
* Deploy model menjadi API menggunakan **Flask/FastAPI** agar bisa digunakan Real-time oleh tim Sales.

---
**Author:** Uqi Shafi