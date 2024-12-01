import json
import os
import uuid
from typing import List, Dict, Any

# Путь к файлу хранения данных
DATA_FILE = 'library.json'

class Book:
    """
    Класс, представляющий книгу в библиотеке.
    """
    def __init__(self, title: str, author: str, year: int, status: str = "в наличии", book_id: str = None):
        self.id = book_id or str(uuid.uuid4())
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует объект книги в словарь.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Book':
        """
        Создает объект книги из словаря.
        """
        return Book(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            status=data['status'],
            book_id=data['id']
        )

class Library:
    """
    Класс для управления библиотекой.
    """
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """
        Загружает книги из файла.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    self.books = [Book.from_dict(book) for book in data]
                except json.JSONDecodeError:
                    self.books = []
        else:
            self.books = []

    def save_books(self):
        """
        Сохраняет книги в файл.
        """
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.
        """
        new_book = Book(title=title, author=author, year=year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID: {new_book.id}")

    def delete_book(self, book_id: str):
        """
        Удаляет книгу по ID.
        """
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Ошибка: Книга с ID {book_id} не найдена.")

    def search_books(self, **kwargs):
        """
        Ищет книги по заданным параметрам.
        """
        results = self.books
        for key, value in kwargs.items():
            if key in ['title', 'author']:
                results = [book for book in results if value.lower() in getattr(book, key).lower()]
            elif key == 'year':
                results = [book for book in results if getattr(book, key) == value]
        return results

    def display_books(self, books: List[Book] = None):
        """
        Отображает список книг.
        """
        if books is None:
            books = self.books
        if not books:
            print("Библиотека пуста.")
            return
        print(f"{'ID':36} | {'Название':30} | {'Автор':20} | {'Год':4} | {'Статус':10}")
        print("-" * 110)
        for book in books:
            print(f"{book.id} | {book.title[:30]:30} | {book.author[:20]:20} | {book.year:4} | {book.status:10}")

    def change_status(self, book_id: str, new_status: str):
        """
        Изменяет статус книги по ID.
        """
        if new_status not in ["в наличии", "выдана"]:
            print("Ошибка: Недопустимый статус. Возможные значения: 'в наличии', 'выдана'.")
            return
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
                return
        print(f"Ошибка: Книга с ID {book_id} не найдена.")

def main():
    library = Library()

    while True:
        print("\n--- Система Управления Библиотекой ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие (1-6): ")

        if choice == '1':
            title = input("Введите название книги: ").strip()
            author = input("Введите автора книги: ").strip()
            try:
                year = int(input("Введите год издания: ").strip())
                library.add_book(title, author, year)
            except ValueError:
                print("Ошибка: Год издания должен быть числом.")
        elif choice == '2':
            book_id = input("Введите ID книги для удаления: ").strip()
            library.delete_book(book_id)
        elif choice == '3':
            print("Поиск по: 1. Названию 2. Автору 3. Году издания")
            search_choice = input("Выберите критерий поиска (1-3): ").strip()
            if search_choice == '1':
                title = input("Введите название для поиска: ").strip()
                results = library.search_books(title=title)
                library.display_books(results)
            elif search_choice == '2':
                author = input("Введите автора для поиска: ").strip()
                results = library.search_books(author=author)
                library.display_books(results)
            elif search_choice == '3':
                try:
                    year = int(input("Введите год издания для поиска: ").strip())
                    results = library.search_books(year=year)
                    library.display_books(results)
                except ValueError:
                    print("Ошибка: Год издания должен быть числом.")
            else:
                print("Ошибка: Недопустимый выбор.")
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            book_id = input("Введите ID книги для изменения статуса: ").strip()
            print("Новый статус: 1. В наличии 2. Выдана")
            status_choice = input("Выберите новый статус (1-2): ").strip()
            if status_choice == '1':
                new_status = "в наличии"
            elif status_choice == '2':
                new_status = "выдана"
            else:
                print("Ошибка: Недопустимый выбор статуса.")
                continue
            library.change_status(book_id, new_status)
        elif choice == '6':
            print("Выход из системы. До свидания!")
            break
        else:
            print("Ошибка: Недопустимый выбор. Пожалуйста, выберите от 1 до 6.")

if __name__ == "__main__":
    main()
