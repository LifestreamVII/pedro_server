import time
import subprocess
import asyncio
import os

class GameCard:
    def __init__(self):
        self.type = "UNKNOWN"

    async def readInfo(self, cmd: str):
        with open('output.txt', 'w') as f:
            detected_game = "None"
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE
            )

            stdout, stderr = await proc.communicate()
            print(f'[{cmd!r} exited with {proc.returncode}]')
            if stdout:
                print(f'[stdout]\n{stdout.decode()}')
                f.write(stdout.decode('utf-8'))
                for line in stdout.decode('utf-8').splitlines():
                  if line.startswith("Detected game"):
                    detected_game = line
                    break
            if stderr:
                print(f'[stderr]\n{stderr.decode()}')
                f.write(stderr.decode())
        return detected_game

    def decryptSaveFile(self, args):
        with open('output.txt', 'w') as f:
            subprocess.Popen(args, stdout=f, stderr=f, universal_newlines=True)
            # while True:
            #     line = str(proc.stdout.read(100))
            #     if not line:
            #         break
            #     print(f'[stdout]\n{line}')
            #     f.write(line)
        return True

    def decryptPkmFile(self, cmd: str):
        with open('decrypted.txt', 'w') as f:
            subprocess.Popen(args, stdout=f, stderr=f, universal_newlines=True)
            # while True:
            #     line = str(proc.stdout.read(100))
            #     if not line:
            #         break
            #     print(f'[stdout]\n{line}')
            #     f.write(line)
        return True
    
    def writeSaveFile(self, args):
        with open('output.txt', 'w') as f:
            proc = subprocess.Popen(args, stdout=f, stderr=f, universal_newlines=True)
            proc.wait()  # Wait for the subprocess to exit
            # Run another subprocess with the same command
            task = self.uploadSave()
            print("Game card savedata write task started.")
            return task

    def downloadSave(self):
        if os.path.exists("progress.txt"):
            os.remove("progress.txt")
        else:
            print("The file does not exist")
            
        with open('progress.txt', 'a+') as f:
            subprocess.Popen(args=['./005tools', 'download', 'savefile.sav', '--save-size=524288'], stdout=f, stderr=f, universal_newlines=True)
            # while True:
            #     line = str(proc.stdout.read(100))
            #     if not line:
            #         break
            #     print(f'[stdout]\n{line}')
            #     f.write(line)
        return True
    
    def uploadSave(self):        
        if os.path.exists("progress.txt"):
            os.remove("progress.txt")
        else:
            print("The file does not exist")
            
        with open('progress.txt', 'a+') as f:
            subprocess.Popen(args=['./005tools', 'upload', 'savefile.sav', '--save-size=524288'], stdout=f, stderr=f, universal_newlines=True)
            # while True:
            #     line = str(proc.stdout.read(100))
            #     if not line:
            #         break
            #     print(f'[stdout]\n{line}')
            #     f.write(line)
        return True

    def read(self):
        print("Reading game card...")
        res = asyncio.run(self.readInfo('./005tools info'))
        print("Game card read.")
        print(res)
        return res
    
    def write(self, genFlag, boxFlag):
        print("Writing game card...")
        task = self.writeSaveFile(['/opt/dotnet/dotnet', 'run', 'writesave', 'savefile.sav', 'pkm', genFlag, boxFlag])
        print("Game card savedata write task started.")
        return task

    def download(self):
        print("Downloading game card save...")
        task = self.downloadSave()
        print("Game card savedata read task started.")
        return task
    
    def decode(self, genFlag):
        print("Decoding PKM file...")
        task = self.decryptPkmFile(['/opt/dotnet/dotnet', 'run', 'decpkm', 'pkm', genFlag])
        return task
    
    def decrypt(self):
        print("Decrypting savefile of game card...")
        task = self.decryptSaveFile(['/opt/dotnet/dotnet', 'run', 'readsave', 'savefile.sav'])
        return task
