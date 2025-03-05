# Enable

from Interface import Devices, Subjects


class Subject_Switch(Subjects.DemoSwitch):
    def update(self, flag: bool):
        Devices.DemoLight.set(flag)
        Devices.DemoSwitch.notify(Devices.DemoLight.status())
