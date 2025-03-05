import os
from pip._internal import main as pip_main


def update_types():
    """
    更新Type
    """
    print("Updating Types...")
    lines_server = []
    lines_subject = []
    lines_forwards = []
    files = []
    if os.path.exists("Types"):
        files = os.listdir("Types")
    else:
        print("No Types folder found")
    for file in files:
        if file.endswith(".py"):
            name = file.split(".")[0]
            ff = open("Types/" + file, "r", encoding="utf-8")
            supports = ff.readline()[2:-1].split(",")
            ff.close()
            for support in supports:
                match support:
                    case 'Server':
                        lines_server.append('from Types.' + name + ' import Server as ' + name + '\n')
                    case 'Subject':
                        lines_subject.append('from Types.' + name + ' import Subject as ' + name + '\n')
                    case 'Forward':
                        lines_forwards.append('from Types.' + name + ' import Forward as ' + name + '\n')
                    case _:
                        raise Exception("Error Mode For Type")
            f = open("Interface/TypeServer.py", "w")
            f.writelines(lines_server)
            f.close()
            f = open("Interface/TypeSubject.py", "w")
            f.writelines(lines_subject)
            f.close()
            f = open("Interface/TypeForward.py", "w")
            f.writelines(lines_forwards)
            f.close()
    print("Type Updated Successfully")


def update_lib():
    """
    更新python环境包
    """
    print("Updating Library...")
    dirs = []
    if os.path.exists("Modules"):
        dirs = os.listdir("Modules")
    else:
        print("No Modules folder found")
    for d in dirs:
        if os.path.exists("Modules/" + d + "/requirements.txt"):
            print("Installing " + d + " Requirements...")
            pip_main(['install', '-r', './Modules/' + d + '/requirements.txt'])
    print("Library Updated Successfully")


def update_modules():
    """
    更新Module
    """
    print("Updating Modules...")
    lines = []
    dirs = []
    if os.path.exists("Modules"):
        dirs = os.listdir("Modules")
    else:
        print("No Modules folder found")
    for d in dirs:
        files = os.listdir("Modules/" + d)
        lines.append('class ' + d + ':\n')
        for f in files:
            if f.endswith(".py"):
                name = f.split(".")[0]
                lines.append('\tfrom Modules.' + d + '.' + name + ' import Template as ' + name + '\n')
    f = open("Interface/ModuleTemplates.py", "w")
    f.writelines(lines)
    f.close()
    print("Module Updated Successfully")


