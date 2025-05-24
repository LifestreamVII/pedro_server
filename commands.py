from cmds.send import send
from cmds.chck import chck
from cmds.recv import recv
from cmds.rdec import rdec
from cmds.game import GameCard
from cmds.progress import detect_percentage
from threading import Thread
import time
from fileio import rFile, wFile
import subprocess
import asyncio
import os
import base64

class Command:
    def __init__(self, command_string, then, data=None, char=None, svc=None, *args):
        self.command_string = command_string
        self.then = then
        self.args = args
        self.data = data
        self.task = None
        self.char = char
        self.svc = svc
        self.max_chunk = 500 # bytes
        # for a 512kb save transfer to be completed in 1 minute with 500 bytes chunks, there should be (roughly) a maximum delay of 50 ms between each write operation

    def readGame(self):
        detected_game = "None"
        process = subprocess.Popen(['./005tools', 'info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stdout:
            for line in stdout.decode().split('\n'):
                if "Detected game" in line:
                    print(line)
                    detected_game = line
                    break
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')
        time.sleep(4)
        self.svc.get_characteristics()[1].WriteValue(detected_game.encode(), {})
        print(detected_game)
        return detected_game
    
    def readSaveFile(self):
        # prevent repeated call / check if download process is running
        process = subprocess.Popen(['./005tools', 'download', 'savefile.sav', '--save-size=524288'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # stdout, stderr = process.communicate()
        line = 'e'
        perc = 0
        while True:
            if not line:
                break
            line = process.stdout.readline()
            print(line)
            if "%" in str(line):
                if "100%" in line:
                    self.svc.get_characteristics()[4].WriteValue(line.encode(), {})
                    break
                if perc is not int(line.split("%")[0]):
                    self.svc.get_characteristics()[4].WriteValue((str(perc)+"%").encode(), {})
                    perc = int(line.split("%")[0])
                    print(f'[stdout]\n{line}')
        
        if process.stderr and not process.returncode == 0:
            # File "/home/lois/ble-new/commands.py", line 58, in readSaveFile
            # print(f'[stderr]\n{process.stderr.decode()}')
            # AttributeError: '_io.TextIOWrapper' object has no attribute 'decode'
            print(f'[stderr]\n{process.stderr.read()}')

        print("Save file read.")
        # this has to be a separate function for reusability
        # GETDAT command will read the output.txt file and write to DATA channels
        with open('output.txt', 'w') as f:
            with open('savefile.sav', 'rb') as save_file:
                encoded_content = base64.b64encode(save_file.read()).decode('utf-8')
                # f.write(encoded_content)
        self.svc.get_characteristics()[4].WriteValue("READY_SAV".encode(), {})
        return "READY_SAV"
    
    def readOutputData(self, offset):
        with open('output.txt', 'r') as f:
            channel = int(offset[-1])
            offset = int(offset[:-1])
            f.seek(offset)
            chunk = f.read(self.max_chunk)
            if chunk:
                self.svc.get_characteristics()[channel].WriteValue(chunk.encode(), {'mtu': 512})
        return "GETDAT_OK"

    def run(self):
        if self.command_string == 'SEND':  # Connected Bluetooth device wants to send data
            return send("data.txt")
        elif self.command_string == 'RECV':  # Connected Bluetooth device wants to receive data
            return recv(self.data, 'data.txt', trim=False)
        elif self.command_string == 'DONE':  # Transfer done
            pass
        elif self.command_string == 'REST':  # Reset the process
            pass
        elif self.command_string == 'CHCK':  # Check sent hash with calculated hash of data
            return chck(self.data)
        elif self.command_string == 'VOID':  # Do nothing
            pass
        elif self.command_string == 'GCINFO':  # Info from game card
            # gc = GameCard()
            # gamename = gc.read()
            # time.sleep(2)
            t = Thread(target=self.readGame)
            t.start()
            print("Game card read.")
            return "GCINFO_OK"
        elif self.command_string == 'WNFC':  # Write new contents to NFC tag
            pass
        elif self.command_string == 'RNFC':  # Read contents from NFC tag
            pass
        elif self.command_string == 'GETSAV':  # Read save file from game card
            t = Thread(target=self.readSaveFile)
            t.start()
            print("Game card read.")
            return "GETSAV_OK"
        elif 'GETDAT' in self.command_string:  # Read data (write output.txt to DATA1 and DATA2)
            offset = self.command_string.split('GETDAT(')[1].split(')')[0]
            t = Thread(target=self.readOutputData, args=[offset])
            t.start()
            print("Get data.")
            return "GETDAT_OK"
        elif self.command_string == 'DSAV':  # Decrypt save data from game card
            gc = GameCard()
            task = gc.decrypt()
            self.task = task
            t = Thread(target=detect_percentage, args=(self.char, 'output.txt'))
            t.start()
            return "DSAV_OK"
        elif self.command_string == 'DPKM':  # Decrypt save data from game card
            gc = GameCard()
            d = rFile('data.txt').split(",")
            wFile('pkm', d[0], 'overwrite')
            task = gc.decode(d[1])
            self.task = task
            t = Thread(target=detect_percentage, args=(self.char, 'decrypted.txt'))
            t.start()
            return "DPKM_OK"
        elif self.command_string == 'RDEC':  # Read the decrypted data text output
            return rdec(self.data)
        elif self.command_string == 'WSAV':  # Write save file to game card
            gc = GameCard()
            d = rFile('data.txt').split(",")
            wFile('pkm', d[0], 'overwrite')
            task = gc.write(d[1], d[2])
            self.task = task
            t = Thread(target=detect_percentage, args=(self.char, 'progress.txt'))
            t.start()
            return 'WSAV_OK'
        elif self.command_string == 'DOWN':  # Restart BT daemon + BT server
            pass
        else:
            raise ValueError(f'Invalid command: {self.command_string}')

    def do_then(self):
        self.command_string = self.then
        return self.run()
