class Picture:
    def __init__(self, index, href, fileName):
        self.index = index
        self.href = href
        self.fileName = fileName
    
    def __repr__(self) -> str:
        return str(vars(self))
