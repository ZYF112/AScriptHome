# Server

from Interface import BaseClass
from abc import ABC, abstractmethod


class Server(ABC):
    @abstractmethod
    def set(self, flag: bool):
        pass

    @abstractmethod
    def status(self) -> bool:
        pass


class Client(BaseClass.Client):
    def __init__(self, id: int):
        super().__init__(id)
        self.set = self.lock_func(self.set)

    def set(self, flag: bool):
        """
        开关控制
        :param flag: 开或关
        :type flag: bool
        :return: 是否执行
        :rtype: bool
        """
        if self.status() != flag:
            self.device.set(flag)
            return True
        return False

    def status(self):
        """
        返回当前状态
        :return: 开或关
        :rtype: bool
        """
        return self.device.status()
