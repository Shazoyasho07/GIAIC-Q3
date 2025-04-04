import json
import os

data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []   

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

def add_book(library):
    title = input('Enter the title of the book: ')
    author = input('Enter the author of the book: ')
    year = input('Enter the year of the book: ')
    genre = input('Enter the genre of the book: ')
    read = input('Have you read the book? (yes/no): ').lower() == 'yes'

    new_book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read' : read
    }

    library.append(new_book)
    save_library(library)
    print(f'Book {title} added successfully.')

def remove_book(library):
    title = input("Enter the title of the book to remove from the library: ").strip().lower()

    for i, book in enumerate(library):
        if book['title'].strip().lower() == title:
            del library[i]  # Directly delete the book from the original list
            save_library(library)  # Save updated list
            print(f'Book "{book["title"]}" removed successfully.')  # Show correct case
            return  # Exit the function after removing the book

    print(f'Book "{title}" not found in the library.')
 
def search_library(library):
    search_by = input("Search by title or year: ").strip().lower()  # Strip spaces
    if search_by not in ["title", "year"]:
        print("Invalid search field. Please enter 'title' or 'year'.")
        return  # Exit function if input is invalid

    search_term = input(f"Enter the {search_by}: ").strip().lower()

    results = [book for book in library if search_term in book[search_by].strip().lower()]

    if results:
        for book in results:
            status = "Read" if book['read'] else "Unread"
            print(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
    else:
        print(f"No books found matching '{search_term}' in the {search_by} field.")
        
def display_all_books(library):
    if library:
        for book in library:
            status = "Read" if book['read'] else "Unread"
            print(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
    else:
        print("The library is empty.")

def display_statistics(library):
    total_books = len(library)
    read_books = len([book for book in library if book['read']])
    percentage_read =  (read_books / total_books) * 100 if total_books > 0 else 0

    print(f"Total books: {total_books}")
    print(f"Percentage read : {percentage_read:.2f}%")

def main():
    library = load_library()
    while True:
        print("Welcome to your Personal Library Manager!  ")
        print("Menu")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search the library")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_library(library)
        elif choice == '4':
            display_all_books(library)
        elif choice == '5':
            display_statistics(library)
        elif choice == '6':
            print("Goodbye! Have a nice Day")
            break
        else :
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
