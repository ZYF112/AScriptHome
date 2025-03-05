# Server,Subject

from Interface import BaseClass
from abc import ABC, abstractmethod


class Server(ABC):
    @abstractmethod
    def notify(self, flag: bool):
        pass


class Client(BaseClass.Client):
    def __init__(self, id: int):
        super().__init__(id)
        self.notify = self.lock_func(self.notify)

    def notify(self, flag: bool):
        """
        状态改变通知
        :param flag: 开或关
        """
        self.device.notify(flag)


class Subject(BaseClass.Subject, ABC):
    def subject_notify(self, flag: bool):
        self.observers_notify(flag)


class Observer(BaseClass.Observer, ABC):
    @abstractmethod
    def update(self, flag: bool):
        """
        开关动作通知
        :param flag: 开或关
        """
        pass
