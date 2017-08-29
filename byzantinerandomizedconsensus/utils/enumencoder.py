import json
from byzantinerandomizedconsensus.utils.messagetype import MessageType


class EnumEncoder(json.JSONEncoder):

    PUBLIC_ENUMS = {
        'MessageType': MessageType
    }

    def default(self, obj):
        if type(obj) in self.PUBLIC_ENUMS.values():
            return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)

    def as_enum(self, d):
        if "__enum__" in d:
            name, member = d["__enum__"].split(".")
            return getattr(self.PUBLIC_ENUMS[name], member)
        else:
            return d