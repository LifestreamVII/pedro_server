#!/usr/bin/python3

import dbus
import re
from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor
from hashlib import sha256
from commands import Command
from fileio import wFile
import random

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class SimpleBLEAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("SimpleBLEDevice")
        self.include_tx_power = True

class SimpleBLEService(Service):
    SIMPLE_SVC_UUID = "00000001-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, index):
        Service.__init__(self, index, self.SIMPLE_SVC_UUID, True)
        # need Characteristics for status, data storage, trainer data, boxes, etc.
        # Define constants for UUIDs
        COMMANDS_CHARACTERISTIC_UUID = "54a69653-1077-4c1b-a4d9-644179df7b6e"
        STATUS_CHARACTERISTIC_UUID = "c2f58894-ed80-4f98-be74-ea99cdab409f"
        GAMEINFO_CHARACTERISTIC_UUID = "42621f66-0772-4967-96a0-e11e31aee5b9"
        DATA1_CHARACTERISTIC_UUID = "aa17a295-7840-4076-a1ce-845aa9968368"
        DATA2_CHARACTERISTIC_UUID = "cbbe0aff-5e75-49ae-bad2-a9cac26bd3cb"
        # 0 - Commands characteristic
        self.add_characteristic(CommandsCharacteristic(self, COMMANDS_CHARACTERISTIC_UUID, ["notify", "read", "write", "write-without-response"]))
        # 1 - Gameinfo characteristic
        self.add_characteristic(GameInfoCharacteristic(self, GAMEINFO_CHARACTERISTIC_UUID, ["notify", "read", "write", "write-without-response"]))
        # 2 - Data1 characteristic
        self.add_characteristic(DataOutputCharacteristic(self, DATA1_CHARACTERISTIC_UUID, ["notify", "read", "write", "write-without-response"]))
        # 3 - Data2 characteristic
        self.add_characteristic(DataOutputCharacteristic(self, DATA2_CHARACTERISTIC_UUID, ["notify", "read", "write", "write-without-response"]))
        # 4 - Status characteristic
        self.add_characteristic(DataOutputCharacteristic(self, STATUS_CHARACTERISTIC_UUID, ["notify", "read", "write", "write-without-response"]))
    
class DataCharacteristic(Characteristic):
    def __init__(self, service, uid, flags):
        Characteristic.__init__(self, uid, flags, service)
        
        # Not sure if this is useful
        # self.add_descriptor(DataDescriptor(self))

        self.data_value = []
        self.full_body = []
        self.write_mode = False
        self.notifying = False

    def ReadValue(self, options):
        return self.data_value

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        print("Started notifying...")

        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": self.data_value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.WriteValue(self.data_value))

    def StopNotify(self):
        self.notifying = False
        print("Stopped notifying...")

class CommandsCharacteristic(Characteristic):
    def __init__(self, service, uid, flags):
        Characteristic.__init__(self, uid, flags, service)

    def ReadValue(self, options):
        return self.data_value
    
    def WriteValue(self, value, options):
        try:
            input_data = ''.join([chr(b) for b in value])
            print(input_data)
            cmdStr = input_data
            cmd = Command(cmdStr, [], data="", svc=svc)
            exec = cmd.run()
            if exec:
                print('Command OK')
                value = exec.encode()
            self.data_value = value
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": self.data_value}, [])
        except:
            pass
        return self.data_value
        

class GameInfoCharacteristic(Characteristic):
    def __init__(self, service, uid, flags):
        Characteristic.__init__(self, uid, flags, service)

        self.notifying = False
        self.data_value = []
        for c in "NoGame":
            self.data_value.append(dbus.Byte(c.encode()))

    def ReadValue(self, options):
        return self.data_value
    
    def WriteValue(self, value, options):
        try:
            self.data_value = []
            input_data = ''.join([chr(b) for b in value])
            print("Game info received...")
            for c in input_data:
                self.data_value.append(dbus.Byte(c.encode()))
            if self.notifying:
                self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": self.data_value}, [])
        except:
            pass
        return self.data_value
    
    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        print("Started notifying...")

    def StopNotify(self):
        self.notifying = False
        print("Stopped notifying...")

class DataOutputCharacteristic(Characteristic):
    def __init__(self, service, uid, flags):
        Characteristic.__init__(self, uid, flags, service)

        self.notifying = False
        self.data_value = []

    def ReadValue(self, options={'mtu': 512}):
        return self.data_value
    
    def WriteValue(self, value, options={'mtu': 512}):
        try:
            self.data_value = []
            input_data = ''.join([chr(b) for b in value])
            print("Output data received...")
            for c in input_data:
                self.data_value.append(dbus.Byte(c.encode()))
            if self.notifying:
                self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": self.data_value}, [])
        except:
            pass
        return self.data_value
    
    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        print("Started notifying...")

    def StopNotify(self):
        self.notifying = False
        print("Stopped notifying...")

class DataDescriptor(Descriptor):
    DATA_DESCRIPTOR_UUID = "2901"
    DATA_DESCRIPTOR_VALUE = "Data Characteristic"

    def __init__(self, characteristic):
        Descriptor.__init__(self, self.DATA_DESCRIPTOR_UUID, ["read"], characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.DATA_DESCRIPTOR_VALUE
        for c in desc:
            value.append(dbus.Byte(c.encode()))
        return value

    def WriteValue(self, value, options):
        try:
            input_data = ''.join([chr(b) for b in value])
            in_type = input_data[:3]
            param = input_data[4:]
            print(in_type)
            print(param)
        except:
            pass

app = Application()
svc = SimpleBLEService(0)
app.add_service(svc)
app.register()

adv = SimpleBLEAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()

