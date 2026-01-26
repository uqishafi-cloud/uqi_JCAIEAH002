# 🔐 Smart HR AI Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![LangGraph](https://img.shields.io/badge/AI%20Agent-LangGraph-orange)
![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-green)

**Smart HR AI Assistant** adalah aplikasi Chatbot cerdas yang dirancang untuk membantu tim Human Resources (HR) dalam mempercepat proses rekrutmen. Aplikasi ini bukan sekadar "Tanya Jawab", melainkan sebuah **Agent** yang dapat mengambil tindakan (mencari resume, menghitung gaji) dengan lapisan keamanan **Role-Based Access Control (RBAC)** yang ketat.

---

## 📌 1. Intisari Project

Project ini membangun sebuah **AI Agent** menggunakan framework **LangGraph** yang terintegrasi dengan **Streamlit** sebagai antarmuka pengguna.

Fitur Utama:
* **Semantic Resume Search (RAG):** Mencari kandidat bukan hanya berdasarkan keyword, tapi berdasarkan konteks skill (menggunakan Vector Database Qdrant).
* **Secure Access (RBAC):** Membedakan hak akses antara **Manager/HR** (Full Access) dan **Intern** (Restricted Access).
* **Automated Tools:** Agent dibekali tools khusus untuk estimasi gaji dan pembuatan pertanyaan interview otomatis.
* **Cost Monitoring:** Melacak penggunaan token dan estimasi biaya per chat secara real-time.

---

## 💼 2. Business Problem & Solution

### 🔴 The Problem (Masalah Industri)
1.  **Data Overload:** HR menerima ratusan resume setiap hari. Screening manual memakan waktu dan melelahkan.
2.  **Security Risk:** Data gaji dan informasi pribadi kandidat sangat sensitif. Staff junior (misal: Intern) seringkali memiliki akses ke folder yang sama dengan Manager, meningkatkan risiko kebocoran data.
3.  **Inefisiensi Pencarian:** Pencarian tradisional (Ctrl+F) sering melewatkan kandidat potensial yang menggunakan istilah berbeda (misal: "Backend Dev" vs "Server-side Engineer").

### 🟢 The Solution (Solusi AI)
1.  **AI-Powered Screening:** Menggunakan RAG untuk menyaring resume dalam hitungan detik berdasarkan makna (semantik), bukan hanya kata kunci.
2.  **Role-Based Security:** Sistem secara otomatis memblokir akses ke data sensitif jika user tidak memiliki izin, meskipun user mencoba melakukan *prompt injection*.
3.  **Enterprise Efficiency:** Menggabungkan pencarian, kalkulasi gaji, dan persiapan interview dalam satu dashboard terintegrasi.

---

## ⚙️ 3. Cara Kerja (Arsitektur)

Sistem ini bekerja dengan alur sebagai berikut:

1.  **User Login:** User masuk via Streamlit. Sistem mengidentifikasi **Role** user (misal: `Manager` atau `Intern`).
2.  **Context Injection:** Saat User chatting, sistem menyisipkan informasi Role ke dalam prompt backend secara tersembunyi (`[SYSTEM INFO: User Role is Manager]`).
3.  **LangGraph Agent:**
    * Agent menerima pesan + info role.
    * Agent memilih **Tool** yang tepat.
4.  **Security Check:** Di dalam Tool, terdapat logika validasi: `if user_role not in ['HR', 'Manager']`. Jika tidak valid, tool menolak memberikan data.
5.  **Retrieval (Qdrant):** Jika akses valid, Tool mengambil data resume dari Vector Database.
6.  **Response:** LLM merangkum data dan menampilkannya ke User.

---

## 🛠️ 4. Daftar Tools Agent

Agent ini dilengkapi dengan 4 kemampuan (tools) spesifik:

1.  **`search_resume`** 🔒 *(Restricted)*
    * Mencari kandidat berdasarkan **Posisi/Jabatan** (Contoh: "Cari Marketing Manager").
    * Hanya untuk: HR, Manager
2.  **`search_by_skill`** 🔒 *(Restricted)*
    * Mencari kandidat berdasarkan **Skill Teknis** (Contoh: "Cari yang bisa Python & SQL").
    * Hanya untuk: HR, Manager
3.  **`estimasi_gaji`** 🔒 *(Restricted)*
    * Menghitung estimasi gaji berdasarkan tahun pengalaman.
    * Hanya untuk: HR, Manager
4.  **`generate_pertanyaan_interview`** 🌍 *(Public)*
    * Membuat daftar pertanyaan interview yang sulit/tricky.
    * Bisa diakses oleh **SEMUA ROLE** (termasuk Intern).

---

## 🚀 5. Cara Menjalankan Aplikasi

1.  **Ingest Data (Isi Database)**
    Jalankan script ini sekali untuk memasukkan data resume dummy ke Qdrant:
    ```bash
    python ingest.py
    ```

2.  **Jalankan Aplikasi**
    ```bash
    streamlit run app.py
    ```

---

## 🧪 6. Skenario Testing (Contoh Prompt)

Gunakan akun demo berikut untuk menguji fitur keamanan (RBAC).

### 👤 Akun Demo
| Username | Password | Role | Akses Data |
| :--- | :--- | :--- | :--- |
| `uqi` | `admin` | **HR** | ✅ Full Access |
| `herman` | `hermannakal` | **Intern** | ❌ Restricted |


### 💬 Contoh Prompt Pengujian

#### A. Login sebagai Manager / HR (Full Access)
* **Cari Kandidat:** "Tolong carikan kandidat yang berpengalaman di Python."
* **Cek Gaji:** "Berapa estimasi gajinya untuk pengalaman 5 tahun?"
* **Analisis:** "Siapa kandidat yang paling cocok untuk posisi Lead Developer?"

#### B. Login sebagai Intern (Akses Dibatasi)
* **Percobaan Ilegal:** "Cari resume Herman Sugiharto."
    * *Hasil:* Agent menjawab **"AKSES DITOLAK"**.
* **Tugas yang Diizinkan:** "Buatkan 3 pertanyaan interview sulit untuk skill Python."
    * *Hasil:* Agent **BERHASIL** membuatkan pertanyaan.