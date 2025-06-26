from dataclasses import dataclass

class Parser:

    @dataclass
    class Results:
        title: str
        author: str

    def __init__(self):
        self.ext = self.get_ext()
        
    def get_ext(self) -> str:
        return ''
    
    def __call__(self, *args, **kwds):
        return self.parse(*args, **kwds)
    
    def parse(self, file_path):
        return self.publish_results()
    
    def publish_results(self, title='', author=''):
        '''
        Enforces format of results returned from parsers
        "parse()" should always return this method call.
        '''
        return self.Results(title=title, author=author)
