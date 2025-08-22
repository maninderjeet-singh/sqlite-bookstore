import sqlite3
from rich.console import Console
from rich.table import Table
import datetime

console = Console()


def getDBConnect():
    conn = sqlite3.connect('books_db')
    cursor = conn.cursor()
    cursor.execute(''' 
        create table if not exists authors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name varchar(150),
        email varchar UNIQUE,
        phone varchar(20) UNIQUE,
        created_at text
        )
    ''')
    cursor.execute(''' 
        create table if not exists books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER,
        name varchar(255),
        price REAL,
        publish_at text,
        created_at text
        )
    ''')
    return conn



console.print("=" * 40, style="bold cyan")
console.print("              Author App  ", style="bold yellow")
console.print("=" * 40, style="bold cyan")



def authorCreate():
    fields = {'name': '' ,'email': '','phone': ''}
    console.print("Please fill following details.", style="bold cyan")
    x = datetime.datetime.now()
    now = x.strftime("%Y-%m-%d %H:%M:%S")
    conn = getDBConnect()
    cursor = conn.cursor()
    for field in fields:
        while True:
            inputEntered = console.input(f"[bold cyan] Enter {field}: [/bold cyan] ").strip()
            if (inputEntered != ''):
                match field:
                    case 'email':
                        alreadyExist = cursor.execute('select email from authors where email =?',(inputEntered,)).fetchone()
                        if(alreadyExist):
                            console.print(f"This email is already used {field}", style="bold red")
                            continue
                    case 'phone':
                        alreadyExist = cursor.execute('select phone from authors where phone =?',(inputEntered,)).fetchone()
                        if(alreadyExist):
                            console.print(f"This phone number is already used {field}", style="bold red")
                            continue

                fields[field] = inputEntered
                break
            else:
                console.print(f"Please enter value of {field}", style="bold red")
    cursor.execute('insert into authors (name, email,phone,created_at) values(?,?,?,?)', (fields['name'],fields['email'],fields['phone'],now,))
    conn.commit()
    conn.close()
    console.print("Author detail saved successfully", style="bold green")
    


def displayAuthor(authors):
    table = Table(title="Author List", style="cyan")
    table.add_column("ID", style="bold green")
    table.add_column("Name", style="bold yellow")
    table.add_column("Email", style="bold yellow")
    table.add_column("Phone", style="bold yellow")
    table.add_column("Created at", style="bold yellow")
    for author in authors:
        table.add_row(str(author[0]), author[1],author[2],author[3],author[4])
    console.print(table)
    
def authorList():
    conn = getDBConnect()
    cursor = conn.cursor()
    result = cursor.execute('select * from authors').fetchall()
    conn.close()
    displayAuthor(result)
    
    

def searchAuthorById(id):
    conn = getDBConnect()
    cursor = conn.cursor()
    result = cursor.execute('select * from authors where id = ?',(id,)).fetchall()
    conn.close()
    displayAuthor(result)

def searchAuthorByName(name):
    conn = getDBConnect()
    cursor = conn.cursor()
    result = cursor.execute('select * from authors where name like ?',('%'+name+'%',)).fetchall()
    conn.close()
    displayAuthor(result)


def updateAuthor(id):
    conn = getDBConnect()
    cursor = conn.cursor()
    author = cursor.execute('select * from authors where id = ?',(id,)).fetchone()
    authors = [author]
    displayAuthor(authors)
    choice = console.input("[bold cyan] Are you sure, you want to update that author? (yes/no): [/bold cyan] ").strip()
    if choice != 'yes':
        return
    fields = {'name': '' ,'email': '','phone': ''}
    console.print("Please fill following details.", style="bold cyan")
    x = datetime.datetime.now()
    now = x.strftime("%Y-%m-%d %H:%M:%S")
    fieldIndex = 1
    for field in fields:
        while True:
            # inputEntered = console.input(f"[bold cyan] Enter {field}: [/bold cyan] ").strip()
            inputEntered = console.input(f"[bold cyan] Enter {field} (skip blank if you want keep {author[fieldIndex]}): [/bold cyan] ").strip()
            if (inputEntered != ''):
                match field:
                    case 'email':
                        alreadyExist = cursor.execute('select email from authors where email =? and id!=?',(inputEntered,id)).fetchone()
                        if(alreadyExist):
                            console.print(f"This email is already used {field}", style="bold red")
                            continue
                    case 'phone':
                        alreadyExist = cursor.execute('select phone from authors where phone =? and id!=?',(inputEntered,id)).fetchone()
                        if(alreadyExist):
                            console.print(f"This phone number is already used {field}", style="bold red")
                            continue

                fields[field] = inputEntered
                break
            else:
                fields[field] = author[fieldIndex]
                console.print(f"value of {field} is keep to {author[fieldIndex]}", style="bold yellow")
                break
        fieldIndex = fieldIndex+1
    # cursor.execute('insert into authors (name, email,phone,created_at) values(?,?,?,?)', (fields['name'],fields['email'],fields['phone'],now,))
    # cursor.execute(f'update authors set name = "{fields['name']}", email="{fields['email']}",phone="{fields['phone']}" where id=?',(id,))
    cursor.execute('update authors set name = ?, email=?,phone=? where id=?',(fields['name'],fields['email'],fields['phone'],id,))
    conn.commit()
    conn.close()
    console.print("Author detail saved successfully", style="bold green")

