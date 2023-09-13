---
title: "week01: introduction"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 18:05

---

{{< slide class="center" >}}
# course intro + background
## COMP6447 Week01

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

# course introduction

---

{{% section %}}

## contact hours
* lectures - 2 hours
* tutorials - 2 hours

> maybe less than you're used to

---

## lectures
* lectures are streamed online && recorded
* small intermission for questions
* stop me anytime throughout for questions

&nbsp;

#### an aside
* please come in person
* ~~recordings won't get released if attendance is low~~
* this lecture hall already looks like a dungeon, don't let us here alone

---

## tutorials
* *hour 1*: more depth into lecture content, and demonstrations/walkthroughs of techniques
* *hour 2*: you give the challenges (e.g. tutorial demos/wargames) a try
    * there are separate (easier) tutorial challenges

> this week: tooling setup

---

## self-learning
A lot of hard/niche content in this course

* We cover the fundamentals.
* Burden is on you to experiment with techniques.
    * All advanced exploitation techniques are based on the fundamentals we teach
    * But it will require more depth of understanding than we go into

---

## how to contact us
* discord [TODO: link]() ~/SECURITY/comp6447
* contact your tutor
* cs6447@cse.unsw.edu.au (personal stuff)
* ~~ask adam directly~~

> please come with a good question

{{% /section %}}

---

{{% section %}}

# assessments
* Weekly Wargames (30%)
* Fuzzer Assignment (30%)
* Final Exam (40%)

---

## wargames
* 2 - 6 challenges per week
    * made up of pwn, re, and src (more on this later)
    * mostly pwn (but, this requires skills in the others)
* submit the flags and writeup for each challenge
* *wargame 6 is under exam conditions*

> should be on CTFd soon&trade;

---

## final exam
* very similar to the weekly wargames
* *under time pressure*
    * plsplspls prepare for this
* in the final, pwn, src and re are weighted equally

---

## fuzzer assignment
* group assignment
* 3 - 4 people per group
* really fun, open-ended project
* more on this later (comes out ~ week5)

{{% /section %}}

---

{{% section %}}

# course content
what do you actually do

---

## three major parts 
* source code auditing (src)
* reverse engineering (re)
* binary exploitation (pwn)

> and fuzzing, kinda

---

### source code auditing
* examining the source code of an application to find any bugs, errors, vulnerabilities
* sounds simple, but can be very difficult
    * what if the application has many code paths
    * what if it's a multi-file application
    * what if it uses a bunch of libraries

---

