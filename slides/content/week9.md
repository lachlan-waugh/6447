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

* generally you'll have access to many more functions

---

### www
write-what-where gadgets

```php
mov <[register]>, <register>
```

---

### using the stack
we can still use the stack

* that's where our payload (padding) is
* doesn't have to be mov, what about add, mul, ???

```php
    mov eax, esp
    sub eax, 10
```

{{% /section %}}

---

## stack pivots
{{% section %}}

### the problem
* we have an overflowable buffer
* it's too small for a full ROP payload

> think back to shellcode egghunters

---

### the solution
* We could:
    * jump back earlier in the current buffer
    * jump into a bigger buffer (better/harder)

> a.k.a we ~pivot the stack~

{{% /section %}}

---

### stack pivot example
{{% section %}}

```C
vuln(){
    char buff[16];
    fgets(buff,24,stdin);
}
```

> here, we only have enough room to overwrite a single address

---

```
[  AAAA  ]
[  AAAA  ]
[  AAAA  ]
[  AAAA  ]
[  ARGS  ] <- Any stored args
[  EBP   ] <- Stored Frame Pointer
[  EIP   ] <- Stored Return Pointer
[  ????  ] <- We cant write here
```

> we can overwrite the return address, but can only execute one instruction?

---

> `GADGET_1 = sub esp, 24`
```
[ GADGET_2 ] 
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[ GADGET_1 ] <- ESP points here 
```

> GADGET_1 gets invoked

---

> `GADGET2 = ret`
```
[ GADGET_2 ] <- ESP points here
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[ GADGET_1 ]
```

> GADGET_2 gets invoked

---

```
[ GADGET_2 ]
[   AAAA   ] <- ESP & EIP point here
[   AAAA   ]
[   AAAA   ]
[   AAAA   ]
[ GADGET_1 ]
```

{{% /section %}}

---

### stack-pivots (extreme!!)
{{% section %}}

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

## how realistic is this?
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

## how realistic is this?
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

{{% /section %}}

---

### Another simple example
{{% section %}}

> 
```
[    AAAA    ] (Address == 0xfffffff0)
[    AAAA    ]
[    AAAA    ]
[    AAAA    ]
[ 0xffffffff ] <- Stored EBP
[     EIP    ]
```

---

> What does leave do?
```
Leave:
    mov esp, ebp
    pop ebp
    ret
```

---

> Overflow into Least Significant Byte
```
[    AAAA    ] 
[    AAAA    ]
[    AAAA    ]
[    AAAA    ]
[ 0xfffffff0 ] <- partial overwrite
[     EIP    ] 
```

---

> once we leave, ESP points to `0xfffffff0`
```
[    AAAA    ] <- ESP points here (execution resumes here)
[    AAAA    ] 
[    AAAA    ]
[    AAAA    ]
[ 0xfffffff0 ] <- partial overwrite
[     EIP    ] 
```

{{% /section %}}

---

{{% section %}}

## srop
sig-return oriented programming

---

TODO

{{% /section %}}

---

## 
> are there any challenges you want me to demo?

---

## Tutorial
