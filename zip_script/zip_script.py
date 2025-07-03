from tkinter import *
from tkinter import ttk
from zip_script.models.bible_model import BibleBook, BibleModel
from zip_script.repositories.bible_repositories import BibleRepository


BIBLE: BibleModel = None
BOOK: BibleBook = None
BIBLES_VAR = None
BOOKS_VAR = None
CHAPTER_VAR = None
VERSE_VAR = None


def main():
    root = Tk()
    root.geometry("800x600")
    root.resizable(False, False)
    global BIBLES_VAR, BOOKS_VAR, CHAPTER_VAR, VERSE_VAR
    BIBLES_VAR = StringVar()
    BOOKS_VAR = StringVar()
    CHAPTER_VAR = StringVar()
    VERSE_VAR = StringVar()
    repository = BibleRepository()
    root.title("ZipScript 2.0")
    
    # Create a simple label
    label = ttk.Label(root, text="Welcome to ZipScript 2.0!")
    label.pack(pady=20)

    # Frame to hold the label and dropdown inline
    bible_frame = ttk.Frame(root)
    bible_frame.pack(pady=10)

    bibles_label = ttk.Label(bible_frame, text="Bibles:")
    bibles_label.pack(side=LEFT, padx=(0, 5))

    BIBLES_VAR.set(repository.list_bibles()[0]['name'])  # default value

    # load the first bible by default
    BIBLE = repository.get_bible(file_path=repository.list_bibles()[0]['path'])

    # Selecting a bible will load it
    def load_bible(selected_bible_name):
        file_path = next((bible['path'] for bible in repository.list_bibles() if bible['name'] == selected_bible_name), None)
        if not file_path:
            print(f"Bible {selected_bible_name} not found.")
            return
        global BIBLE
        BIBLE = repository.get_bible(file_path=file_path)
        if not BIBLE:
            print(f"Failed to load Bible: {selected_bible_name}")
            return
        # Reset BOOK and CHAPTER_VAR when a new Bible is loaded
        global BOOKS_VAR, CHAPTER_VAR, BOOK
        BOOK = None
        BOOKS_VAR.set(BIBLE.list_books()[0]['name'] if BIBLE and BIBLE.list_books() else "Select a book")
        CHAPTER_VAR.set("Select a chapter")
        # Do something with the loaded bible
        print(f"Loaded Bible: {BIBLE.bible_name} ({BIBLE.edition})")

    bibles_dropdown = ttk.OptionMenu(
        bible_frame,
        BIBLES_VAR,
        repository.list_bibles()[0]['name'],
        *[b['name'] for b in repository.list_bibles()],
        command=load_bible
    )
    bibles_dropdown.pack(side=LEFT)

    books_label = ttk.Label(bible_frame, text="Books:")
    books_label.pack(side=LEFT, padx=(10, 5))

    def load_book(selected_book_name):
        if not BIBLE:
            print("No Bible loaded.")
            return
        global BOOK, CHAPTER_VAR
        BOOK = next((b for b in BIBLE.list_books() if b.name == selected_book_name), None)
        if not BOOK:
            print(f"Book {selected_book_name} not found in the loaded Bible.")
            return
        chapters = [str(c) for c in BOOK.list_chapters()] if BOOK and BOOK.list_chapters() else []
        # Update the chapter dropdown menu
        menu = chapter_dropdown['menu']
        menu.delete(0, 'end')
        for chapter in chapters:
            menu.add_command(label=chapter, command=lambda value=chapter: CHAPTER_VAR.set(value))
        CHAPTER_VAR.set(chapters[0] if chapters else "Select a chapter")
        # Do something with the selected book
        print(f"Selected Book: {BOOK.name} ({BOOK.short_name})")

    books_dropdown = ttk.OptionMenu(
        bible_frame,
        BOOKS_VAR,
        "Select a book",
        *[book.name for book in BIBLE.list_books()] if BIBLE else [],
        command=load_book
    )
    books_dropdown.pack(side=LEFT)

    chapters_label = ttk.Label(bible_frame, text="Chapters:")
    chapters_label.pack(side=LEFT, padx=(10, 5))

    def load_chapter(selected_chapter):
        if not BOOK:
            print("No book selected.")
            return
        global VERSE_VAR
        chapter_num = int(selected_chapter)
        verses = [str(v) for v in BOOK.chapters[chapter_num].verses.keys()] if chapter_num in BOOK.chapters else []
        # Update the verse dropdown menu
        menu = verse_dropdown['menu']
        menu.delete(0, 'end')
        for verse in verses:
            menu.add_command(label=verse, command=lambda value=verse: VERSE_VAR.set(value))
        VERSE_VAR.set(verses[0] if verses else "Select a verse")
        print(f"Selected Chapter: {selected_chapter}")

    CHAPTER_VAR.trace_add('write', lambda *args: load_chapter(CHAPTER_VAR.get()) if CHAPTER_VAR.get().isdigit() else None)

    chapter_dropdown = ttk.OptionMenu(
        bible_frame,
        CHAPTER_VAR,
        "Select a chapter",
        *[str(chapter) for chapter in BOOK.list_chapters()] if BOOK else [],
        command=load_chapter
    )
    chapter_dropdown.pack(side=LEFT)

    verse_label = ttk.Label(bible_frame, text="Verses:")
    verse_label.pack(side=LEFT, padx=(10, 5))

    verse_dropdown = ttk.OptionMenu(
        bible_frame,
        VERSE_VAR,
        "Select a verse",
    )
    verse_dropdown.pack(side=LEFT)

    # Verses range selection
    verse_range_frame = ttk.Frame(root)
    verse_range_frame.pack(fill="x", padx=20, pady=(10, 0))
    verse_range_label = ttk.Label(verse_range_frame, text="Verse Range:")
    verse_range_label.pack(anchor="w")
    verse_start_var = StringVar()
    verse_end_var = StringVar()
    verse_start_dropdown = ttk.OptionMenu(verse_range_frame, verse_start_var, "Start", "")
    verse_end_dropdown = ttk.OptionMenu(verse_range_frame, verse_end_var, "End", "")
    verse_start_dropdown.pack(side=LEFT, padx=(0, 5))
    verse_end_dropdown.pack(side=LEFT, padx=(5, 0))

    # Move search field for verse range above the verse text box
    search_frame = ttk.Frame(root)
    search_frame.pack(fill="x", padx=20, pady=(10, 0))
    search_label = ttk.Label(search_frame, text="Search (e.g. John 3:16-18):")
    search_label.pack(side=LEFT, padx=(0, 5))
    search_var = StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side=LEFT, padx=(0, 5))

    def search_verse_range():
        query = search_var.get().strip()
        import re
        match = re.match(r'([\w ]+)\s+(\d+):(\d+)(?:-(\d+))?', query)
        if not match:
            verse_text.config(state="normal")
            verse_text.delete("1.0", "end")
            verse_text.insert("1.0", "Invalid search format. Use e.g. John 3:16-18")
            verse_text.config(state="disabled")
            return
        book_name, chapter, start_verse, end_verse = match.groups()
        book_name = book_name.strip().lower()
        chapter = int(chapter)
        start_verse = int(start_verse)
        end_verse = int(end_verse) if end_verse else start_verse
        # Find the book
        book = next((b for b in BIBLE.list_books() if b.name.lower() == book_name or b.short_name.lower() == book_name), None)
        if not book or chapter not in book.chapters:
            verse_text.config(state="normal")
            verse_text.delete("1.0", "end")
            verse_text.insert("1.0", "Book or chapter not found.")
            verse_text.config(state="disabled")
            return
        verses = [book.chapters[chapter].verses.get(v, "") for v in range(start_verse, end_verse+1)]
        range_text = " ".join([f"[v{v}] {t}" for v, t in zip(range(start_verse, end_verse+1), verses)])
        verse_text.config(state="normal")
        verse_text.delete("1.0", "end")
        verse_text.insert("1.0", range_text)
        verse_text.config(state="disabled")

    search_button = ttk.Button(search_frame, text="Search", command=search_verse_range)
    search_button.pack(side=LEFT, padx=(5, 0))

    # Text box to display verse text
    verse_text_frame = ttk.Frame(root)
    verse_text_frame.pack(fill="x", padx=20, pady=(30, 10))
    verse_text_label = ttk.Label(verse_text_frame, text="Verse Text:")
    verse_text_label.pack(anchor="w")
    verse_text = Text(verse_text_frame, height=12, wrap="word", state="disabled")
    verse_text.pack(fill="x")

    def show_verse_text(*args):
        if not BOOK or not CHAPTER_VAR.get().isdigit() or not VERSE_VAR.get().isdigit():
            verse_text.config(state="normal")
            verse_text.delete("1.0", "end")
            verse_text.insert("1.0", "")
            verse_text.config(state="disabled")
            return
        chapter_num = int(CHAPTER_VAR.get())
        verse_num = int(VERSE_VAR.get())
        text_val = BOOK.chapters.get(chapter_num, None)
        if text_val:
            verse_val = text_val.verses.get(verse_num, "")
        else:
            verse_val = ""
        verse_text.config(state="normal")
        verse_text.delete("1.0", "end")
        verse_text.insert("1.0", verse_val)
        verse_text.config(state="disabled")

    VERSE_VAR.trace_add('write', show_verse_text)
    CHAPTER_VAR.trace_add('write', show_verse_text)

    def copy_range_to_clipboard():
        text = verse_text.get("1.0", "end").strip()
        if text:
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()  # Keeps clipboard after app closes

    copy_button = ttk.Button(root, text="Copy Range", command=copy_range_to_clipboard)
    copy_button.pack(pady=(0, 10))

    # Create a button to exit the application
    exit_button = ttk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()