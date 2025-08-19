# 📚 SQLite Bookstore

🚧 **Development in Progress** 🚧  

A simple Python CLI tool to manage **authors** and their **books** using **SQLite**.  
You can add authors, insert books for each author, and fetch lists of authors and books easily.  

---

## 🚀 Features (Planned & Implemented)
- [x] Add new authors with name, email, and phone  
- [x] View list of authors  
- [x] View all books  
- [ ] View books by a specific author  
- [ ] Insert books linked to specific authors  
- [ ] Improve error handling and input validation  
- [ ] Add unit tests  

---

## 📦 Requirements
- Python 3.8+  
- [rich](https://pypi.org/project/rich/) (for styled console output)  

Install dependencies:
```bash
pip install rich
````

---

## ⚡ Usage

1. Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/sqlite-bookstore.git
cd sqlite-bookstore
```

2. Run the script:

```bash
python main.py
```

---

## 🛠 Database Schema

**authors**

* id (PK)
* name
* email
* phone
* created\_at

**books**

* id (PK)
* title
* author\_id (FK → authors.id)
* created\_at

---

## 📝 Notes

This project is still under development. Features will be added gradually.
Feel free to suggest ideas or improvements via Issues or Pull Requests.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📄 License

This project is licensed under the MIT License.


