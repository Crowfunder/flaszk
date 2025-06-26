from ebooklib import epub

from _parser import Parser

class EpubParser(Parser):
    def get_ext(self) -> str:
        return 'epub'

    def parse(self, file_path):
        book = epub.read_epub(file_path)
        # Use get_metadata for robust extraction
        title_list = book.get_metadata('DC', 'title')
        author_list = book.get_metadata('DC', 'creator')
        title = title_list[0][0] if title_list else ''
        author = author_list[0][0] if author_list else ''
        return self.publish_results(title, author)

# Example usage
if __name__ == "__main__":
    path = "C:\\Users\\storm\\OneDrive\\Pulpit\\proces_kafka.epub"
    docx = EpubParser()
    print(docx(path))