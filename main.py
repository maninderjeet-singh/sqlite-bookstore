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

actions = [
    {
        'id':1,
        'name' : 'list of authors'
    },
    {
        'id':2,
        'name' : 'list of books'
    },
    {
        'id':3,
        'name' : 'list of books of specific author'
    },
    {
        'id':4,
        'name' : 'Create a new author'
    },
]

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
    console.print("Author detail saved successfully", style="bold green")
    


    
def authorList():
    conn = getDBConnect()
    cursor = conn.cursor()
    result = cursor.execute('select * from authors').fetchall()    
    table = Table(title="Author List", style="cyan")
    table.add_column("ID", style="bold green")
    table.add_column("Name", style="bold yellow")
    table.add_column("Email", style="bold yellow")
    table.add_column("Phone", style="bold yellow")
    table.add_column("Created at", style="bold yellow")
    for author in result:
        table.add_row(str(author[0]), author[1],author[2],author[3],author[4])
    console.print(table)


def bookList(id=''):
    conn = getDBConnect()
    cursor = conn.cursor()
    statement = 'select books.*, authors.name from books join authors on authors.id = books.author_id'
    if(id == ''):
        result = cursor.execute(statement).fetchall()
    else:
        result = cursor.execute(statement+' where author_id=?',(id,)).fetchall()

    if len(result):
        table = Table(title="Book List", style="cyan")
        table.add_column("ID", style="bold green")
        table.add_column("Author ID", style="bold green")
        table.add_column("Author Name", style="bold green")
        table.add_column("Name", style="bold yellow")
        table.add_column("Price", style="bold yellow")
        table.add_column("Publish at", style="bold yellow")
        table.add_column("Created at", style="bold yellow")
        for book in result:
            table.add_row(str(book[0]), str(book[1]),str(book[6]),str(book[2]),str(book[3]),str(book[4]),str(book[5]))
        console.print(table)
    else:
        console.print('No Books added yet',style="bold yellow")


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
        break
    else:
        console.print(f"You choosed invalid option", style="bold red")


console.print(f"You choosed {choice}", style="bold cyan")

match choice:
    case 1:
        console.print("list of authors", style="bold cyan")
        authorList()
    case 2:
        console.print("list of books", style="bold cyan")
        bookList()
    case 3:
        console.print("list of books of specific author", style="bold cyan")
        id = console.input("[bold cyan] Enter author id: [/bold cyan] ").strip()
        bookList(id=id)
    case 4:
        console.print("Create a new author", style="bold cyan")
        authorCreate()

