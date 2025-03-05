import sys
import os

sys.path.append(os.path.abspath('.'))

from bin import Updater


def update(command: str):
    print("updating...")
    """
    配置更新
    :param command: 更新配置选项
    """
    count = 0
    match command:
        case 'type':
            count = 1
        case 'module':
            count = 3
        case 'device':
            count = 4
        case 'script':
            count = 5
    for i in range(count):
        update_single(i)
    print("updating finished")


def update_single(num: int):
    match num:
        case 0:
            Updater.update_types()
        case 1:
            Updater.update_lib()
        case 2:
            Updater.update_modules()
        case 3:
            Updater.update_devices()
        case 4:
            Updater.update_scripts()


def single_run(name: str):
    """
    单独测试运行（运行脚本内的test函数）
    :param name: 测试脚本名称
    """
    from bin import DeviceInit
    from Interface import Devices
    script = __import__('Scripts.' + name, fromlist=[name])
    script.test()


def run():
    """
    运行
    """
    print("Starting...")
    from bin.System import System
    from bin import DeviceInit
    from bin import ScriptInit
    System.start()
    print("Started")
    command = ''
    while command != 'stop':
        command = input('>>> ')
    print("Stopping...")
    System.stop()
    from bin import ScriptStop
    print("Stopped")


if __name__ == '__main__':
    match sys.argv[1]:
        case 'update':
            update(sys.argv[2])
        case 'single_run':
            single_run(sys.argv[2])
        case 'run':
            run()
