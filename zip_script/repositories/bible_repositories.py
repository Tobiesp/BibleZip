import os
from zip_script.models.bible_model import BibleModel

class BibleRepository:
    def __init__(self):
        self.bible_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bibles')
        self.bible_dir = os.path.abspath(self.bible_dir)

    def list_bibles(self):
        bibles = []
        for file in os.listdir(self.bible_dir):
            if file.endswith('.txt'):
                # read first line to get the Bible name
                with open(os.path.join(self.bible_dir, file), 'r', encoding='utf-8') as f:
                    bible_name = f.readline().strip()
                bibles.append({
                    'name': bible_name.lower(),
                    'file': file,
                    'path': os.path.join(self.bible_dir, file)
                })
        return bibles
    
    def get_bible(self, file_path: str):
        bible_path = os.path.join(self.bible_dir, file_path)
        if not os.path.exists(bible_path):
            raise FileNotFoundError(f"The Bible file {file_path} does not exist.")

        self.bible_model = BibleModel(bible_path)
        self.bible_model.load_bible_text()
        return self.bible_model
