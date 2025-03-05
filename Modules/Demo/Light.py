from Interface import TypeBase, TypeServer
from abc import ABC


class Server(TypeBase.Server, TypeServer.SimpleSwitch):
    def __init__(self, name: str, none: None):
        self.name = name
        self.flag = False
        TypeBase.Server.__init__(self, self)

    def set(self, flag: bool):
        self.flag = flag
        if self.flag:
            print("the Light " + self.name + " is on")
        else:
            print("the Light " + self.name + " is off")

    def status(self) -> bool:
        print("the Light " + self.name + "'s status is " + str(self.flag))
        return self.flag

    def start(self):
        pass

    def stop(self):
        pass


class Template(ABC):
    module = 'Demo.Light'
    client = 'SimpleSwitch'
    name: str

    @classmethod
    def help(cls):
        say = "Param:\n"
        say += "\t灯名称: (name: str)\n"
        return say

    @classmethod
    def unpack(cls):
        return cls.name, None
