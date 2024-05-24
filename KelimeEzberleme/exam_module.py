from tkinter import messagebox
import customtkinter as tk
import sqlite3
import random
from datetime import datetime, timedelta

def exam():
    baglanti = sqlite3.connect("words.db")
    cursor = baglanti.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS words(turkish TEXT, english TEXT)")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bilinenler (
            id INTEGER PRIMARY KEY,
            turkish TEXT,
            english TEXT,
            dogru_cevap INTEGER,
            sorma_tarihi TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sorular (
            id INTEGER PRIMARY KEY,
            turkish TEXT,
            english TEXT,
            dogru_cevap INTEGER,
            sorma_tarihi TEXT
        )
    """)

    baglanti.commit()
    baglanti.close()

    def yeni_sorular_ekle(gun):
        baglanti = sqlite3.connect("words.db")
        cursor = baglanti.cursor()

        cursor.execute("SELECT * FROM bilinenler")
        dunden_bilinenler = cursor.fetchall()

        # Eğer dünden bilinenler varsa ve 3'ten fazla ise, rastgele 3 kelime seç
        if len(dunden_bilinenler) >= 3:
            bilinenler = random.sample(dunden_bilinenler, 3)
        else:
            # Eğer dünden bilinenler 3'ten azsa, tümünü al
            bilinenler = dunden_bilinenler

        # Rastgele yeni kelime
        cursor.execute(
            "SELECT turkish, english FROM words WHERE english NOT IN (SELECT english FROM bilinenler) ORDER BY RANDOM() LIMIT 10")
        yeni_kelimeler = cursor.fetchall()

        # Dünden bilinen kelimeler hariç 10 yeni kelimeyi ekle
        for kelime in yeni_kelimeler:
            cursor.execute("INSERT INTO sorular(turkish, english, dogru_cevap, sorma_tarihi) VALUES (?, ?, ?, ?)",
                           (kelime[0], kelime[1], 0, gun))

        # Öğrenci dünden bildiği 5 kelimenin 3 tanesini bu sefer bildi
        for kelime in bilinenler:
            cursor.execute("UPDATE sorular SET dogru_cevap = ?, sorma_tarihi = ? WHERE english = ?",
                           (6, gun, kelime[0]))

        baglanti.commit()
        baglanti.close()

    def rastgele_kelimeyi_goster():

        baglanti = sqlite3.connect("words.db")
        cursor = baglanti.cursor()

        # Bugünün tarihini al
        gun = datetime.now().date()

        # Eğer bugün için sorular yoksa, yeni soruları ekle
        cursor.execute("SELECT COUNT(*) FROM sorular WHERE sorma_tarihi = ?", (gun,))
        if cursor.fetchone()[0] == 0:
            yeni_sorular_ekle(gun)

        # Bugün için bir soruyu seç
        cursor.execute("SELECT english FROM sorular WHERE sorma_tarihi = ? ORDER BY RANDOM() LIMIT 1", (gun,))
        ingilizce_kelime = cursor.fetchone()[0]

        # CustomTkinter arayüzünü oluştur
        pencere = tk.CTk()
        pencere.title("Kelime Öğrenme Uygulaması")

        kelime_label = tk.CTkLabel(pencere, text=f"İngilizce kelime: {ingilizce_kelime}", font=("Arial", 18))
        kelime_label.pack(pady=10)

        cevap_entry = tk.CTkEntry(pencere, font=("Arial", 16))
        cevap_entry.pack(pady=10)
        baglanti.commit()
        baglanti.close()



        def cevabi_kontrol_et():

            baglanti = sqlite3.connect("words.db")
            cursor = baglanti.cursor()

            # Kullanıcının girdiği cevabı kontrol et
            turkce_cevap = cevap_entry.get().strip().lower()

            cursor.execute("SELECT turkish FROM sorular WHERE english = ?", (ingilizce_kelime,))
            dogru_turkce_cevap = cursor.fetchone()[0].lower()

            if turkce_cevap == dogru_turkce_cevap:
                # Doğru cevaplanmışsa, doğru cevap sayısını artır
                cursor.execute("UPDATE sorular SET dogru_cevap = dogru_cevap + 1 WHERE english = ?",
                               (ingilizce_kelime,))

                # Eğer doğru cevap sayısı 6 ise, bu soruyu bilinenler havuzuna taşı
                cursor.execute("SELECT dogru_cevap FROM sorular WHERE english = ?", (ingilizce_kelime,))
                dogru_cevap_sayisi = cursor.fetchone()[0]
                if dogru_cevap_sayisi >= 6:
                    cursor.execute("INSERT INTO bilinenler SELECT * FROM sorular WHERE english = ?",
                                   (ingilizce_kelime,))
                    cursor.execute("DELETE FROM sorular WHERE english = ?", (ingilizce_kelime,))

                sonuc_label.configure(text="Doğru!", fg="green")
            else:
                sonuc_label.configure(text="Yanlış!", fg="red")

        kontrol_button = tk.CTkButton(pencere, text="Cevabı Kontrol Et", command=cevabi_kontrol_et)
        kontrol_button.pack(pady=10)

        sonuc_label = tk.CTkLabel(pencere, text="", font=("Arial", 16))
        sonuc_label.pack(pady=10)
        baglanti.commit()


        pencere.mainloop()

    rastgele_kelimeyi_goster()


def rapor():
    baglanti = sqlite3.connect("words.db")
    cursor = baglanti.cursor()

    cursor.execute("SELECT COUNT(*) FROM sorular")
    toplam_soru_sayisi = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sorular WHERE dogru_cevap >= 6")
    dogru_cevap_sayisi = cursor.fetchone()[0]

    if toplam_soru_sayisi > 0:
        basari_yuzdesi = (dogru_cevap_sayisi / toplam_soru_sayisi) * 100
    else:
        basari_yuzdesi = 0

    messagebox.showinfo("Analiz Raporu", f"Toplam Soru Sayısı: {toplam_soru_sayisi}\nDoğru Cevap Sayısı: {dogru_cevap_sayisi}\nBaşarı Yüzdesi: {basari_yuzdesi:.2f}%")

    baglanti.commit()
    baglanti.close()

