class BibleModel:
    def __init__(self, file_path):
        self.file_path = file_path
        self.bible_name = ""
        self.edition = ""
        self.books: list[BibleBook] = []

    def load_bible_text(self):
        # Optimized logic to load the Bible text from the file (line-by-line, minimal memory usage)
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                current_book = None
                current_chapter = None
                for idx, line in enumerate(file):
                    line = line.strip()
                    if idx == 0:
                        self.bible_name = line
                        continue
                    if idx == 1:
                        self.edition = line
                        continue
                    if not line:
                        continue
                    line_parts = line.split(':', 1)
                    if len(line_parts) != 2:
                        continue  # skip malformed lines
                    book_chap = line_parts[0].strip()
                    verse_part = line_parts[1].strip()
                    if '\t' not in verse_part:
                        continue  # skip malformed lines
                    try:
                        book, chapter = book_chap.rsplit(' ', 1)
                        chapter = int(chapter)
                        verse, *verse_text = verse_part.split('\t', 1)
                        verse = int(verse)
                        verse_text = verse_text[0] if verse_text else ""
                    except Exception:
                        continue  # skip malformed lines
                    book_lower = book.lower()
                    if not current_book or current_book.name != book_lower:
                        if current_book:
                            if current_chapter:
                                current_book.chapters[current_chapter.number] = current_chapter
                                current_chapter = None
                            self.books.append(current_book)
                        current_book = BibleBook(name=book_lower, short_name=book[:3].lower(), chapters={})
                    if not current_chapter or current_chapter.number != chapter:
                        if current_chapter:
                            current_book.chapters[current_chapter.number] = current_chapter
                        current_chapter = BibleChapter(number=chapter, verses={})
                    current_chapter.verses[verse] = verse_text
                # Add the last chapter and book if they exist
                if current_chapter and current_book:
                    current_book.chapters[current_chapter.number] = current_chapter
                if current_book:
                    self.books.append(current_book)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")

    def get_verse(self, book, chapter: int, verse: int):
        # Logic to retrieve a specific verse from the Bible text
        book = book.lower()
        for b in self.books:
            if b.name == book or b.short_name == book:
                return b.get_verse(chapter, verse)
        raise ValueError(f"Book {book} not found in the Bible")
    
    def list_books(self):
        # Logic to list all books in the Bible text
        return [b for b in self.books]

    def search(self, query):
        # Logic to search for a query in the Bible text
        results = []
        for b in self.books:
            for c in b.chapters.values():
                for v in c.verses.values():
                    if query in v:
                        results.append((b.name, c.number, v))
        return results


class BibleBook:
    def __init__(self, name, short_name, chapters: dict[int, 'BibleChapter']):
        self.name = name.lower()
        self.short_name = short_name.lower()
        self.chapters: dict[int, BibleChapter] = chapters

    def list_chapters(self) -> list[int]:
        return list([chapter.number for chapter in self.chapters.values()])

    def get_chapter(self, chapter_number):
        if chapter_number not in self.chapters:
            raise ValueError(f"Chapter {chapter_number} not found in {self.name}")
        return self.chapters[chapter_number]

    def get_verse(self, chapter_number, verse_number):
        chapter = self.get_chapter(chapter_number)
        if isinstance(chapter, BibleChapter):
            return chapter.get_verse(verse_number)
        return chapter


class BibleChapter:
    def __init__(self, number, verses):
        self.number = number
        self.verses: dict[int, str] = verses

    def get_verse(self, verse_number):
        if verse_number not in self.verses:
            raise ValueError(f"Verse {verse_number} not found in chapter {self.number}")
        return self.verses[verse_number]