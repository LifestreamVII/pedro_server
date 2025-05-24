import dbus

def encode_str(string):
    # length = len(string)
    # a = []
    # b = []
    # for i in range(0, length):
    #     a.append(dbus.Byte(ord(string[i])))
    #     b.append(string[i])
    #     string = dbus.Array(a, signature=dbus.Signature('y'))
    value = []
    for c in string:
        value.append(dbus.Byte(c.encode()))
    return value
