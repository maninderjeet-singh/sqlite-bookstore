Here’s a **README.md** draft tailored for your project **sqlite-bookstore** 👇

---

# 📚 sqlite-bookstore

A simple **command-line bookstore management system** built with **Python** and **SQLite**.
You can add authors, manage their books, and perform CRUD operations via a text-based menu.

⚠️ **Note:** This project is currently under active development. Features and structure may change.

---

## 🚀 Features

* Manage **Authors**

  * Add, update, view, and delete authors
  * Unique email & phone validation

* Manage **Books**

  * Add, update, view, and delete books
  * Link books to specific authors
  * Store price & publish date

* SQLite Database (auto-created)

* Input validation & interactive CLI

* Rich output formatting using [rich](https://github.com/Textualize/rich)


---

## ⚙️ Installation

1. Clone this repo:

   ```bash
   git clone https://github.com/<your-username>/sqlite-bookstore.git
   cd sqlite-bookstore
   ```

2. Create virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install rich
   ```

---

## ▶️ Usage

Run the app:

```bash
python main.py
```

You’ll see a menu like this:

```
1. Add Author
2. List Authors
3. Update Author
4. Delete Author
5. Add Book
6. List Books
7. Update Book
8. Delete Book
9. Exit
```

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **SQLite3** (lightweight database)
* **Rich** (for colored CLI output)

---

## 📌 Roadmap

* [ ] Better input validation (price, dates)
* [ ] Pagination for long lists
* [ ] Export data to CSV/JSON
* [ ] Modularize into packages (`author`, `book`, `db`)
* [ ] Unit tests

---
