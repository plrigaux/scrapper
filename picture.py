class Picture:
    def __init__(self, index, href, fileName):
        self.index = index
        self.href = href
        self.fileName = fileName
    
    def __repr__(self) -> str:
        return str(vars(self))

    def __to_yaml_dict__(self):
        """ This optional method is called when you call yaml.dump()"""
        return vars(self)