---
title: "9: more rop"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 1[68]:05

---

{{< slide class="center" >}}
# rop techniques & revision
### 6447 week9

---

## good faith policy

we expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

{{% section %}}

## doing more with rop

---

### calling functions
it's not just syscalls for `execve("/bin/sh")`

* *won't always be calling assembly instructions*
* generally you'll have access to many more functions
* probably won't get exactly what you want

> malloc, printf, mmap can all leverage other exploits

---

### www
write-what-where gadgets

* basically a write primitive as a gadget
    * register 1: the target address
    * register 2: the value to write

```php
mov [register1], register2
```

---

### using the stack
we can still use the stack to store stuff

* that's where our payload (padding) is
    * we can already write to it (most of the time)

```php
    mov eax, esp
    sub eax, 10
    mov ebx, eax
```

> not just mov (add, mul, push, xchg?)

{{% /section %}}

---

{{% section %}}

## stack pivots
my buffer is too small

---

### the problem
we can't get a full payload

* we have an overflowable buffer
* overflow isn't large enough for a full ROP payload

> think back to egghunters in shellcode

---

### the solution
* we could:
    * jump back earlier in the current buffer
    * jump into a bigger buffer (harder/better?)

> a.k.a we ~pivot the stack~

{{% /section %}}

---

{{% section %}}

### stack pivot example
```C
vuln(){
    char buff[16];
    fgets(buff,24,stdin);
}
```

> here, we only have enough room to overwrite a single address

---

### in memory
```
    [  XXXX  ] *we cannot write here*
    [  GDGT  ] <- stored return pointer
    [  AAAA  ] <- stored frame pointer
    [  AAAA  ] <- padding
    [  AAAA  ]
    [  AAAA  ]
    [  AAAA  ]
```

> we can overwrite the return address, but can only execute one instruction?

---

### stack pivot in action
`GADGET_1` = `sub esp, 24`

```
[ GADGET_1 ] <- ESP points here 
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[ GADGET_2 ] <- start of our payload 
```

> GADGET_1 gets invoked

---

### stack pivot in action
gadget moves ESP to point at the start of our payload

```
[ GADGET_1 ]
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[ GADGET_2 ] <- ESP points here 
```

---

### stack pivot in action
so put our ROPChain as our "padding"

```
[ GADGET_1 ] <- ESP points here 
[ GADGET_8 ] <- int 0x80
[ GADGET_7 ] <- xor esi, esi; ret
[ GADGET_5 ] <- xor edx, edx; ret
[ GADGET_4 ] <- mov ecx, 0x12345678; ret
[ GADGET_3 ] <- mov ebx, 0x12345678; ret
[ GADGET_2 ] <- mov eax, 11; ret
```

---

### other stack pivots
it could be the same buffer or another one

* if it's another buffer, you'll just need to move esp more
* or directly change it's value (with a leak maybe?)

{{% /section %}}

---

{{% section %}}

## stack-pivots (extreme!!)
* what if we only had a single byte overflow
* e.g. we overwrite one byte of EBP

```C
int vuln() {
    char buffer[100];
    fgets(buffer, 101, stdin);

    return 0;
}
```

> how2exploit?

---

### how realistic is this?
why is this vulnerable?

```C
int vuln(char *s) {
    char buffer[100];
    memset(buffer, 0, sizeof(buffer));
    strncat(buffer, s, sizeof(buffer));
    return 0;
}
```

---

### what is the bug?
these should be `sizeof(buffer) - 1`

```C
int vuln(char *s) {
    char buffer[100];
    //                vvvvvvvvvvvvvv
    memset(buffer, 0, sizeof(buffer));
    strncat(buffer, s, sizeof(buffer));
    //                 ^^^^^^^^^^^^^^
    return 0;
}
```

---

### how to exploit this?
its only one byte

```php
0xFFFF [ ABCD ] <- stored EIP
0xFFFC [ FFFF ] <- stored EBP
0xFFF8 [ AAAA ]
0xFFF4 [ AAAA ]
0xFFF0 [ AAAA ]
```

---

### leave and ret
what do leave and ret do?

```php
leave:
    mov esp, ebp    // esp = ebp
    pop ebp         // ebp = old_ebp

ret:
    pop eax         // eax = stored_eip
    call eax        // jump eax
```

---

### the overflow
overflow into least significant byte

```php
0xFFFF [ ABCD ]
0xFFFC [ FFF0 ] <- partial overwrite
0xFFF8 [ AAAA ]
0xFFF4 [ AAAA ]
0xFFF0 [ AAAA ]
```

---

### redirecting program flow
> once we leave, ESP points to `0xFFF0`
```php
0xFFFF [ ABCD ]
0xFFFC [ FFFF ]
0xFFF8 [ AAAA ]
0xFFF4 [ AAAA ]
0xFFF0 [ AAAA ] <- ESP points here (execution resumes here)
```

{{% /section %}}

---

{{% section %}}

## srop
sig-return oriented programming

---

### what is sigreturn
how kernel returns execution to program after signal

* when a signal is invoked, the context (e.g. registers) are all pushed to the stack

* the signal-handler may modify them, etc

* these values are restored using sigreturn (a syscall)

---

### so how could we exploit this
we fake a sigreturn

* sigreturn restores the values of registers **based** on content stored on the stack (we control the stack)

* what if we pushed our own fake "context" (register values) onto the stack, and triggerd a sigreturn?

* we could control all of the register values?

{{% /section %}}

---

## revision
need help?

* any content you want covered?

* any challenges you want me to demo?

---

## tutorial
