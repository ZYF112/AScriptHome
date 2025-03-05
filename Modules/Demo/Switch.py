from Interface import TypeBase, TypeServer, TypeSubject
from abc import ABC
import threading
from time import sleep


class Server(TypeBase.Server, TypeServer.RemoteSwitch, TypeSubject.RemoteSwitch):
    def __init__(self, name: str, interval: int):
        self.name = name
        self.interval = interval
        self.thread = None
        self.stop_event = threading.Event()
        TypeBase.Server.__init__(self, self)
        TypeSubject.RemoteSwitch.__init__(self, self.id)

    def notify(self, flag: bool):
        if flag:
            print('the Light on - ' + self.name)
        else:
            print('the Light off - ' + self.name)

    def fun(self):
        while not self.stop_event.is_set():
            sleep(self.interval)
            self.subject_notify(True)
            sleep(self.interval)
            self.subject_notify(True)
            sleep(self.interval)
            self.subject_notify(False)
            sleep(self.interval)
            self.subject_notify(False)

    def subject_start(self):
        self.thread = threading.Thread(target=self.fun)
        self.thread.start()

    def subject_stop(self):
        self.stop_event.set()
        self.thread.join()

    def start(self):
        pass

    def stop(self):
        pass


class Template(ABC):
    module = 'Demo.Switch'
    client = 'RemoteSwitch'
    subject = 'RemoteSwitch'
    name: str
    interval: int = 2

    @classmethod
    def help(cls):
        say = "Param:\n"
        say += "\t开关名称: (name: str)\n"
        say += "\t开关间隔: (interval: int)\n[默认2]"
        return say

    @classmethod
    def unpack(cls):
        return cls.name, cls.interval
