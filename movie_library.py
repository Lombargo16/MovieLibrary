import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# ------------------ Работа с JSON ------------------
DATA_FILE = "movies.json"

def load_movies():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_movies(movies):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

# ------------------ Основное приложение ------------------
class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x500")

        self.all_movies = load_movies()
        self.current_genre_filter = ""
        self.current_year_filter = ""

        # Поля ввода
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=20)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, padx=5, pady=5)
        self.genre_entry = tk.Entry(input_frame, width=15)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Год выпуска:").grid(row=0, column=4, padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, width=8)
        self.year_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=0, column=6, padx=5, pady=5)
        self.rating_entry = tk.Entry(input_frame, width=5)
        self.rating_entry.grid(row=0, column=7, padx=5, pady=5)

        self.add_btn = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=0, column=8, padx=10, pady=5)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side=tk.LEFT, padx=5)
        self.genre_filter_entry = tk.Entry(filter_frame, width=15)
        self.genre_filter_entry.pack(side=tk.LEFT, padx=5)
        self.genre_filter_entry.bind("<KeyRelease>", self.apply_filters)

        tk.Label(filter_frame, text="Фильтр по году:").pack(side=tk.LEFT, padx=5)
        self.year_filter_entry = tk.Entry(filter_frame, width=8)
        self.year_filter_entry.pack(side=tk.LEFT, padx=5)
        self.year_filter_entry.bind("<KeyRelease>", self.apply_filters)

        self.clear_filter_btn = tk.Button(filter_frame, text="Сбросить фильтры", command=self.clear_filters)
        self.clear_filter_btn.pack(side=tk.LEFT, padx=10)

        # Таблица
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.update_table()

    def validate_movie_data(self, title, genre, year_str, rating_str):
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр не могут быть пустыми")
            return False
        try:
            year = int(year_str)
            if year < 1888 or year > 2100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом (1888-2100)")
            return False
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return False
        return True

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        if not self.validate_movie_data(title, genre, year, rating):
            return

        new_movie = {
            "название": title,
            "жанр": genre,
            "год": int(year),
            "рейтинг": float(rating)
        }
        self.all_movies.append(new_movie)
        save_movies(self.all_movies)
        self.clear_input_fields()
        self.update_table()

    def clear_input_fields(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def apply_filters(self, event=None):
        self.current_genre_filter = self.genre_filter_entry.get().strip().lower()
        self.current_year_filter = self.year_filter_entry.get().strip()
        self.update_table()

    def clear_filters(self):
        self.genre_filter_entry.delete(0, tk.END)
        self.year_filter_entry.delete(0, tk.END)
        self.current_genre_filter = ""
        self.current_year_filter = ""
        self.update_table()

    def update_table(self):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Фильтрация
        filtered = self.all_movies
        if self.current_genre_filter:
            filtered = [m for m in filtered if self.current_genre_filter in m["жанр"].lower()]
        if self.current_year_filter:
            try:
                year_filter_int = int(self.current_year_filter)
                filtered = [m for m in filtered if m["год"] == year_filter_int]
            except ValueError:
                pass  # если введено не число — игнорируем фильтр по году

        # Вывод в таблицу
        for movie in filtered:
            self.tree.insert("", tk.END, values=(
                movie["название"],
                movie["жанр"],
                movie["год"],
                movie["рейтинг"]
            ))

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
