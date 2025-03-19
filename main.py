import streamlit as st
import json
import os

DATA_FILE = "library.json"

def load_library():
    """Load library data from JSON file with error handling."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Return empty list if JSON is corrupted
    return []

def save_library(library):
    """Save library data to JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(library, file, indent=4)

def initialize_library():
    """Initialize session state for the library."""
    if "library" not in st.session_state:
        st.session_state.library = load_library()

def add_book(title, author, year, genre, read):
    """Add a book to the library."""
    new_book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }
    st.session_state.library.append(new_book)
    save_library(st.session_state.library)
    st.success(f"✅ '{title}' added successfully!")

def remove_book(title):
    """Remove a book from the library."""
    original_length = len(st.session_state.library)
    st.session_state.library = [book for book in st.session_state.library if book["title"].lower() != title.lower()]
    if len(st.session_state.library) < original_length:
        save_library(st.session_state.library)
        st.success(f"🗑️ '{title}' removed successfully!")
    else:
        st.warning(f"⚠️ Book '{title}' not found!")

def search_books(query, search_by):
    """Search books by title or author."""
    return [book for book in st.session_state.library if query.lower() in book[search_by].lower()]

def display_statistics():
    """Display statistics of the library."""
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.subheader("📊 Library Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("📚 Total Books", total_books)
    col2.metric("✅ Read Books", read_books)
    col3.metric("❌ Unread Books", unread_books)
    
    st.progress(read_percentage / 100)

# --- UI Design ---
st.title("📚 Personal Library Manager")
initialize_library()

menu = ["📖 Add Book", "🗑️ Remove Book", "🔍 Search Books", "📚 View Library", "📊 Statistics"]
choice = st.sidebar.selectbox("📌 Select an option", menu)

if choice == "📖 Add Book":
    st.subheader("📖 Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Book Title", placeholder="Enter book title...")
        author = st.text_input("Author", placeholder="Enter author name...")
        year = st.number_input("Publication Year", min_value=0, step=1)
        genre = st.text_input("Genre", placeholder="Enter genre...")
        read = st.checkbox("Have you read this book?")
        submit = st.form_submit_button("📥 Add Book")
        if submit and title and author and genre:
            add_book(title, author, year, genre, read)

elif choice == "🗑️ Remove Book":
    st.subheader("🗑️ Remove a Book")
    book_titles = [book["title"] for book in st.session_state.library]
    title_to_remove = st.selectbox("Select a book to remove", book_titles) if book_titles else None
    if title_to_remove and st.button("❌ Remove Book"):
        remove_book(title_to_remove)

elif choice == "🔍 Search Books":
    st.subheader("🔍 Search Books")
    search_by = st.radio("Search by", ("title", "author"))
    query = st.text_input("Enter search term", placeholder="Type here...")
    if query:
        results = search_books(query, search_by)
        if results:
            with st.expander("📋 Search Results"):
                for book in results:
                    st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("⚠️ No matching books found.")

elif choice == "📚 View Library":
    st.subheader("📚 Your Library")
    if st.session_state.library:
        with st.expander("📋 View All Books"):
            for book in st.session_state.library:
                st.write(f"📖 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.info("ℹ️ Your library is empty!")

elif choice == "📊 Statistics":
    display_statistics()

# --- FOOTER WITH ICONS ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='text-align: center; font-size: 16px;'>
      <b>Developed by <span style="color: #FF0000;">🔥 Muhammad Anas ❤😎</span></b>    
        <br><br>
        <a href="https://github.com/Anas-ahmed12?tab=repositories" target="_blank" style="margin-right: 15px;">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="30" height="30">
        </a>
        <a href="https://www.linkedin.com/in/anas-ahmed12/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30" height="30">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
