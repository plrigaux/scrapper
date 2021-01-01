class Picture:
    def __init__(self, index=-1, href="", fileName=None, status='new', **entries):
        self.index = index
        self.href = href
        self.fileName = fileName
        self.status = status
        self.__dict__.update(entries)

    def __repr__(self) -> str:
        return str(vars(self))

