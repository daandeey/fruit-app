import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, insert, MetaData, Table

def buat_koneksi():
    """Membuat koneksi ke database MySQL menggunakan SQLAlchemy"""
    try:
        # Format connection string: mysql+driver://username:password@host/database
        print("Koneksi ke database berhasil")
        return engine
    except Exception as e:
        print(f"Terjadi error: '{e}'")
        return None

def tampilkan_dataframe(koneksi):
    """Menampilkan data buah dalam bentuk DataFrame"""
    try:
        query = "SELECT * FROM fruits"
        df = pd.read_sql(query, koneksi)
        
        print("\n=== DATA BUAH ===")
        print(df)
        return df
    except Exception as e:
        print(f"Terjadi error: '{e}'")
        return None

def tambah_buah_baru(koneksi):
    """Menambahkan data buah baru menggunakan SQLAlchemy Core dengan benar"""
    print("\n=== TAMBAH BUAH BARU ===")
    try:
        # Input data dari user
        nama = input("Masukkan nama buah: ")
        kategori = input("Masukkan kategori buah: ")
        harga = int(input("Masukkan harga (Rp): "))
        stok = int(input("Masukkan jumlah stok: "))
        
        # Membuat metadata dan merefleksikan tabel
        metadata = MetaData()
        fruits_table = Table('fruits', metadata, autoload_with=koneksi)
        
        # Membuat statement INSERT yang benar
        stmt = insert(fruits_table).values(
            name=nama,
            category=kategori,
            price=harga,
            stock=stok
        )
        
        # Eksekusi statement
        with koneksi.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        
        print(f"\nBuah '{nama}' berhasil ditambahkan!")
        print(f"ID buah baru: {result.inserted_primary_key[0]}")
        
    except ValueError:
        print("Error: Harga dan stok harus berupa angka")
    except Exception as e:
        print(f"Terjadi error database: {e}")

def hitung_mean(koneksi):
    """Menghitung nilai mean/rata-rata dari kolom numerik"""
    try:
        df = pd.read_sql("SELECT * FROM fruits", koneksi)
        kolom_numerik = df.select_dtypes(include=['int64', 'float64']).columns
        
        print("\nKolom numerik yang tersedia:")
        for i, kolom in enumerate(kolom_numerik, 1):
            print(f"{i}. {kolom}")
            
        pilihan = input("Pilih kolom untuk menghitung mean (masukkan angka): ")
        
        try:
            kolom_terpilih = kolom_numerik[int(pilihan)-1]
            nilai_mean = df[kolom_terpilih].mean()
            print(f"\nNilai rata-rata dari kolom '{kolom_terpilih}': {nilai_mean:.2f}")
        except (IndexError, ValueError):
            print("Pilihan tidak valid!")
            
    except Exception as e:
        print(f"Terjadi error: '{e}'")

def tampilkan_visualisasi(koneksi):
    """Menampilkan visualisasi data berdasarkan kolom yang dipilih"""
    try:
        df = pd.read_sql("SELECT * FROM fruits", koneksi)
        
        print("\nKolom yang tersedia:")
        for i, kolom in enumerate(df.columns[1:], 1):  # Skip kolom ID
            print(f"{i}. {kolom}")
            
        pilihan = input("Pilih kolom untuk visualisasi (masukkan angka): ")
        
        try:
            kolom_terpilih = df.columns[1:][int(pilihan)-1]
            
            plt.figure(figsize=(10, 6))
            
            if df[kolom_terpilih].dtype == 'object':  # Untuk data kategorikal
                print(f"\nDistribusi Kategori pada Kolom '{kolom_terpilih}'")
                counts = df[kolom_terpilih].value_counts()
                sns.barplot(x=counts.index, y=counts.values)
                plt.title(f'Distribusi {kolom_terpilih}')
                plt.xticks(rotation=45)
            else:  # Untuk data numerik
                print(f"\nDistribusi Nilai pada Kolom '{kolom_terpilih}'")
                sns.histplot(df[kolom_terpilih], kde=True)
                plt.title(f'Distribusi {kolom_terpilih}')
                
            plt.tight_layout()
            plt.show()
            
        except (IndexError, ValueError):
            print("Pilihan tidak valid!")
            
    except Exception as e:
        print(f"Terjadi error: '{e}'")

def main():
    # Membuat koneksi ke database
    engine = buat_koneksi()
    if not engine:
        return
    
    try:
        while True:
            print("\n=== MENU UTAMA ===")
            print("1. Tampilkan data buah")
            print("2. Tambah buah baru")
            print("3. Hitung rata-rata kolom numerik")
            print("4. Tampilkan visualisasi data")
            print("5. Keluar dari program")
            
            pilihan = input("Masukkan pilihan Anda (1-5): ")
            
            if pilihan == "1":
                tampilkan_dataframe(engine)
            elif pilihan == "2":
                tambah_buah_baru(engine)
            elif pilihan == "3":
                hitung_mean(engine)
            elif pilihan == "4":
                tampilkan_visualisasi(engine)
            elif pilihan == "5":
                print("Terima kasih, program dihentikan.")
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan 1-5.")
                
    finally:
        # Menutup koneksi database
        engine.dispose()
        print("Koneksi database ditutup")

if __name__ == "__main__":
    main()