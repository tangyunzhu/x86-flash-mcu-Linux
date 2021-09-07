import subprocess
import datetime
import os
import time
import shlex
import serial
from serial.tools import list_ports
from time import sleep

tool = 'bossac'
#BOOTLOADER = 'firmware/optiboot_atmega328.hex'
TEST_PROGRAM = 'ReComputer_GPIO.ino.bin'

def timeout_command(command, timeout=10):
    """
    call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None
    """

    if type(command) == type(''):
        command = shlex.split(command)
    start = datetime.datetime.now()
    process = subprocess.Popen(command)  # , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    resultcode = process.poll()
    while resultcode is None:
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            process.kill()
            return -1
        sleep(0.01)
        resultcode = process.poll()
    return resultcode

def find_device():
    timeout = 30
    while timeout != 0:
        port = None
        for p in list_ports.comports():
            print p[2]
            if p[2].upper().startswith('USB VID:PID=2886:0027'):
                port = p[0]
                print('find port: ' + port)
                return port

            if p[2].upper().startswith('USB VID:PID=2886:8027'):
                port = p[0]
                com = serial.Serial(port, 1200)
                com.dtr = False
                com.close
                time.sleep(0.5)

        sleep(0.1)
        timeout -= 1

    print('No SAM21 chip found')
    return None

def write_test():
    print('Write  test program to test board')
    port = find_device()
    if not port:
        return -1

    cmd = './bossac -i -d --port=%s -U true -i -e -w -v %s -R' % ( port, TEST_PROGRAM)
    return timeout_command(cmd)


port=find_device()
write_test()  


