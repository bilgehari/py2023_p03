import os
import tkinter as tk
from xml.etree import ElementTree as ET
from PIL import Image, ImageTk


class BookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bilge'nin Arşivi")

        # Kitap verilerini saklamak için bir liste
        self.books = self.parse_xml("veriSeti.xml")
        self.current_book_index = 0  # Şu anki kitap indeksi

        # İleri ve geri butonları
        self.prev_button = tk.Button(root, text="Önceki Kitap", command=self.show_prev_book)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(root, text="Sonraki Kitap", command=self.show_next_book)
        self.next_button.pack(side=tk.RIGHT, padx=5)
        # Kitap listesi butonu
        self.book_list_button = tk.Button(root, text="Kitap Listesi", command=self.show_book_list)
        self.book_list_button.pack(pady=5)


        # Çıkış butonu
        self.exit_button = tk.Button(root, text="Çıkış", command=root.destroy)
        self.exit_button.pack(pady=5)


    def parse_xml(self, file_path):
        books = []
        tree = ET.parse(file_path)
        root = tree.getroot()
        for book_elem in root.findall("eser"):
            book = {}
            for child_elem in book_elem:
                if child_elem.tag == "dcImage":
                    image_filename = f"{book_elem.find('dcTitle').text.lower().replace(' ', '_')}.jpg"
                    book[child_elem.tag] = os.path.join("image", image_filename)
                else:
                    book[child_elem.tag] = child_elem.text
            books.append(book)
        return books

    def show_details(self):
        selected_book = self.books[self.current_book_index]

        # Detay penceresi
        detail_window = tk.Toplevel(self.root)
        detail_window.title(selected_book["dcTitle"])

        # Kitap detayları
        detail_label = tk.Label(detail_window, text=f"{selected_book['dcTitle']} - {selected_book['dcCreator']}")
        detail_label.pack(pady=10)

        # Kitap açıklaması
        description_label = tk.Label(detail_window, text=selected_book['dcDescription'], wraplength=400,
                                     justify="left")
        description_label.pack(pady=10)

        # Diğer bilgiler
        subject_label = tk.Label(detail_window, text=f"Subject: {selected_book['dcSubject']}")
        subject_label.pack(pady=5)

        creator_label = tk.Label(detail_window, text=f"Creator: {selected_book['dcCreator']}")
        creator_label.pack(pady=5)

        contributor_label = tk.Label(detail_window, text=f"Contributor: {selected_book['dcContributor']}")
        contributor_label.pack(pady=5)

        language_label = tk.Label(detail_window, text=f"Language: {selected_book['dcLanguage']}")
        language_label.pack(pady=5)

        identifier_label = tk.Label(detail_window, text=f"Identifier: {selected_book['dcIdentifier']}")
        identifier_label.pack(pady=5)

        # Kitap görseli
        image_path = selected_book['dcImage']
        image_file = Image.open(image_path)
        image_resized = image_file.resize((150, 200))
        image_tk = ImageTk.PhotoImage(image_resized)

        image_label = tk.Label(detail_window, image=image_tk)
        image_label.image = image_tk  # Referansı tutmak önemlidir
        image_label.pack(pady=10)

    def show_prev_book(self):
        if self.current_book_index > 0:
            self.current_book_index -= 1
            self.show_details()  # Yeni kitabın detaylarını göster

    def show_next_book(self):
        if self.current_book_index < len(self.books) - 1:
            self.current_book_index += 1
            self.show_details()  # Yeni kitabın detaylarını göster

    def show_book_list(self):
        # Kitap listesi penceresi
        book_list_window = tk.Toplevel(self.root)
        book_list_window.title("Kitap Listesi")

        # Kitap listesi
        listbox = tk.Listbox(book_list_window)
        for book in self.books:
            listbox.insert(tk.END, book["dcTitle"])
        listbox.pack(pady=10)


# Ana uygulama penceresini oluştur
root = tk.Tk()
app = BookApp(root)
root.mainloop()