def deleteAuthor(id):
    with getDBConnect() as conn:
        cursor = conn.cursor()
        author = cursor.execute('SELECT * FROM authors WHERE id=?', (id,)).fetchone()
        if not author:
            console.print("[red]Author not found[/red]")
            return
        displayAuthor([author])
        choice = console.input("[cyan]Are you sure you want to delete this author? (yes/no): [/cyan]").strip()
        if choice == 'yes':
            cursor.execute("DELETE FROM authors WHERE id=?", (id,))
            conn.commit()
            console.print("[green]Author deleted successfully[/green]")


def createBook():
    fields = {'author_id':'','name': '' ,'price': '','publish_at': ''}
    console.print("Please fill following details.", style="bold cyan")
    x = datetime.datetime.now()
    now = x.strftime("%Y-%m-%d %H:%M:%S")
    conn = getDBConnect()
    cursor = conn.cursor()
    for field in fields:
        while True:
            inputEntered = console.input(f"[bold cyan] Enter {field}: [/bold cyan] ").strip()
            if (inputEntered != ''):
                fields[field] = inputEntered
                break
            else:
                console.print(f"Please enter value of {field}", style="bold red")
    cursor.execute('insert into books (author_id, name,price,publish_at,created_at) values(?,?,?,?,?)', (fields['author_id'],fields['name'],fields['price'],fields['publish_at'],now,))
    conn.commit()
    conn.close()
    console.print("Book detail saved successfully", style="bold green")

def displayBooks(books):
    table = Table(title="Book List", style="cyan")
    table.add_column("ID", style="bold green")
    table.add_column("Author ID", style="bold green")
    table.add_column("Author Name", style="bold green")
    table.add_column("Name", style="bold yellow")
    table.add_column("Price", style="bold yellow")
    table.add_column("Publish at", style="bold yellow")
    table.add_column("Created at", style="bold yellow")
    for book in books:
        table.add_row(str(book[0]), str(book[1]),str(book[6]),str(book[2]),str(book[3]),str(book[4]),str(book[5]))
    console.print(table)

def bookList(id=''):
    conn = getDBConnect()
    cursor = conn.cursor()
    statement = 'select books.*, authors.name from books join authors on authors.id = books.author_id'
    if(id == ''):
        result = cursor.execute(statement).fetchall()
    else:
        result = cursor.execute(statement+' where author_id=?',(id,)).fetchall()

    conn.close()
    if len(result):
        displayBooks(result)
    else:
        console.print('No Books added yet',style="bold yellow")


def updateBook(id):
    conn = getDBConnect()
    cursor = conn.cursor()
    statement = 'select books.*, authors.name from books join authors on authors.id = books.author_id'
    book = cursor.execute(statement+' where books.id=?',(id,)).fetchone()
    books = [book]
    displayBooks(books)
    choice = console.input("[bold cyan] Are you sure, you want to update that book? (yes/no): [/bold cyan] ").strip()
    if choice != 'yes':
        return
    fields = {'author_id':'','name': '' ,'price': '','publish_at': ''}
    console.print("Please fill following details.", style="bold cyan")
    x = datetime.datetime.now()
    now = x.strftime("%Y-%m-%d %H:%M:%S")
    fieldIndex = 1
    for field in fields:
        inputEntered = console.input(f"[bold cyan] Enter {field} (skip blank if you want keep {book[fieldIndex]}): [/bold cyan] ").strip()
        if (inputEntered != ''):
            fields[field] = inputEntered
        else:
            fields[field] = book[fieldIndex]
            console.print(f"value of {field} is keep to {book[fieldIndex]}", style="bold yellow")
        fieldIndex = fieldIndex+1
    # cursor.execute(f'update books set author_id = "{fields['author_id'] }" , name = "{fields['name']}",price={fields['price']},publish_at="{fields['publish_at']}" where id = ?',(id))
    cursor.execute('update books set author_id = ? , name = ?,price=?,publish_at=? where id = ?',(fields['author_id'],fields['name'],fields['price'],fields['publish_at'],id))
    conn.commit()
    conn.close()
    console.print("Book detail update successfully", style="bold green")

