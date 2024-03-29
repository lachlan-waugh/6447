---
title: "Week10"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05

---

{{< slide class="center" >}}
# Week10
### T1[68]A COMP6447 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

## My Experience

How'd you find the course
* What'd you like
* What'd you dislike
* What can be improved

> [https://myexperience.unsw.edu.au](https://myexperience.unsw.edu.au)

---

{{% section %}}
## iOS Hacking

---

## demo
> anyone have an iPhone I can hack?

---

## jk
{{% /section %}}

---

## Final exam
`3` section (each worth `33%`)
* `pwn`
* `reversing`
* `source auditing`

> each has `3-4` challenges

---

## tips
{{% section %}}

### general
* Practice, practice, practice
    * Time pressure makes the exam suck
    * You've seen this from the midterm
* You should be able to solve all wargames in `<20` minutes by now (minus heap lol)
* it won't just be stuff we've covered (think of image-viewer)

---

### pwn
* not all challenges are a single vulnerability
    * e.g. could be format string -> shellcode (midterm3)
* not everything is `gets()` and `printf()`
    * e.g. `strcpy()`, `syslog()`

---

### re
* focus on **making the code make sense**
    * use meaningful variable names
    * try to make it legible/clean (pls)
* don't read everything: focus on important stuff
    * look at function calls, loops
    * build the fundamentals, then fill in details

---

### src
* consider the impact
    * don't post every single bug
    * include only meaningful **vulnerabilities**
* explain the bugs: **why they're vulnerable**
* not all vulnerabilities exist in isolation

{{% /section %}}

---

## Revision
{{% section %}}
### how2hack
* Buffer overflows
* Shellcode
* Return-oriented programming
* Format strings
* Heap

---

### Buffer overflows
1. abusing functions which allow arbitrary length input to static length buffers
2. the stack stores data (local variables) and control (return address, stored EBP)

> 1+2 = bad

---

### Buffer overflow mitigations
| protection     | bypassing it          |
| -------------- | --------------------- |
| stack canaries | guess it/leak it      |
| ASLR/PIE       | leak a binary pointer |

---

### Shellcode
* with buffer overflows, we can control where the program execution goes, but where do we point it?
* we can write shellcode on the stack, and jump into it

we can use syscalls:
* `read('./flag')`,
* `execve('/bin/sh')`

---

### shellcode mitigations
| protection     | bypassing it |
| -------------- | ------------ |
| small buffers  | egg hunters  |
| NX             | write it somewhere else |
| where payload? | NOPSled      |

---

### Return-oriented programming
* we can't write our own shellcode, but we can use existing instructions from the binary/libc
* instructions are multi-byte, so we can jump into some offset into one and get a different one

*bypasses NX as we aren't writing our own instructions*

---

### rop mitigations
| protection | bypassing it |
| --- | ------------- |
| PAC | idk, PACMAN? |
| where payload? | RETSled      |

---

### Format strings

---

### fstring mitigations
| protection                    | bypassing it |
| ----------------------------- | --- |
| grep -r "printf([^\'\`\"]" .  | cry |

---


### Heap
you probably shouldn't need a recap (im lazy)

---

### Memory protections
* *ASLR*: system-wide address randomization
* *PIE*: program specific address randomization
* *RELRO*: prevents overwriting GOT memory
* *NX*: writable regions aren't executable `W^X`

---

### RELRO
* *None*: trivial, overwrite anything
* *Partial*: overwrite an unitiliased entry
* *Full*: overwrite a hook (e.g. `__malloc`/`__free`)

[more here](https://ctf101.org/binary-exploitation/relocation-read-only/)

{{% /section %}}

---

## ~~Tutorial~~

---

## Now you
* wargames: harder ROP (trivial tho)
* [2021 exam](2021.exam.comp6447.wtf)