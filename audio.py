import customtkinter as ctk  # Mengimpor pustaka customtkinter untuk antarmuka GUI
from tkinter import filedialog, messagebox  # Mengimpor modul untuk dialog file dan pesan dari tkinter
from Crypto.Cipher import DES  # Mengimpor cipher DES dari pustaka Crypto
from Crypto.Util.Padding import pad, unpad  # Mengimpor fungsi pad dan unpad untuk manajemen padding
import os  # Mengimpor modul os untuk operasi file
import time  # Mengimpor modul time untuk mengukur waktu

class AudioCryptoApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Audio Encryption & Decryption Tool")  # Mengatur judul jendela
        self.window.geometry("680x540")  # Menentukan ukuran jendela
        self.selected_file = None  # Menyimpan path file yang dipilih

        ctk.set_default_color_theme("blue")  # Mengubah tema warna aplikasi menjadi biru

        # Menyiapkan elemen-elemen UI
        self.init_ui()

    def init_ui(self):
        container = ctk.CTkFrame(self.window)
        container.pack(pady=15, padx=10)  # Penempatan frame

        browse_button = ctk.CTkButton(container, text="Pilih File Audio", command=self.select_file, width=630, height=60)
        browse_button.grid(row=0, column=0, columnspan=3, padx=8, pady=8, sticky='ew')

        self.selected_file_label = ctk.CTkLabel(container, text="File: Belum dipilih")
        self.selected_file_label.grid(row=1, column=0, columnspan=3, padx=8, pady=8)

        action_frame = ctk.CTkFrame(self.window)
        action_frame.pack(pady=15, padx=12)

        key_label = ctk.CTkLabel(action_frame, text="Masukkan NIM (10 digit):")
        key_label.grid(row=0, column=0, padx=8, pady=8)
        self.key_input = ctk.CTkEntry(action_frame)
        self.key_input.grid(row=0, column=1, columnspan=2, padx=8, pady=8, sticky='ew')

        encrypt_btn = ctk.CTkButton(action_frame, text="Enkripsi", command=self.encrypt, width=260)
        encrypt_btn.grid(row=1, column=0, padx=8, pady=8, sticky='ew')

        decrypt_btn = ctk.CTkButton(action_frame, text="Dekripsi", command=self.decrypt, width=260)
        decrypt_btn.grid(row=1, column=1, padx=8, pady=8, sticky='ew')

        reset_btn = ctk.CTkButton(action_frame, text="Reset", command=self.reset, fg_color="#FF6347", hover_color="#FF4500", width=120)
        reset_btn.grid(row=1, column=2, padx=8, pady=8)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.aac")])
        if file_path:
            self.selected_file = file_path
            self.selected_file_label.configure(text=f"File: {os.path.basename(file_path)}")

    def encrypt(self):
        key = self.key_input.get()
        if len(key) != 10 or not key.isdigit():
            messagebox.showerror("Kesalahan", "NIM harus terdiri dari 10 digit!")
            return
        if not self.selected_file:
            messagebox.showerror("Kesalahan", "Silakan pilih file terlebih dahulu!")
            return
        try:
            with open(self.selected_file, 'rb') as file:
                data = file.read()

            start_time = time.time()

            key_padded = key[:8].ljust(8)
            des = DES.new(key_padded.encode('utf-8'), DES.MODE_CBC)
            iv = des.iv
            padded_data = pad(data, DES.block_size)
            encrypted_data = des.encrypt(padded_data)
            combined_data = iv + encrypted_data

            encrypted_file_path = self.selected_file + "_encrypted.mp3"
            with open(encrypted_file_path, 'wb') as enc_file:
                enc_file.write(combined_data)

            duration = time.time() - start_time
            size_in_kb = os.path.getsize(encrypted_file_path) / 1024

            messagebox.showinfo("Berhasil", f"File terenkripsi disimpan sebagai {encrypted_file_path}\nWaktu: {duration:.4f} detik\nUkuran: {size_in_kb:.2f} KB")
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan selama enkripsi: {e}")

    def decrypt(self):
        key = self.key_input.get()
        if len(key) != 10 or not key.isdigit():
            messagebox.showerror("Kesalahan", "NIM harus terdiri dari 10 digit!")
            return
        if not self.selected_file or not self.selected_file.endswith('_encrypted.mp3'):
            messagebox.showerror("Kesalahan", "Silakan pilih file terenkripsi (.mp3)!")
            return
        try:
            with open(self.selected_file, 'rb') as file:
                encrypted_data = file.read()

            start_time = time.time()

            iv = encrypted_data[:DES.block_size]
            cipher_text = encrypted_data[DES.block_size:]
            key_padded = key[:8].ljust(8)
            des = DES.new(key_padded.encode('utf-8'), DES.MODE_CBC, iv)
            decrypted_data = unpad(des.decrypt(cipher_text), DES.block_size)

            decrypted_file_path = self.selected_file.replace('_encrypted.mp3', '.mp3')
            with open(decrypted_file_path, 'wb') as dec_file:
                dec_file.write(decrypted_data)

            duration = time.time() - start_time
            size_in_kb = os.path.getsize(decrypted_file_path) / 1024

            messagebox.showinfo("Berhasil", f"File didekripsi disimpan sebagai {decrypted_file_path}\nWaktu: {duration:.4f} detik\nUkuran: {size_in_kb:.2f} KB")
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Terjadi kesalahan selama dekripsi: {e}")

    def reset(self):
        self.selected_file_label.configure(text="File: Belum dipilih")
        self.selected_file = None
        self.key_input.delete(0, 'end')

if __name__ == "__main__":
    main_window = ctk.CTk()
    app = AudioCryptoApp(main_window)
    main_window.mainloop()
