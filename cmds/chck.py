from fileio import rFile
from hashlib import sha256

def chck(hash):
    print(hash) 
    if hash:
        data = rFile('data.txt')
        if data:
            sha = sha256(data.encode('utf-8')).hexdigest()
            if sha == hash:
                return "CHCK_OK"
            else:
                return "CHCK_BAD"
        else:
            raise ValueError(f'Error: No data')

    return False