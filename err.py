from some_module import function1
from another_module import function2

class Err:
    def __init__(self, command_string, then, *args):
        self.command_string = command_string
        self.then = then
        self.args = args

    def run(self):
        match self.command_string:
            case 'SEND': # Connected Bluetooth device wants to send data
                return function1(*self.args)
            case 'RECV': # Connected Bluetooth device wants to receive data
                return function2(*self.args)
            case 'DONE': # Transfer done
                return function2(*self.args)
            case 'REST': # Reset the process
                return function2(*self.args)
            case 'CHCK': # Check sent hash with calculated hash of data
                return function2(*self.args)
            case 'VOID': # Do nothing
                return function2(*self.args)
            case 'WNFC': # Write new contents to NFC tag
                return function2(*self.args)
            case 'RNFC': # Read contents from NFC tag
                return function2(*self.args)
            case _:
                raise ValueError(f'Invalid command: {self.command_string}')
        
    def do_then(self):
        self.command_string = self.then
        return self.run()