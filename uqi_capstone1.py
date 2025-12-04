import pandas as pd
import numpy as np
import seaborn as sns
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import os
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'uqiuqian',     
    'database': 'uqi_capstone1'
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[FATAL ERROR] Gagal koneksi ke Database: {e}")
        print("Pastikan MySQL menyala dan database 'nilai_siswa' terinput.")
        sys.exit(1)

def fetch_data_as_df(query):
    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn)
        return df
    except Error as e:
        print(f"[ERROR] Query gagal: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

#---------------------------------------FITUR-FITUR YEAY---------------------------------------

def fitur_view_data():
    while True:
        clear_screen()
        print("=====MENU TAMPILKAN DATA=====")
        print("1. Tampilkan Semua Data")
        print("2. Tampilkan Berdasarkan Pelajaran")
        print("3. Tampilkan Berdasarkan Kelas")
        print("0. Kembali")

        pilihan = input("Pilih (nomor): ")

        if pilihan == '1':
            df = fetch_data_as_df("SELECT * FROM nilai_siswa")
            print(df.to_string(index=False))
            input("\nTekan Enter...")

        elif pilihan == '2':
            mapel_map = {
                '1': 'nilai_matematika', '2': 'nilai_fisika', '3': 'nilai_kimia',
                '4': 'nilai_biologi', '5': 'nilai_english', '6': 'nilai_bahasa_indonesia'
            }
            print("\nPilih Pelajaran:")
            print("1. Matematika | 2. Fisika | 3. Kimia | 4. Biologi | 5. English | 6. B.Indo")
            idx = input("Pilih (nomor): ")

            if idx in mapel_map:
                col = mapel_map[idx]
                query = f"SELECT nis, nama_siswa, kelas, {col} FROM nilai_siswa"
                df = fetch_data_as_df(query)
                print(f"\nData Nilai {col.replace('nilai_', '').capitalize()}:")
                print(df.to_string(index=False))
            else:
                print("Pilihan tidak valid.")
            input("\nTekan Enter...")

        elif pilihan == '3':
            df = fetch_data_as_df("SELECT * FROM nilai_siswa")
            kelas_list = sorted(df['kelas'].unique())
            print("Kelas Tersedia:")
            for i, k in enumerate(kelas_list, 1):
                print(f"{i}. {k}")
            
            try:
                idx_kelas = int(input("\n Pilih nomor kelas: ")) - 1

                if 0 <= idx_kelas <len(kelas_list):
                    target_kelas = kelas_list[idx_kelas]
                    query = f"SELECT * FROM nilai_siswa WHERE kelas = '{target_kelas}'"
                    df = fetch_data_as_df(query)

                    print(df.to_string(index=False))

                else:
                    print("Data tidak ditemukan untuk kelas tersebut.")

            except ValueError:
                print("Input harus angka.")
            except Exception as e:
                print(f"Error: {e}")
            input("\nTekan Enter...")

        elif pilihan =='0':
            break


def fitur_statistik():
    while True:
        clear_screen()
        print("=== STATISTIK NILAI (mean)===")
        print("1. Statistik Angkatan")
        print("2. Statistik Kelas")
        print("0. Kembali")

        pilihan = input("Pilih (nomor): ")

        if pilihan == '1':
            df = fetch_data_as_df("SELECT * FROM nilai_siswa")
            cols_nilai = [c for c in df.columns if 'nilai_' in c]
            
            print("===Statistik Angkatan===")
            print("Pelajaran tersedia:")
            for i, c in enumerate(cols_nilai, 1):
                print(f"{i}. {c.replace('nilai_', '').capitalize()}")
                
            try:
                idx = int(input("Pilih (nomor): ")) - 1
                if 0 <= idx < len(cols_nilai):
                    col = cols_nilai[idx]
                    col_name_display = col.replace('nilai_', '').capitalize()

                    # --- 1. Hitung Nilai ---
                    mean_val = df[col].mean()
                    max_val = df[col].max()
                    min_val = df[col].min()
                    
                    print(f"\n=== STATISTIK {col_name_display.upper()} ===")
                    print(f"Rata-rata Angkatan : {mean_val:.2f}")
                    
                    print(f"\n[+] Nilai Tertinggi: {max_val}")
                    print("    Diraih oleh:")

                    siswa_max = df[df[col] == max_val]
                    for i, row in siswa_max.iterrows():
                        print(f"    - {row['nama_siswa']} ({row['kelas']})")
                    
                    print(f"\n[-] Nilai Terendah : {min_val}")
                    print("    Dimiliki oleh:")

                    siswa_min = df[df[col] == min_val]
                    for i, row in siswa_min.iterrows():
                        print(f"    - {row['nama_siswa']} ({row['kelas']})")
                else:
                    print("Pilihan salah.")
            except ValueError:
                print("Input harus angka.")
            input("\nTekan Enter...")
        
        elif pilihan == '2':
            print("=== STATISTIK SPESIFIK PER KELAS ===")
        
            df = fetch_data_as_df("SELECT * FROM nilai_siswa")
            kelas_list = sorted(df['kelas'].unique())
            
            print("Kelas Tersedia:")
            for i, k in enumerate(kelas_list, 1):
                print(f"{i}. {k}")
                
            try:
                idx_kelas = int(input("\nPilih Nomor Kelas: ")) - 1
                
                if 0 <= idx_kelas < len(kelas_list):
                    target_kelas = kelas_list[idx_kelas]
                    
                    df_filtered = df[df['kelas'] == target_kelas]
                    
                    print(f"\n--- [ DATA TERPILIH: KELAS {target_kelas} ] ---")
                    cols = [c for c in df_filtered.columns if 'nilai_' in c]
                    
                    print("Pilih Mapel untuk dianalisis:")
                    for i, c in enumerate(cols, 1): 
                        print(f"{i}. {c.replace('nilai_', '').capitalize()}")
                        
                    idx_mapel = int(input("Nomor Mapel: ")) - 1
                    
                    if 0 <= idx_mapel < len(cols):
                        col = cols[idx_mapel]
                        col_display = col.replace('nilai_', '').capitalize()
                        
                        mean_val = df_filtered[col].mean()
                        max_val = df_filtered[col].max()
                        min_val = df_filtered[col].min()
                        
                        print(f"\n=== HASIL ANALISIS KELAS {target_kelas} ({col_display.upper()}) ===")
                        print(f"Rata-rata Kelas {target_kelas} : {mean_val:.2f}")
                        
                        print(f"\n[+] Tertinggi di {target_kelas}: {max_val}")
                        siswa_max = df_filtered[df_filtered[col] == max_val]
                        for i, row in siswa_max.iterrows():
                            print(f"    - {row['nama_siswa']}") 
                        print(f"\n[-] Terendah di {target_kelas} : {min_val}")
                        siswa_min = df_filtered[df_filtered[col] == min_val]
                        for i, row in siswa_min.iterrows():
                            print(f"    - {row['nama_siswa']}")
                    
                    else:
                        print("Pilihan mapel tidak valid.")
                else:
                    print("Pilihan kelas tidak valid.")
                    
            except ValueError:
                print("Input harus angka.")
            except Exception as e:
                print(f"Error: {e}")
            input("\nTekan Enter...")
        elif pilihan =='0':
            break

def fitur_visualisasi():
    while True:
        clear_screen()
        print("=== VISUALISASI DATA ===")
        print("1. Pie Chart (Proporsi Gender)")
        print("2. Bar Plot (Jumlah Siswa per Kelas)")
        print("3. Histogram (Distribusi Nilai)")
        print("0. Kembali")
        
        pilihan = input("Pilih: ")
        df = fetch_data_as_df("SELECT * FROM nilai_siswa")
        
        if pilihan == '1':
            # Pie Chart Gender
            counts = df['jenis_kelamin'].value_counts()
            plt.figure(figsize=(6,6))
            plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
            plt.title('Proporsi Siswa Laki-laki vs Perempuan')
            print("Menampilkan Pie Chart...")
            plt.show()
            
        elif pilihan == '2':
            # Bar Plot Kelas
            counts = df['kelas'].value_counts().sort_index()
            plt.figure(figsize=(8,5))
            counts.plot(kind='bar', color='teal')
            plt.title('Jumlah Siswa Per Kelas')
            plt.xlabel('Kelas')
            plt.ylabel('Jumlah Siswa')
            plt.xticks(rotation=0)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            print("Menampilkan Bar Plot...")
            plt.show()
            
        elif pilihan == '3':
            # Histogram Nilai
            cols_nilai = [c for c in df.columns if 'nilai_' in c]
            
            print("\nPilih Mapel untuk Histogram:")
            for i, c in enumerate(cols_nilai, 1):
                nama_mapel = c.replace('nilai_', '').capitalize()
                print(f"{i}. {nama_mapel}")
            
            try:
                idx = int(input("\nMasukkan nomor mapel: ")) - 1
                
                if 0 <= idx < len(cols_nilai):
                    col_input = cols_nilai[idx]
                    nama_display = col_input.replace("nilai_", "").capitalize()
                    
                    # 4. Plotting
                    plt.figure(figsize=(8,5))
                    plt.hist(df[col_input], bins=10, color='orange', edgecolor='black')
                    plt.title(f'Distribusi Nilai {nama_display}')
                    plt.xlabel('Nilai')
                    plt.ylabel('Frekuensi')
                    plt.grid(axis='y', linestyle='--', alpha=0.7)
                    print("Menampilkan Histogram...")
                    plt.show()
                else:
                    print("Nomor mapel tidak valid.")
                    input("Tekan Enter...")
                    
            except ValueError:
                print("Input harus berupa angka.")
                input("Tekan Enter...")

        elif pilihan =='0':
            break 

def fitur_tambah_data():
    clear_screen()
    print("=== TAMBAH DATA SISWA (INSERT TO MYSQL) ===")
    
    try:
        nis = input("NIS (Unique): ")
        nama = input("Nama Siswa: ")
        jk = input("Jenis Kelamin (L/P): ").upper()
        kelas = input("Kelas (cth: XI A): ").upper()
        
        nilai = {}
        mapels = ['matematika', 'fisika', 'kimia', 'biologi', 'english', 'bahasa_indonesia']
        for m in mapels:
            while True:
                try:
                    val = int(input(f"Nilai {m.capitalize()}: "))
                    if 0 <= val <= 100:
                        nilai[f'nilai_{m}'] = val
                        break
                    else:
                        print("Nilai harus 0-100.")
                except ValueError:
                    print("Harus angka.")

        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """INSERT INTO nilai_siswa (nis, nama_siswa, jenis_kelamin, kelas, 
                 nilai_matematika, nilai_fisika, nilai_kimia, nilai_biologi, 
                 nilai_english, nilai_bahasa_indonesia) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        val = (nis, nama, jk, kelas, 
               nilai['nilai_matematika'], nilai['nilai_fisika'], nilai['nilai_kimia'],
               nilai['nilai_biologi'], nilai['nilai_english'], nilai['nilai_bahasa_indonesia'])
        
        cursor.execute(sql, val)
        conn.commit()
        print("\n[SUKSES] Data berhasil disimpan ke MySQL!")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"\n[ERROR MySQL] Gagal menyimpan: {e}")
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")
    
    input("Tekan Enter...")

def fitur_update_nilai():
    clear_screen()
    
    print("=== UPDATE NILAI SISWA ===")
    nis_cari = input("Masukkan NIS Siswa: ")
    
    query_cari = f"SELECT * FROM nilai_siswa WHERE nis = '{nis_cari}'"
    df_siswa = fetch_data_as_df(query_cari)
    
    if not df_siswa.empty:
        row = df_siswa.iloc[0]
        nama = row['nama_siswa']
        kelas = row['kelas']
        
        print(f"\n[OK] Siswa Ditemukan: {nama} | Kelas: {kelas}")
        print("-" * 40)
        
        mapel_dict = {
            '1': 'nilai_matematika', '2': 'nilai_fisika', '3': 'nilai_kimia',
            '4': 'nilai_biologi', '5': 'nilai_english', '6': 'nilai_bahasa_indonesia'
        }
        
        print("Pilih Mapel yang mau diedit:")
        for key, val in mapel_dict.items():
            display_name = val.replace('nilai_', '').capitalize()
            nilai_saat_ini = row[val]
            print(f"{key}. {display_name} (Nilai saat ini: {nilai_saat_ini})")
            
        pilihan = input("\nPilih Nomor Mapel (1-6): ")
        
        if pilihan in mapel_dict:
            kolom_db = mapel_dict[pilihan]
            nama_mapel = kolom_db.replace('nilai_', '').capitalize()
            
            try:
                nilai_baru = int(input(f"Masukkan Nilai Baru untuk {nama_mapel}: "))
                if 0 <= nilai_baru <= 100:
                    
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    sql = f"UPDATE nilai_siswa SET {kolom_db} = %s WHERE nis = %s"
                    val = (nilai_baru, nis_cari)
                    
                    cursor.execute(sql, val)
                    conn.commit()
                    
                    print(f"\n[SUKSES] Data {nama} berhasil diperbarui.")
                    print(f"Mapel: {nama_mapel} | Nilai Lama: {row[kolom_db]} -> Nilai Baru: {nilai_baru}")
                    
                    cursor.close()
                    conn.close()
                else:
                    print("[ERROR] Nilai harus 0-100.")
            except ValueError:
                print("[ERROR] Harus angka.")
        else:
            print("[ERROR] Nomor mapel tidak valid.")
            
    else:
        print(f"\n Siswa dengan NIS {nis_cari} tidak ditemukan.")
    
    input("\nTekan Enter untuk kembali...")

def fitur_ranking_siswa():
    clear_screen()
    print("=== RANKING / LEADERBOARD SISWA ===")
    
    df = fetch_data_as_df("SELECT * FROM nilai_siswa")
    cols_nilai = [c for c in df.columns if 'nilai_' in c]
    
    df['skor_akhir'] = df[cols_nilai].mean(axis=1)
    
    print("Pilih Mode Ranking:")
    print("1. Ranking Satu Angkatan")
    print("2. Ranking Kelas")
    print("0. Kembali")
    
    pilihan = input("Pilih Menu: ")
    
    if pilihan == '1':
        print("\n--- TOP 10 SISWA SATU ANGKATAN ---")
        
        df_sorted = df.sort_values(by='skor_akhir', ascending=False).reset_index(drop=True)
        
        print(f"{'RANK':<5} | {'NAMA SISWA':<25} | {'KELAS':<8} | {'NILAI RATA-RATA'}")
        print("-" * 50)
        
        for i, row in df_sorted.head(10).iterrows():
            rank = i + 1
            nama = row['nama_siswa']
            kelas = row['kelas']
            nilai = row['skor_akhir']
            
            if len(nama) > 23: nama = nama[:20] + "..."
            
            print(f"{rank:<5} | {nama:<25} | {kelas:<8} | {nilai:.2f}")
            
        print("-" * 50)
        input("\nTekan Enter untuk kembali...")

    elif pilihan == '2':
        kelas_list = sorted(df['kelas'].unique())
        
        print("\nPilih Kelas:")
        for i, k in enumerate(kelas_list, 1):
            print(f"{i}. {k}")
            
        try:
            idx = int(input("Nomor Kelas: ")) - 1
            if 0 <= idx < len(kelas_list):
                target_kelas = kelas_list[idx]
                
                df_kelas = df[df['kelas'] == target_kelas].copy()
                
                df_sorted = df_kelas.sort_values(by='skor_akhir', ascending=False).reset_index(drop=True)
                
                print(f"\n--- RANKING KELAS {target_kelas} ---")
                print(f"{'RANK':<5} | {'NAMA SISWA':<30} | {'NILAI'}")
                print("-" * 50)
                
                for i, row in df_sorted.iterrows():
                    rank = i + 1
                    nama = row['nama_siswa']
                    nilai = row['skor_akhir']
                    print(f"{rank:<5} | {nama:<30} | {nilai:.2f}")
                    
                print("-" * 50)
            else:
                print("Kelas tidak valid.")
        except ValueError:
            print("Input harus angka.")
        
        input("\nTekan Enter untuk kembali...")
        
    elif pilihan == '0':
        return
    else:
        print("Pilihan tidak valid.")
        input("Tekan Enter...")

#   =======================================
#   MAIN MENU
#   =======================================
def main():
    while True:
        clear_screen()
        
        print("==========================================")
        print("   SISTEM MANAJEMEN NILAI SISWA    ")
        print("==========================================")
        print("1. Tampilkan Data (Tabel)")
        print("2. Statistik (Mean)")
        print("3. Visualisasi Data (Grafik)")
        print("4. Tambah Data Baru")
        print("5. Update Nilai Siswa")
        print("6. Ranking Siswa")
        print("0. Keluar")
        print("==========================================")
        
        menu = input("Pilih Menu: ")
        
        if menu == '1':
            fitur_view_data()
        elif menu == '2':
            fitur_statistik()
        elif menu == '3':
            fitur_visualisasi()
        elif menu == '4':
            fitur_tambah_data()
        elif menu == '5':
            fitur_update_nilai()
        elif menu == '6':
            fitur_ranking_siswa()
        elif menu == '0':
            print("Terima kasih!")
            break
        else:
            print("Menu tidak valid.")
            input("Tekan Enter...")


main()