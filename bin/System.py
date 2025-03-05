from functools import wraps
from abc import ABC, abstractmethod
import threading


# =============== Server/Client =================
class Server(ABC):
    def __init__(self, device):
        self.id = System.add_device(self)

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def start(self):
        pass


class Client(ABC):
    def __init__(self, id: int):
        self.id = id
        self.device = System.get_device(id)
        self.lock = threading.Lock()

    def lock_func(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                return func(*args, **kwargs)

        return wrapper


# =============== Subject/Observer =================
class Subject(ABC):
    def __init__(self, id: int):
        self.observers = []
        System.add_subject(id)

    def add_observer(self, observer):
        self.observers.append(observer)

    def observers_notify(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)

    @abstractmethod
    def subject_notify(self, *args, **kwargs):
        pass

    @abstractmethod
    def subject_start(self):
        pass

    @abstractmethod
    def subject_stop(self):
        pass


class Observer(ABC):
    def __init__(self, id: int):
        self.device = System.get_device(id)
        self.device.add_observer(self)

    @abstractmethod
    def update(self, *args, **kwargs):
        pass


# =============== Forward/Node =================
class Forward(ABC):
    def __init__(self, id: int):
        self.nodes = {
            'self': self
        }
        self.end_event = threading.Event()
        self.param = None
        System.add_forward(id)

    def add_node(self, name: str, node):
        self.nodes[name] = node

    def run(self):
        self.end_event.set()
        return 'end'

    def forward_flow(self, name: str):
        self.end_event.clear()
        while not self.end_event.is_set():
            name = self.nodes[name].run()

    @abstractmethod
    def post_param(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_param(self):
        pass

    @abstractmethod
    def forward_start(self):
        pass

    @abstractmethod
    def forward_stop(self):
        pass


class Node(ABC):
    def __init__(self, id: int, name: str):
        self.device = System.get_device(id)
        self.device.add_node(name, self)
        self.forward_post_param = self.device.post_param
        self.forward_get_param = self.device.get_param

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def post_param(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_param(self):
        pass


# =============== External_Interface =================
class External_Interface:

    @staticmethod
    def add_interface(name: str, id: int):
        System.add_interface(name, id)

    @staticmethod
    def get_interface(name: str):
        return System.get_interface(name)


# =============== System =================
class System:
    devices = []
    subjects = []
    forwards = []
    interfaces = {}
    interface_users= []

    @classmethod
    def add_device(cls, device):
        cls.devices.append(device)
        return len(cls.devices) - 1

    @classmethod
    def get_device(cls, id: int):
        return cls.devices[id]

    @classmethod
    def add_subject(cls, id: int):
        cls.subjects.append(id)

    @classmethod
    def start_subject(cls):
        for subject in cls.subjects:
            device = cls.get_device(subject)
            if len(device.observers) < 1:
                continue
            device.subject_start()

    @classmethod
    def stop_subject(cls):
        for subject in cls.subjects:
            device = cls.get_device(subject)
            if len(device.observers) < 1:
                continue
            device.subject_stop()

    @classmethod
    def add_forward(cls, id: int):
        cls.forwards.append(id)

    @classmethod
    def start_forward(cls):
        for forward in cls.forwards:
            device = cls.get_device(forward)
            if len(device.nodes) < 2:
                continue
            device.forward_start()

    @classmethod
    def stop_forward(cls):
        for forward in cls.forwards:
            device = cls.get_device(forward)
            if len(device.nodes) < 2:
                continue
            device.forward_stop()

    @classmethod
    def add_interface(cls, name: str, id: int):
        if name in cls.interfaces.keys():
            raise KeyError(f'Interface {name} already exists')
        if id in cls.interfaces.values():
            raise ValueError(f'Interface {id} already exists')
        cls.interfaces[name] = id

    @classmethod
    def get_interface(cls, name: str):
        return cls.devices[cls.interfaces[name]]

    @classmethod
    def start(cls):
        for device in cls.devices:
            device.start()
        cls.start_subject()
        cls.start_forward()

    @classmethod
    def stop(cls):
        cls.stop_subject()
        cls.stop_forward()
        for device in cls.devices:
            device.stop()
