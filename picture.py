import common
#import json


class Picture:
    index = -1
    status = common.NEW
    fileName = None
    href = ""
    imgSrc = None

    def __init__(self, index=-1, fileName=None, status=common.NEW, href="", **entries):
        self.index = index
        self.href = href
        self.fileName = fileName
        self.status = status    
        self.__dict__.update((), **entries)

    def __repr__(self) -> str:
        #print("!!!!!!!!!!!!!!!!!!!!!", self.__dict__.keys())
        return str(self.__dict__)


"""
    def __repr__(self) -> str:
        return self.toJSON()
    
    def toJSON(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
"""
