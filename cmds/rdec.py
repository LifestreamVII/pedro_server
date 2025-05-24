from fileio import rFile

def rdec(kw):
    offset = 0
    print(kw)
    if kw == "TRAINER":
        data = rFile("trainer.txt")
    elif "BOX" in kw:
        index = kw[3:]
        data = rFile(f"box{index}.txt")
    if data:
        data = ''.join(data.splitlines()).strip()
        if int(offset) > len(data):
            offset = len(data)
        return data[int(offset):]
    else:
        raise ValueError(f'Error: No data')