def deleteBook(id):
    conn = getDBConnect()
    cursor = conn.cursor()
    statement = 'select books.*, authors.name from books join authors on authors.id = books.author_id'
    book = cursor.execute(statement+' where books.id=?',(id,)).fetchone()
    books = [book]
    displayBooks(books)
    choice = console.input("[bold cyan] Are you sure, you want to delete that book? (yes/no): [/bold cyan] ").strip()
    if choice != 'yes':
        return
    cursor.execute(f'delete from books where id = ?',(id))
    conn.commit()
    conn.close()
    console.print("Book detail deleted successfully", style="bold green")

actions = [
    {
        'id':1,
        'name' : 'list of authors'
    },
    {
        'id':2,
        'name' : 'Create a new author'
    },
    {
        'id':3,
        'name' : 'Search author by name'
    },
    {
        'id':4,
        'name' : 'Search author by Id'
    },
    {
        'id':5,
        'name' : 'Update author'
    },
    {
        'id':6,
        'name' : 'Delete author'
    },
    {
        'id':7,
        'name' : 'list of books'
    },
    {
        'id':8,
        'name' : 'list of books of specific author'
    },
    {
        'id':9,
        'name' : 'Create a new book'
    },
    {
        'id':10,
        'name' : 'Update book'
    },
    {
        'id':11,
        'name' : 'Delete book'
    },
    {
        'id':0,
        'name' : 'Exit'
    },
]

again = True
while again:
    console.print("Which operation you want to perform", style="bold cyan")
    for action in actions:
        console.print(f"{action['id']}: {action['name']}", style="bold yellow")

    while True:
        choice = console.input("[bold cyan] Enter your choice: [/bold cyan] ").strip()
        if choice.isnumeric() != True:
            console.print(f"You choosed invalid option num", style="bold red")
            continue
        choice = int(choice)
        actionIds = [action['id'] for action in actions]
        if choice in actionIds:
            if choice == 0:
                again = False
            break
        else:
            console.print(f"You choosed invalid option", style="bold red")


    console.print(f"You choosed {choice}", style="bold cyan")

    match choice:
        case 1:
            console.print("list of authors", style="bold cyan")
            authorList()
        case 2:
            console.print("Create a new author", style="bold cyan")
            authorCreate()
        case 3:
            console.print("Search author by name", style="bold cyan")
            name = console.input("[bold cyan] Enter author name: [/bold cyan] ").strip()
            searchAuthorByName(name)
        case 4:
            console.print("Search author by Id", style="bold cyan")
            id = console.input("[bold cyan] Enter author ID: [/bold cyan] ").strip()
            searchAuthorById(id)
        case 5:
            console.print("Update author", style="bold cyan")
            id = console.input("[bold cyan] Enter author ID: [/bold cyan] ").strip()
            updateAuthor(id)
        case 6:
            console.print("Delete author", style="bold cyan")
            id = console.input("[bold cyan] Enter author ID: [/bold cyan] ").strip()
            deleteAuthor(id)

        case 7:
            console.print("list of books", style="bold cyan")
            bookList()
        case 8:
            console.print("list of books of specific author", style="bold cyan")
            id = console.input("[bold cyan] Enter author id: [/bold cyan] ").strip()
            bookList(id=id)
        case 9:
            console.print("Create a new book", style="bold cyan")
            createBook()
        case 10:
            console.print("Update book", style="bold cyan")
            id = console.input("[bold cyan] Enter book id: [/bold cyan] ").strip()
            updateBook(id)
        case 11:
            console.print("Delete book", style="bold cyan")
            id = console.input("[bold cyan] Enter book id: [/bold cyan] ").strip()
            deleteBook(id)
    
    choice = console.input("[bold cyan] Do you want to perform another operation? (yes/no): [/bold cyan] ").strip()
    if choice != 'yes':
        again = False

