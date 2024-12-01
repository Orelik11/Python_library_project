import unittest
import os
import json
from library import Library, Book

class TestLibrary(unittest.TestCase):
    TEST_DATA_FILE = 'test_library.json'

    def setUp(self):
        # Инициализация библиотеки с тестовым файлом
        self.library = Library(data_file=self.TEST_DATA_FILE)
        # Очистка тестовых данных
        self.library.books = []
        self.library.save_books()

    def tearDown(self):
        # Удаление тестового файла после тестов
        if os.path.exists(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)

    def test_add_book(self):
        self.library.add_book("Test Title", "Test Author", 2020)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Title")

    def test_delete_book(self):
        self.library.add_book("Test Title", "Test Author", 2020)
        book_id = self.library.books[0].id
        self.library.delete_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_delete_nonexistent_book(self):
        with self.assertLogs() as log:
            self.library.delete_book("nonexistent-id")
            self.assertIn("Ошибка: Книга с ID nonexistent-id не найдена.", log.output[0])

    def test_search_books_by_title(self):
        self.library.add_book("Python Programming", "Author A", 2021)
        results = self.library.search_books(title="Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Programming")

    def test_search_books_by_author(self):
        self.library.add_book("Book One", "Author A", 2021)
        self.library.add_book("Book Two", "Author B", 2022)
        results = self.library.search_books(author="Author B")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Author B")

    def test_search_books_by_year(self):
        self.library.add_book("Book One", "Author A", 2021)
        self.library.add_book("Book Two", "Author B", 2022)
        results = self.library.search_books(year=2022)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2022)

    def test_change_status(self):
        self.library.add_book("Book One", "Author A", 2021)
        book_id = self.library.books[0].id
        self.library.change_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_change_status_invalid(self):
        self.library.add_book("Book One", "Author A", 2021)
        book_id = self.library.books[0].id
        with self.assertLogs() as log:
            self.library.change_status(book_id, "недоступна")
            self.assertIn("Ошибка: Недопустимый статус. Возможные значения: 'в наличии', 'выдана'.", log.output[0])

if __name__ == '__main__':
    unittest.main()
