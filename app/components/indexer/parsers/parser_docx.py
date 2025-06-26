from docx import Document

from _parser import Parser

class DocxParser(Parser):
    def get_ext(self):
        return 'docx'

    def parse(self, file_path):
        doc = Document(file_path)
        core_props = doc.core_properties
        return self.publish_results(core_props.title, core_props.author)
