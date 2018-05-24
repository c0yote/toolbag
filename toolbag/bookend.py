class Bookend:
    def __init__(self, intro, outro):
        self.intro = intro
        self.outro = outro
        
        print(self.intro, end='')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        print(self.outro)
    
    def change_outro(self, new_outro):
        self.outro = new_outro