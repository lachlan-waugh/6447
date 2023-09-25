---
title: "01: intro"
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

---

## how to contact me

* lachlan.waugh@student.unsw.edu.au
* [@melon]() on the SecEdu Slack
* [@melon]() on the SecSoc Discord

---

## places for course discussion
* probably the discord mostly
* used to be secedu slack but it is :zombie:
* I will be more responsive on discord than email

---

## where to access resources
* [waugh.zip/6447](https://waugh.zip/6447)
* tutorials may be recorded, idk yet

{{% /section %}}

---

## > whoareu

{{% section %}}

![](../assets/img/week01/icebreaker.jpg)

---

* your name, degree, year?
* why'd you do the course?
* what has been your favourite course so far
* have you done a security course before (644[135])?
* ~~Your credit card number and the 3 wacky digits on the back~~

{{% /section %}}

---

{{% section %}}

## Course content
* wargames (30%)
* fuzzer (30%)
* final (40%)

---

## wargames

* **flag != full marks**, you need to submit:
    * the script you used to get it
    * an explanation: your process/the vulnerability

---

## notes on wargames
* don't leave them to the last minute, you'll be sad :(
* you probably won't get all the flags
* cool to collaborate/work together, but your flags and scripts/explanations need to be different.

---

## fuzzer
* group assignment
* there's also a midpoint submission

{{% /section %}}

---

{{% section %}}

## pointers
![](../assets/img/week01/pointers.png)

---

## pointer arrays
![](../assets/img/week01/pointer.png)

{{% /section %}}

---

## tooling setup
* binary-ninja
* gdb/pwndbg
* pwntools

---

{{% section %}}

## binary-ninja
attempts to reconstruct the source code

---

## the most important things
right-click >

* rename variable
* display as
* create structure
* change type
* highlight instruction

---

## displaying the information
there's multiple ways to display the information

* pseudo-C
* high-level IL
* disassembly
* graph view

---

## demos
* [binja1](/demos/my-first-program)
* [binja2](/demos/my-second-program)

{{% /section %}}

---

{{% section %}}

## gdb / pwndbg
allows you to modify the binary during execution

---

## pwndbg 
* a nice plugin for gdb
* makes the terrible syntax less terrible
* really easy to install just go [here](https://github.com/pwndbg/pwndbg)

---

## debugging a process 
how to get started

```bash
att 1234          # attach to running process 1234
b 0x1337          # break at address 1337
break *(main)     # break at the first instruction in main()
break *(main+12)  # break at the address 12 bytes after main
c                 # continue until next breakpoint/end program
si                # step by a single instruction
fin               # go until end of current function
```

---

## examining & modifying data
changing the flow of the application

```bash
x 0x1337        # examine at 0x1337
x/20wx 0x1337   # examine 20 words from 0x1337
x/s 0x1337      # examine string at 0x1337
set $reg=value  # set register = value ie: set $ebx=1
set *(int *)($ebp + 0xX)=value # set a local variable
jump *(0x1234)  # jump to 0x1234 (e.g. start executing there)
jump *(main)    # jump to main
```

---

## demos
* [gdb1](/demos/bad-check)
* [gdb2](/demos/ripper)

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
p.recvline()                 # reads one line from the process
p.recvuntil('line')          # read input from p until 'line'
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
	* gdb/pwndbg
	* binaryninja
* sort out groups for the fuzzer.

---

# walkthrough
