from fileio import rFile

def recv(offset, file='data.txt', trim=False):
    if int(offset) or int(offset) == 0:
        data = rFile(file)
        if data:
            if trim:
                data = ''.join(data.splitlines()).strip()
            if int(offset) > len(data):
                offset = len(data)
            return data[int(offset):]
        else:
            raise ValueError(f'Error: No data')

    return False