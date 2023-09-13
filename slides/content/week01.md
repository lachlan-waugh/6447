---
title: "week01"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 1[68]:05

---

{{< slide class="center" >}}
# Tooling Setup
### 6447 week01

---

{{% section %}}

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

![](../assets/img/week01/sus.png)

{{% /section %}}

---

{{% section %}}

## > whoami

* Lachlan
* CompSci (Security) / Maths
* 4th year 👴

---

## how to contact me

* lachlan.waugh@student.unsw.edu.au
* [@melon]() on the SecEdu Slack
* [@melon]() on the SecSoc Discord

---

## places for course discussion

* [seceduau.slack.com/signup](https://seceduau.slack.com/signup)
    * #cs6447
    * #cs6447-22t2-t16a

{{% /section %}}

---

## > whoareu

{{% section %}}

![](../assets/img/week01/icebreaker.jpg)

---

* Your name, degree, year?
* Why'd you do the course?
* What has been your favourite course so far
* Fun fact?
* ~~Your credit card number and the 3 wacky digits on the back~~

{{% /section %}}

---

{{% section %}}

## Course content
* Wargames (30%)
* Fuzzer (30%)
* Final (40%)

---

## Wargames
* don't leave them to the last minute, you'll be sad :(

* **flag != full marks**, you need to submit:
    * The script you used to get it
    * An explanation: your process/the vulnerability

* you probably won't get all the flags

* cool to collaborate/work together, but your flags and scripts/explanations need to be different.

{{% /section %}}

---

## tooling setup
* pwntools
* gdb/pwndbg
* binary-ninja

---

{{% section %}}

## binary-ninja

{{% /section %}}

---

{{% section %}}

## gdb


---

{{% /section %}}

---

{{% section %}}

## pwntools
a python library to interact with binaries (remotely?)

---

## connecting to a program
you interact as if it were a python object

```python
from pwn import *

p = remote('abc.com', 1234) # connect to a remote server
p = process('./vuln')       # or run a local binary

# do stuff with the binary

pause()         #  

p.interactive() # drops you into an interactive shell
p.close()       # oh man, idk
```

---

## sending & receiving data
how do we interact with the program?

```python
p.recvuntil(until)           # read input from p until 'line'
p.sendline(line)             # sends the line to the program
p.sendlineafter(until, line) # combines recvuntil() and sendline()
```

---

## packing data
binaries like ints & bytes, not strings

```python
p32(0x12345678)          # packs a 32-bit hex number (b'\x78\x56\x34\x12')
u32(b'\x78\x56\x34\x12') # unpacks a 32-bit (little-endian) number.
hex(x)           #
bytes(x)         #
int(x, 16)
f''.encode()    #
b''.decode()    # 
```

---

## access the binaries data
how do I grab the function pointers automatically?

```python
p = process('./program')
e = ELF('./program')
e = p.elf

e.symbols['win']   # get the address of "function_name"
e.got['printf']    # dw about this yet
e.address = 0x1234 # set the binary base address (for aslr)
```

---

## debugging with gdb
you can launch gdb from within pwntools to debug

```python
# https://docs.pwntools.com/en/stable/gdb.html
context.arch = 'i386'
context.terminal = ['urxvt', '-e', 'sh', '-c']

gdb_command = '''
    break *main
    si
'''

gdb.attach(p, cmd)        # attach to an existing process
gdb.debug('./vuln', cmd)  # spin up a debugger process, stopped at the first instruction
```

if the window it spawns is ugly a hell, check out [this](https://waugh.zip/6447/resources/Xresources)

{{% /section %}}

---

## lab
* set up your tooling
	* pwntools
	* pwndbg
	* binaryninja
* sort out groups for the fuzzer.

---

# Walkthrough
