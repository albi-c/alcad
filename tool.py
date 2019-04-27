class Tool:
    def __init__(self, name, fill=None, data=None):
        self.name = name
        self.fill = fill
        self.data = {"first": False, "x": -1, "y": -1}
        if name == "polygon":
            self.data["bx"] = -1
            self.data["by"] = -1
        if data != None:
            self.data = data
    def export(self):
        return {"type": "tool", "name": self.name, "fill": self.fill, "data": self.data}
    def load(d):
        return Tool(d["name"], d["fill"], d["data"])
