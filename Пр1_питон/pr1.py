import os

class User:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

class Librarian(User):
    def __init__(self, name):
        super().__init__(name)

class Client(User):
    def __init__(self, name):
        super().__init__(name)
        self.my_books = []

class Book:
    def __init__(self, title, author, status):
        self.title = title
        self.author = author
        self.status = status

class Library:
    def __init__(self):
        self.books = []
        self.clients = []
        self.librarians = ["admin"]
        self.load_data()

    def load_data(self):
        if os.path.exists("books.txt"):
            with open("books.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split("|")
                        if len(parts) == 3:
                            b = Book(parts[0], parts[1], parts[2])
                            self.books.append(b)

        if os.path.exists("users.txt"):
            with open("users.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split("|")
                        name = parts[0]
                        client = Client(name)
                        if len(parts) > 1:
                            client.my_books = parts[1:]
                        self.clients.append(client)

        if os.path.exists("librarians.txt"):
            with open("librarians.txt", "r", encoding="utf-8") as f:
                self.librarians = [line.strip() for line in f if line.strip()]

    def save_data(self):
        with open("books.txt", "w", encoding="utf-8") as f:
            for b in self.books:
                f.write(f"{b.title}|{b.author}|{b.status}")

        with open("users.txt", "w", encoding="utf-8") as f:
            for c in self.clients:
                line = c.get_name()
                for bk in c.my_books:
                    line += "|" + bk
                f.write(line + "")

        with open("librarians.txt", "w", encoding="utf-8") as f:
            for lib in self.librarians:
                f.write(lib + "")

    def add_book(self, title, author):
        self.books.append(Book(title, author, "доступна"))
        print("Книга добавлена.")

    def remove_book(self, title):
        for b in self.books:
            if b.title.lower() == title.lower():
                self.books.remove(b)
                print("Книга удалена.")
                return
        print("Книга не найдена.")

    def register_client(self, name):
        for c in self.clients:
            if c.get_name().lower() == name.lower():
                print("Такой пользователь уже есть.")
                return
        self.clients.append(Client(name))
        print("Пользователь зарегистрирован.")

    def show_all_clients(self):
        if not self.clients:
            print("Нет пользователей.")
        for c in self.clients:
            print(f" - {c.get_name()}")

    def show_all_books(self):
        if not self.books:
            print("Нет книг.")
        for b in self.books:
            print(f" - {b.title}, {b.author} — {b.status}")

    def show_available_books(self):
        available = [b for b in self.books if b.status == "доступна"]
        if not available:
            print("Доступных книг нет.")
        for b in available:
            print(f" - {b.title}, {b.author}")

    def take_book(self, client, title):
        for b in self.books:
            if b.title.lower() == title.lower() and b.status == "доступна":
                b.status = "выдана"
                client.my_books.append(b.title)
                print("Книга выдана. Не забудь вернуть!")
                return
        print("Книга недоступна или не найдена.")

    def return_book(self, client, title):
        if title in client.my_books:
            for b in self.books:
                if b.title.lower() == title.lower():
                    b.status = "доступна"
                    client.my_books.remove(title)
                    print("Книга возвращена. Спасибо!")
                    return
        print("У тебя нет такой книги.")

    def show_my_books(self, client):
        if not client.my_books:
            print("Ты ещё не взял ни одной книги.")
        for bk in client.my_books:
            print(f" - {bk}")

    def find_client(self, name):
        for c in self.clients:
            if c.get_name().lower() == name.lower():
                return c
        return None

def main():
    lib = Library()

    while True:
        print("Библиотека")
        print("1. Я библиотекарь")
        print("2. Я читатель")
        print("0. Выйти")

        choice = input("Выбери: ")

        if choice == "0":
            lib.save_data()
            print("Данные сохранены. Пока")
            break

        elif choice == "1":
            name = input("Введи имя библиотекаря: ")
            if name not in lib.librarians:
                print("Доступа нет.")
                continue
            while True:
                print("Библиотекарь")
                print("1. Добавить книгу")
                print("2. Удалить книгу")
                print("3. Зарегистрировать читателя")
                print("4. Список читателей")
                print("5. Список всех книг")
                print("0. Назад")
                act = input("Действие: ")
                if act == "0":
                    break
                elif act == "1":
                    t = input("Название: ")
                    a = input("Автор: ")
                    lib.add_book(t, a)
                elif act == "2":
                    t = input("Название: ")
                    lib.remove_book(t)
                elif act == "3":
                    nm = input("Имя читателя: ")
                    lib.register_client(nm)
                elif act == "4":
                    lib.show_all_clients()
                elif act == "5":
                    lib.show_all_books()
                else:
                    print("Не понял")
            lib.save_data()

        elif choice == "2":
            name = input("Введи своё имя: ")
            client = lib.find_client(name)
            if not client:
                print("Ты не зарегистрирован. Обратись к библиотекарю.")
                continue
            while True:
                print(f"Читатель {name}")
                print("1. Какие книги есть?")
                print("2. Взять книгу")
                print("3. Вернуть книгу")
                print("4. Мои книги")
                print("0. Назад")
                act = input("Действие: ")
                if act == "0":
                    break
                elif act == "1":
                    lib.show_available_books()
                elif act == "2":
                    t = input("Название: ")
                    lib.take_book(client, t)
                elif act == "3":
                    t = input("Название: ")
                    lib.return_book(client, t)
                elif act == "4":
                    lib.show_my_books(client)
                else:
                    print("Не понял")
            lib.save_data()

        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()