import os
import sys
import signal

sys.path.append(os.path.abspath('.'))
print("Starting...")

from bin import System
from bin import DeviceInit
from bin import ScriptInit


def stop():
    print("Stopping...")
    System.System.stop()
    from bin import ScriptStop
    print("Stopped")


def handler(signum, frame):
    stop()
    exit(0)


System.System.start()
print("Started")
signal.signal(signal.SIGINT, handler)
signal.pause()
