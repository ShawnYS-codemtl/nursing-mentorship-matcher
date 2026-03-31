import csv
from .base import DataSource

class CSVDataSource(DataSource):
    def __init__(self, mentor_path, mentee_path):
        self.mentor_path = mentor_path
        self.mentee_path = mentee_path

    def get_mentor_rows(self):
        with open(self.mentor_path, newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def get_mentee_rows(self):
        with open(self.mentee_path, newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))