### reverse engineering
deconstructing a program to work out it’s underlying code, architecture, design, etc
* reading the source code without being given it
* if you want to get started early, check out [this](https://0xinfection.github.io/reversing/)

---

### two main types
* *static*:  examine an executable without executing it (disassembling)
* *dynamic*: examine an executable by .... executing it (debugging)

---

### binary exploitation
the good stuff

* tricking a binary file to do what you want
    * read/write a file
    * pop a shell?

{{% /section %}}

---

{{% section %}}

# tips to succeed
how to get good mark

---

### wheres the bug?
[link](assets/code/large.md)

```C
#include <stdio.h>
#include <stddef.h>

#define NAME_LEN 64;

typedef struct user {
    char name[NAME_LEN];
    int level;
} user_t;

user_t users[100];
int n_users;
int current_user;

int logged_in() {
    return (current_user != -1);
}

int create_user() {
    if (n_users == 100) {
        fprintf(stderr, "nah, too many users already. cya");
        return -1;
    }

    int level;
    printf("whats your level?");
    scanf("%d", &level);
    if (level == 0) {
        fprintf(stderr, "haha no");
        return -1;
    }

    users[n_users].level = level;

    printf("whats your name?");
    fgets(users[n_users].name, 65, stdin);

    current_user = n_users;
    ++n_users;
}

int login() {
    if (logged_in()) {
        printf("nah\n");
        return 0;
    }

    char buffer[128];
    fgets(buffer, 128, stdin);
    for (int i = 0; i < n_users; ++i) {
        if (strcmp(buffer, users[i].name) == 0) {
            current_user = i;
            return 0;
        }
    }

    printf("user not found");
    return 0;
}

int logout() {
    if (logged_in()) {
        current_user = -1;
        printf("cya");
    }
}

int execute_command() {
    if (current_user >= 0 && users[current_user].level == 0) {
        printf("welcome admin!");
        system("/bin/sh");
    }

    printf("you aren't authorized to do that\n");
    return 1;
}

void menu() {
    puts("available commands");
    puts("\t[L]ogin");
    puts("\t[C]reate user");
    puts("\t[M]Logout");
    puts("\t[R]un command");
    puts("\t[Q]uit");
}

int main(void) {
    current_user = -1;
    while (1) {
        menu();
        printf("$> ")

        switch(getchar()) {
            case "L":
                login();
                break;
            case "C":
                create_user();
                break;
            case "M":
                logout();
                break;
            case "R":
                execute_command();
            case "Q":
                exit(1);
            default:
                printf("????");
                return 0;
        }
    }
}
```

---

### how about now?
[link](assets/code/medium.md)

```C
#define NAME_LEN 64;

typedef struct user {
    char name[NAME_LEN];
    int level;
} user_t;

int create_user() {
    if (n_users == 100) {
        fprintf(stderr, "nah, too many users already. cya");
        return -1;
    }

    int level;
    printf("whats your level?");
    scanf("%d", &level);
    if (level == 0) {
        fprintf(stderr, "haha no");
        return -1;
    }

    users[n_users].level = level;

    printf("whats your name?");
    fgets(users[n_users].name, 65, stdin);

    current_user = n_users;
    ++n_users;
}
```

---

### how about now?

```C
#define NAME_LEN 64;

typedef struct user {
    char name[NAME_LEN];
    int level;
} user_t;

int create_user() {
    // boring
    fgets(users[n_users].name, 65, stdin);
    // boring
}
```

---

### if nobody got it
* there's a one byte overflow in the users field
* you can overflow the level field of the user
* e.g. change your level to admin or something

---

### whats your point
* there's a lot of garbage 
    * verbose tooling output
    * assembly instructions
    * random imported functions

> most of it isn't important, pay attention to what is

---

### don't fall behind
* each weeks content will build on the previous weeks
* if you don't understand the fundamentals of a previous topic, it's hard to learn the next topic 

---

### basic course structure
| week02     | buffer overflows                                |
|------------|-------------------------------------------------|
| week03     | shellcode && stack canaries                     |
| week04     | format strings                                  |
| week05     | return-oriented programming                     |
| week07     | heap (uaf, double free)                         |
| week8/9/10 | further techniques (e.g. defeating mitigations) |

---

### get started early
* there's some fantastic resources online you can utilize if you wanted to get ahead
    * [binary exploitation](https://www.youtube.com/watch?v=iyAyN3GFM7A&list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN) - LiveOverflow
    * [developing a fuzzer](https://www.youtube.com/watch?v=TLa2VqcGGEQ&list=PLhixgUqwRTjy0gMuT4C3bmjeZjuNQyqdx) - LiveOverflow
    * [reverse engineering](https://0xinfection.github.io/reversing/) - 0xinfection
    * [protostar challenges](https://exploit.education/phoenix/) - exploit.education

{{% /section %}}

---

{{% section %}}

# Exploitation

---

## terminology
* bug – A programming error or oversight that can be triggered to produce incorrect results, or cause it to behave in unintended ways
* threat - A person or group able to do harm or performing some hostile action

---

## more terminology
* vulnerability – A software or system weakness which allows the system to be used in a manner which would be considered a breach of the intended or extended result.
* exploit – A tool or code created to exploit one or more vulnerabilities for some purpose. In reality, good exploits for some vulnerabilities take weeks or months of
high-skill development

---

## types of vulnerabilities
* design vulnerabilities
    * major mistakes at a high level, ie: how components interact with each other, ie: wifi deauth
    * hard to fix, require total rewrites

* implementation vulnerabilities
    * minor mistakes in implementation (off by one errors, forgetting to seed rand())
    * software engineers making mistakes, misreading documentation, etc

---

## where to find them
* *file formats*: Exploits in complex file formats which are decoded by complex software, ie: videos, images

* *remote*: exploits that can compromise a system over a network ie: web server, ssh, etc

* *client side*: ie: web browser

* *local (privesc)*: exploiting software running as a higher privilege on the same machine. ie: kernel

---

## mitigations 
why we teach old stuff

Modern computers have a lot of exploit mitigations.
* We start by learning the basics (stuff that wouldn't work anymore)
* more tech makes it harder/impossible to get reliable (or any) exploits
getreliable, and sometimes they even make it impossible
* we disable these mitigations, then slowly enable them to teach you how to bypass them

---

## finding bugs IRL
*vulnerabilities*
* public (full) disclose
* coordinated (“responsible”) vendor disclosure
* (responsible) non-disclosure

*exploits*:
* simple PoC, public disclose (ie: metasploit)
* decent - commercial exploit pack (ie: celebrite)
* great - fame, $$$

> good intentions won't keep you safe

---

## when might I use this
* *penetration testing*: brief assessments of a particular product or environment - frequently based on network scanning and/or analysis of a web or mobile app
* *red teaming*: more in-depth, open ended penetration testing - without a limited scope but often with an objective - i.e. compromise any web servers or employees of XYZ company 
* *vulnerability research*: not focused on implementation or deployment of a technology - focused on the actual technology itself - i.e. finding vulnerabilities in the a library

{{% /section %}}

---

{{% section %}}

# why is this important
why are we attacking C programs lol

{{% /section %}}

---

{{% section %}}

# memory fundamentals

---

## what are people's backgrounds?
* who's done operating systems? COMP3231/COMP3891
* who's done web apps? COMP6[84]45
* who's done the intro to security? COMP6[84]41

---

## conceptualising memory
at a low level, CPUs see a long strip of bytes
* Memory is just a range of values CPUs can access
* CPUs have a few registers for super duper fast access, but these are really
small and not considered part of memory
![](../lecture01/assets/img/stack1d.png)

---

## visualising memory
RAM is 1D. But thinking about it in 2d can be useful.
* Memory is often not accessed 1 byte at a time.
* We care about data structures, not bytes

![](../lecture01/assets/img/stack32-2d.png)
![](../lecture01/assets/img/stack64-2d.png)
![](../lecture01/assets/img/address.png)

---

## data types in memory
C and C++ use a bunch of several core types to do work. But all of them are just integers of various sizes.

* char; 1 byte
* short: 2 bytes or more
* int: normally 4 bytes
* long: at least 4 bytes, at least as long as int
* pointers: normally 4 bytes, or 8 depending on architecture (just spicy ints)
* structs: a sequence of different variations of above types

---

## signedness
how is a negative number stored in memory?
* basically flip the bits and add 1
* this could mean a really big number in memory, is actually a very small negative one

> how could this result in vulnerabilities?

---

## pointers
Pointers aren’t special or magic.

> Pointers are just another integer, where the value is the address of something else

---

## endianness
Each architecture has Endianness
* Big or little endian (MIPS, PowerPC vs x86)
* x86 is little endian
* Some architectures let you pick/switch the endianness during runtime (ARM)
* Little endian is more prevalent for reasons (laziness)
    *  Used to be “wrong-endian” (you can be a bit more dodgy with your types and things wouldn’t break)
* Endianness only applies to memory. Not to registers

---

## endianness
![](../lecture01/assets/img/endian.png)

---

## address space layout
We only worry about virtual addresses
* Virtual Address Spaces are split into regions
* Each segment has set permissions
* .text (code) usually r-x
    * .data (global variables) usually rw-
    * .rodata (constants) usually r–

![](../lecture01/assets/img/addressspace.png)

{{% /section %}}

---

{{% section %}}

# other knowledge
background stuff you should know for the course

---

# linux fundamentals

---

## the command line
what is a shell?

![](../lecture01/assets/img/shell.png)
> soo spooky, no gui ahh

---

## linux fundamentals
* does anyone know what "popping a shell means?"
* what can you do once you pop a shell?

---

## essentially
* escaping the sandbox of the application, into the server
* you can start executing commands on the server

---

## shell command deep dive
all you'll need to know to be l33t

> `cat flag`

---

## scripting
* how many people have written a script before
* what about used python for further purposes
* our usage of python will be very basic

---

## pwntools
basic usage

```python
from pwn import *

r = remote('vulnserver.xyz', 1234)  #
p = process('./vuln')               #
e = p.elf

p.recvuntil(b'some text the program outputs')
p.sendline(b'AAAAAAAAAAAAAAAAAAAAA')

p.interactive() # drops you into an interactive shell
p.close()       # oh man, idk
```

--- 

{{% /section %}}

---

{{% section %}}

## how is this relevant, I only write python code

---

### abstraction is cringe
* many people don't really understand

---

## Cloudbleed
* basically a buffer overflow

---

## Zenbleed
* very similar idea to a use-after-free

[read more here](https://lock.cmpxchg8b.com/zenbleed.html)

---

```
    vcvtsi2s{s,d}   xmm, xmm, r64
    vmovdqa         ymm, ymm
    jcc             overzero
    vzeroupper
overzero:
    nop
```

---

## phone phreaking


---

{{% /section %}}

