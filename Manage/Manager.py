import sys
import os

sys.path.append(os.path.abspath('.'))

from bin import Updater


def install():
    if not os.path.exists('/srv/AScriptHome'):
        print("Please make a venv first!(python[version] -m venv /srv/AScriptHome)")
        print("Make Sure you're running this script on a virtual environment!")
        return True
    f = open('/etc/systemd/system/ascripthome.service', 'w')
    f.write('[Unit]\n')
    f.write('Description=AScriptHome System\n')
    f.write('After=network.target\n')
    f.write('[Service]\n')
    f.write('Type=simple\n')
    f.write('User=root\n')
    f.write('WorkingDirectory=' + os.path.abspath('.') + '\n')
    f.write('ExecStart=/bin/bash ' + os.path.abspath('./run.sh') + '\n')
    f.write('[Install]\n')
    f.write('WantedBy=multi-user.target\n')
    f.close()
    f = open(os.path.abspath("./run.sh"), 'w')
    f.write('#!/bin/bash\n')
    f.write('sleep 15\n')
    f.write('source /srv/AScriptHome/bin/activate\n')
    f.write('python ' + os.path.abspath('./bin/Main.py') + '\n')
    f.close()
    os.system('chmod +x ./run.sh')
    os.system('systemctl daemon-reload')
    os.system('systemctl enable ascripthome.service')
    return False

def check_install():
    if not os.path.exists('/etc/systemd/system/ascripthome.service'):
        print("Please Install First")
        return False
    if not os.path.exists('./run.sh'):
        print("Please Install First")
        return False
    return True


def update():
    if not check_install():
        return True
    Updater.update_types()
    Updater.update_lib()
    Updater.update_modules()
    Updater.update_devices()
    Updater.update_scripts()
    return False


def start():
    if not check_install():
        return True
    return os.system('systemctl restart ascripthome.service')


def stop():
    if not check_install():
        return True
    return os.system('systemctl stop ascripthome.service')


def uninstall():
    if not check_install():
        return True
    os.system('systemctl stop ascripthome.service')
    os.system('rm /etc/systemd/system/ascripthome.service')
    os.system('systemctl daemon-reload')
    return False


def status():
    if not check_install():
        return True
    os.system('systemctl status ascripthome.service')
    return False


if __name__ == '__main__':
    match sys.argv[1]:
        case 'install':
            if install():
                print("Installation failed")
        case 'update':
            if update():
                print("Update failed")
        case 'start':
            if start():
                print("Start failed")
        case 'stop':
            if stop():
                print("Stop failed")
        case 'uninstall':
            if uninstall():
                print("Uninstall failed")
        case 'status':
            if status():
                print("Status failed")
