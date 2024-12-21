import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import subprocess
import os

class LibraryInterface:
    def __init__(self):
        self.visitors = []

        self.window = tk.Tk()
        self.window.title("Марущак")
        self.window.geometry("800x600")

        # Завантаження фонового зображення
        image = Image.open("lr8.jpg")
        resized_image = image.resize((800, 600), Image.LANCZOS)
        background_image = ImageTk.PhotoImage(resized_image)

        # Створення об'єкту Label та встановлення фонового зображення
        image_label = ttk.Label(self.window, image=background_image)
        image_label.image = background_image  # Збереження посилання
        image_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ttk.Label(
            self.main_frame,
            text="Базова інформація про відвідувачів",
            font=("Times New Roman", 14, "bold"),
            foreground="blue"
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Таблиця для відображення даних
        self.table = ttk.Treeview(self.main_frame, columns=("PIBReduction", "Address", "Gender", "Age"))
        self.table.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="nsew")

        # Налаштування заголовків колонок
        self.table.heading("#0", text="№")
        self.table.column("#0", width=30, anchor="center")
        self.table.heading("PIBReduction", text="ПІБ")
        self.table.column("PIBReduction", width=150)
        self.table.heading("Address", text="Адреса")
        self.table.column("Address", width=200)
        self.table.heading("Gender", text="Стать")
        self.table.column("Gender", width=70, anchor="center")
        self.table.heading("Age", text="Вік")
        self.table.column("Age", width=50, anchor="center")

        # Labels для статистики
        self.average_age_label = ttk.Label(
            self.main_frame, text="Середній вік відвідувачів:", font=("Times New Roman", 11), foreground="green"
        )
        self.average_age_label.grid(row=2, column=0, pady=(5, 5), sticky="w")

        self.oldest_person_label = ttk.Label(
            self.main_frame, text="Найстарший відвідувач:", font=("Times New Roman", 11), foreground="red"
        )
        self.oldest_person_label.grid(row=3, column=0, pady=(5, 5), sticky="w")

        self.youngest_person_label = ttk.Label(
            self.main_frame, text="Наймолодший відвідувач:", font=("Times New Roman", 11), foreground="blue"
        )
        self.youngest_person_label.grid(row=4, column=0, pady=(5, 5), sticky="w")

        # Форма для додавання відвідувачів
        self.add_visitor_frame = ttk.Frame(self.main_frame, padding="10")
        self.add_visitor_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="w")

        # Поля вводу
        self.fio_label = ttk.Label(self.add_visitor_frame, text="ПІБ:")
        self.fio_label.grid(row=0, column=0, padx=(0, 10))
        self.fio_entry = ttk.Entry(self.add_visitor_frame, width=30)
        self.fio_entry.grid(row=0, column=1)

        self.address_label = ttk.Label(self.add_visitor_frame, text="Адреса:")
        self.address_label.grid(row=1, column=0, padx=(0, 10))
        self.address_entry = ttk.Entry(self.add_visitor_frame, width=30)
        self.address_entry.grid(row=1, column=1)

        self.year_label = ttk.Label(self.add_visitor_frame, text="Рік народження:")
        self.year_label.grid(row=2, column=0, padx=(0, 10))
        self.year_entry = ttk.Entry(self.add_visitor_frame, width=10)
        self.year_entry.grid(row=2, column=1)

        # Кнопки
        self.add_visitor_button = ttk.Button(
            self.add_visitor_frame, text="Додати відвідувача", command=self.add_visitor
        )
        self.add_visitor_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.show_data_button = ttk.Button(
            self.main_frame, text="Показати дані", command=self.show_data
        )
        self.show_data_button.grid(row=6, column=0, columnspan=2, pady=(10, 0), sticky="w")

        self.window.mainloop()  # Запуск головного циклу подій інтерфейсу

    def add_visitor(self):
        fio = self.fio_entry.get()
        address = self.address_entry.get()
        year = int(self.year_entry.get())

        visitor = Visitor(fio, address, year)
        self.visitors.append(visitor)

        self.fio_entry.delete(0, "end")
        self.address_entry.delete(0, "end")
        self.year_entry.delete(0, "end")

    def show_data(self):
        self.clear_table()

        # Запис відвідувачів у input.txt
        with open("input.txt", "w", encoding="UTF-8") as BD:
            for i, visitor in enumerate(self.visitors, start=1):
                age = 2024 - visitor.GetYear()
                gender = "Жін." if visitor.IsFemale() else "Чол."

                self.table.insert(
                    "", "end", text=str(i),
                    values=(visitor.GetPIBReduction(), visitor.address, gender, age)
                )
                BD.write(f"{visitor.fio};{visitor.address};{visitor.year};\n")

        try:
            subprocess.run(["Source.exe"], check=True)
        except FileNotFoundError:
            print("Не знайдено myprogram. Переконайтеся, що C++ програма скомпільована та розташована поруч.")
            return
        except subprocess.CalledProcessError:
            print("Помилка при виконанні C++ програми.")
            return

        # Зчитуємо output.txt та оновлюємо 
        if os.path.exists("output.txt"):
            with open("output.txt", "r", encoding="utf-8") as out:
                lines = out.read().strip().split('\n')
                
            # Очікується 3 рядки з С++
            if len(lines) >= 3:
                self.average_age_label.configure(text=lines[0])
                self.oldest_person_label.configure(text=lines[1])
                self.youngest_person_label.configure(text=lines[2])
        else:
            print("output.txt не знайдено.")

    def clear_table(self):
        for item in self.table.get_children():
            self.table.delete(item)


class Visitor:
    def __init__(self, fio, address, year):
        self.fio = fio
        self.address = address
        self.year = year

    def GetYear(self):
        return self.year

    def GetPIBReduction(self):
        name_parts = self.fio.split()
        last_name = name_parts[0]
        initials = '.'.join([name[0] for name in name_parts[1:]])
        return f"{last_name} {initials}"

    def IsFemale(self):
        return self.fio[-1] in ['а', 'я']


if __name__ == "__main__":
    LibraryInterface()
