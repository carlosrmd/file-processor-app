from itertools import islice
import json


class FileFormatter:

    def __init__(self, separator):
        self.separator = separator
        self.skip_first_line = False

    def format(self, line):
        raise NotImplementedError


class CsvFileFormatter(FileFormatter):

    def __init__(self, separator):
        super().__init__(separator)
        self.skip_first_line = True

    def format(self, line):
        return line.replace('\n', '').split(self.separator)


class JsonlinesFileFormatter(FileFormatter):

    def format(self, line):
        j = json.loads(line)
        return [j['site'], j['id']]


class TextFileFormatter(FileFormatter):

    def format(self, line):
        return line.replace('\n', '').split(self.separator)


class FileReader:

    def __init__(self, file_name, formatter, encoding):
        self.file_name = file_name
        self._formatter = formatter
        self.encoding = encoding

    def chunk_reader(self, chunk_size):
        file_descriptor = open(self.file_name, 'r', encoding=self.encoding)
        if self._formatter.skip_first_line:
            file_descriptor.readline()  # Skip first line
        new_round = True
        while new_round:
            print("Starting new chunk...")
            lines = []
            current_chunk = islice(file_descriptor, chunk_size)
            new_round = False
            for line in current_chunk:
                s = self._formatter.format(line)
                lines.append(s)
                new_round = True
            yield lines


class FileProcessor:

    def __init__(self, file_reader, chunk_size, api_manager):
        self._file_reader = file_reader
        self._chunk_size = chunk_size
        self._api_manager = api_manager

    def process(self):
        for line_set in self._file_reader.chunk_reader(self._chunk_size):
            if not line_set:
                # Empty list implies EOF
                break
            self._api_manager.download_and_store_items(line_set)


file_format_classes = {
    'csv': CsvFileFormatter,
    'jsonlines': JsonlinesFileFormatter,
    'text': TextFileFormatter
}