def update_devices():
    """
    更新用户设备
    """
    print("Updating Devices...")
    files = []
    modules = []
    modules_line = []
    clients = []
    clients_line = []
    subjects = []
    subjects_line = []
    forwards = []
    forwards_line = []
    devices_lines_server = []
    devices_lines_client = []
    devices_lines_subject = []
    devices_lines_forward = []
    depend_devices = []
    device_count = 0
    if os.path.exists("DeviceConfig"):
        files = os.listdir("DeviceConfig")
    else:
        print("No DeviceConfig folder found")
    for file in files:
        if file.endswith(".py"):
            ff = open("DeviceConfig/" + file, "r", encoding="utf-8")
            flag_str = ff.readline()[2:-1]
            ff.close()
            match flag_str:
                case 'Enable':
                    pass
                case 'Disable':
                    continue
                case _:
                    raise Exception("Device Config Error: flag value error")
            name = file.split(".")[0]
            config = __import__("DeviceConfig." + name, fromlist=[name])
            # 判断是否有依靠
            if 'depend_on' in dir(config.Config):
                depend_flag, depend_count = config.Config.depend_on()
                if depend_flag:
                    if len(depend_devices) < depend_count:
                        depend_devices.append([])
                    depend_devices[depend_count - 1].append(file)
                    continue
            # 常规注册
            module_str: str = config.Config.module
            client_name: str = config.Config.client
            if module_str not in modules:
                modules.append(module_str)
                modules_line.append('from Modules.' + module_str + ' import Server as ' + module_str.split(".")[0] +
                                    '_' + module_str.split(".")[1] + '\n')
            if client_name not in clients:
                clients.append(client_name)
                if client_name == "Base":
                    clients_line.append('\tfrom Interface.BaseClass import Client as Base\n')
                else:
                    clients_line.append('\tfrom Types.' + client_name + ' import Client as ' + client_name + '\n')
            devices_lines_server.append('from DeviceConfig.' + name + ' import Config as ' + name + '\n')
            devices_lines_server.append(module_str.split(".")[0] + '_' + module_str.split(".")[1] + '(*' + name +
                                        '.unpack())\n')
            devices_lines_client.append(name + ' = _Env.' + client_name + '(' + str(device_count) + ')\n')
            # 判断是否有事件
            event_flag = False
            event_type = 'None'
            if 'subject' in dir(config.Config):
                if event_flag:
                    raise Exception("Device Config Error: event too much")
                event_flag = True
                event_type = 'Subject'
            if 'forward' in dir(config.Config):
                if event_flag:
                    raise Exception("Device Config Error: event too much")
                event_flag = True
                event_type = 'Forward'
            if not event_flag:
                device_count += 1
                continue
            # 注册事件
            match event_type:
                case 'Subject':
                    subject_name: str = config.Config.subject
                    if subject_name not in subjects:
                        subjects.append(subject_name)
                        subjects_line.append('\tfrom Types.' + subject_name + ' import Observer as ' + subject_name + '\n')
                    devices_lines_subject.append('class ' + name + '(_Env.' + subject_name +
                                                 ', _Env.ABC):\n\tdef __init__(self):\n\t\tsuper().__init__(' +
                                                 str(device_count) + ')\n\n')
                case 'Forward':
                    forward_name: str = config.Config.forward
                    if forward_name not in forwards:
                        forwards.append(forward_name)
                        forwards_line.append('\tfrom Types.' + forward_name + ' import Node as ' + forward_name + '\n')
                    devices_lines_forward.append('class ' + name + '(_Env.' + forward_name +
                                                 ', _Env.ABC):\n\tdef __init__(self, name: str):\n\t\tsuper().__init__('
                                                 + str(device_count) +
                                                 ', name)\n')
            device_count += 1
    # 依赖注册
    for depend in depend_devices:
        for file in depend:
            name = file.split(".")[0]
            config = __import__("DeviceConfig." + name, fromlist=[name])
            # 常规注册
            module_str: str = config.Config.module
            client_name: str = config.Config.client
            if module_str not in modules:
                modules.append(module_str)
                modules_line.append('from Modules.' + module_str + ' import Server as ' + module_str.split(".")[0] +
                                    '_' + module_str.split(".")[1] + '\n')
            if client_name not in clients:
                clients.append(client_name)
                if client_name == "Base":
                    clients_line.append('\tfrom Interface.BaseClass import Client as Base\n')
                else:
                    clients_line.append('\tfrom Types.' + client_name + ' import Client as ' + client_name + '\n')
            devices_lines_server.append('from DeviceConfig.' + name + ' import Config as ' + name + '\n')
            devices_lines_server.append(module_str.split(".")[0] + '_' + module_str.split(".")[1] + '(*' + name +
                                        '.unpack())\n')
            devices_lines_client.append(name + ' = _Env.' + client_name + '(' + str(device_count) + ')\n')
            # 判断是否有事件
            event_flag = False
            event_type = 'None'
            if 'subject' in dir(config.Config):
                if event_flag:
                    raise Exception("Device Config Error: event too much")
                event_flag = True
                event_type = 'Subject'
            if 'forward' in dir(config.Config):
                if event_flag:
                    raise Exception("Device Config Error: event too much")
                event_flag = True
                event_type = 'Forward'
            if not event_flag:
                device_count += 1
                continue
            # 注册事件
            match event_type:
                case 'Subject':
                    subject_name: str = config.Config.subject
                    if subject_name not in subjects:
                        subjects.append(subject_name)
                        subjects_line.append(
                            '\tfrom Types.' + subject_name + ' import Observer as ' + subject_name + '\n')
                    devices_lines_subject.append('class ' + name + '(_Env.' + subject_name +
                                                 ', _Env.ABC):\n\tdef __init__(self):\n\t\tsuper().__init__(' +
                                                 str(device_count) + ')\n\n')
                case 'Forward':
                    forward_name: str = config.Config.forward
                    if forward_name not in forwards:
                        forwards.append(forward_name)
                        forwards_line.append('\tfrom Types.' + forward_name + ' import Node as ' + forward_name + '\n')
                    devices_lines_forward.append('class ' + name + '(_Env.' + forward_name +
                                                 ', _Env.ABC):\n\tdef __init__(self, name: str):\n\t\tsuper().__init__('
                                                 + str(device_count) +
                                                 ', name)\n')
            device_count += 1

    # 文件写入
    f = open("bin/DeviceInit.py", "w")
    f.writelines(modules_line)
    f.write('\n')
    f.writelines(devices_lines_server)
    f.close()
    f = open("Interface/Devices.py", "w")
    f.write('class _Env:\n')
    f.writelines(clients_line)
    f.write('\n')
    f.writelines(devices_lines_client)
    f.close()
    f = open("Interface/Subjects.py", "w")
    f.write('class _Env:\n')
    f.write('\tfrom abc import ABC\n')
    f.writelines(subjects_line)
    f.write('\n\n')
    f.writelines(devices_lines_subject)
    f.close()
    f = open("Interface/Forwards.py", "w")
    f.write('from Interface import TypeForward\n\n')
    f.write('class _Env:\n')
    f.write('\tfrom abc import ABC\n')
    f.writelines(forwards_line)
    f.write('\n\n')
    f.writelines(devices_lines_forward)
    f.close()
    print("Devices Updated Successfully")


def update_scripts():
    """
    更新用户脚本
    """
    print("Updating Scripts...")
    from bin import DeviceInit
    files = []
    import_lines = []
    init_lines = []
    stop_lines = []
    class_lines = []
    if os.path.exists("Scripts"):
        files = os.listdir("Scripts")
    else:
        print("No Scripts folder found")
    for file in files:
        if file.endswith(".py"):
            name = file.split(".")[0]
            ff = open("Scripts/" + file, "r", encoding="utf-8")
            flag_str = ff.readline()[2:-1]
            ff.close()
            match flag_str:
                case 'Enable':
                    pass
                case 'Disable':
                    continue
                case _:
                    raise Exception("Script" + name + "Config Error: flag value error")
            import_lines.append('from Scripts import ' + name + '\n')
            script = __import__("Scripts." + name, fromlist=[name])
            if 'init' in dir(script):
                init_lines.append(name + '.init()\n')
            if 'stop' in dir(script):
                stop_lines.append(name + '.stop()\n')
            dirs = dir(script)
            for d in dirs:
                if len(d.split("_")) < 2:
                    continue
                if d.split("_")[0] == "Subject":
                    class_lines.append(name + '.' + d + '()\n')
                if d.split("_")[0] == "Forward":
                    class_lines.append(name + '.' + d + '()\n')
    f = open("bin/ScriptInit.py", "w")
    f.writelines(import_lines)
    f.write('\n')
    f.writelines(init_lines)
    f.write('\n')
    f.writelines(class_lines)
    f.close()
    f = open("bin/ScriptStop.py", "w")
    f.writelines(import_lines)
    f.write('\n')
    f.writelines(stop_lines)
    f.close()
    print("Scripts Updated Successfully")
