from utils import customtkinter, sqlite3,tkinter
from tkinter import messagebox
import exam_module


def app():
    app = customtkinter.CTk()
    app.title("Word ")
    app.geometry("480x600")
    app.configure(bg="#333333")
    app.resizable(False, False)

    playframe = customtkinter.CTkFrame(master=app, width=210, height=140, border_width=1, corner_radius=15)
    playframe.place(relx=0.3, rely=0.20)

    addframe = customtkinter.CTkFrame(master=app, width=210, height=140,border_width=1, corner_radius=15)
    addframe.place(relx=0.3, rely=0.35)

    settingframe = customtkinter.CTkFrame(master=app, width=140, height=100, border_width=1,corner_radius=15)
    settingframe.place(relx=0.3, rely=0.5)

    reportframe = customtkinter.CTkFrame(master=app, width=210, height=140, border_width=1, corner_radius=15)
    reportframe.place(relx=0.3, rely=0.65)

    playButton = customtkinter.CTkButton(master=playframe, text="PLAY", command=play)
    playButton.grid(row=0, column=0, padx=20, pady=20)

    addingButton = customtkinter.CTkButton(master=addframe, text="Add Word",command=addWord)
    addingButton.grid(row=0, column=0, padx=20, pady=20)

    settingsButton = customtkinter.CTkButton(master=settingframe, text="Settings",command=settings)
    settingsButton.grid(row=0, column=0,padx=20, pady=20)

    reportButton = customtkinter.CTkButton(master=reportframe, text="Take a Report", command=report)
    reportButton.grid(row=0, column=0, padx=20, pady=20)



    app.mainloop()

def addWord():
    global kelime
    global word
    addscreen = customtkinter.CTk()
    addscreen.title("Please Enter Your Words")
    addscreen.geometry("320x150")
    addscreen.configure(bg="#006400")
    addscreen.resizable(False, False)

    wordTurkish = customtkinter.CTkEntry(master=addscreen, width=130, placeholder_text="Turkish")
    wordTurkish.place(x=20, y=80)
    wordEnglish = customtkinter.CTkEntry(master=addscreen, width=130, placeholder_text="English")
    wordEnglish.place(x=180, y=80)

    submitButton = customtkinter.CTkButton(master=addscreen, text="Submit", command=lambda: submit(wordTurkish, wordEnglish))
    submitButton.place(relx=0.5, rely=0.28, anchor=tkinter.CENTER)

    addscreen.mainloop()
def submit(wordTurkish, wordEnglish):

    try:
        conn = sqlite3.connect("words.db")
        cursor = conn.cursor()

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS words(
                    turkish TEXT,
                    english TEXT )""")

        kelime = wordTurkish.get()
        word = wordEnglish.get()

        if kelime != "" and word != "":
            cursor.execute("SELECT turkish FROM words WHERE turkish=?", [kelime])
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "This word-duo already exists.")
            else:
                cursor.execute("INSERT INTO words VALUES (?,?)", [word, kelime])
                conn.commit()
                messagebox.showinfo("", "Successfully added")
                conn.close()
    except sqlite3.Error as error:
        print("Veritabanı hatası:", error)
        messagebox.showerror("Veritabanı Hatası", "Kelime eklenirken bir hata oluştu.")


def play():
    exam_module.exam()
def report():
    exam_module.rapor()
def settings():
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()


    ayarlar_penceresi = customtkinter.CTk()
    ayarlar_penceresi.title("Ayarlar")
    global yeni_kelime_sayisi_giris


    yeni_kelime_sayisi_etiket = customtkinter.CTkLabel(ayarlar_penceresi, text="Yeni kelime çıkma sayısı:")
    yeni_kelime_sayisi_etiket.pack(pady=10)

    yeni_kelime_sayisi_giris = customtkinter.CTkEntry(ayarlar_penceresi, font=("Arial", 16))
    yeni_kelime_sayisi_giris.pack()

    kaydet_dugmesi = customtkinter.CTkButton(ayarlar_penceresi, text="Ayarları Kaydet", command=ayarlari_kaydet)
    kaydet_dugmesi.pack(pady=10)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS ayarlar (
                anahtar TEXT PRIMARY KEY,
                deger TEXT
            )
        """)

    cursor.execute("""
            INSERT OR IGNORE INTO ayarlar (anahtar, deger) VALUES (?, ?)
        """, ("kelime_sayisi", "10"))
    conn.commit()
    conn.close()

    ayarlar_penceresi.mainloop()


def ayarlari_kaydet():
    try:
        yeni_kelime_sayisi = yeni_kelime_sayisi_giris.get()
        conn = sqlite3.connect("words.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE ayarlar SET deger = ? WHERE anahtar = 'kelime_sayisi'", (yeni_kelime_sayisi,))
        conn.commit()
        messagebox.showinfo("Succesful", "Settings has changed")
        conn.close()
    except sqlite3.Error as error:
        print("Veritabanı hatası:", error)
        messagebox.showerror("Veritabanı Hatası", "Ayarlar kaydedilirken bir hata oluştu.")



    















