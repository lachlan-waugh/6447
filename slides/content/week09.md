---
title: "Week09"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05

---

{{< slide class="center" >}}
# Week09
### T1[68]A COMP6447 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

## Stack pivots
{{% section %}}

### The problem
* we have an overflowable buffer
* it's too small for a full ROP payload

> think back to shellcode egghunters

---

### The solution
* We could:
    * jump back earlier in the current buffer
    * jump into a bigger buffer (better/harder)

> a.k.a we ~pivot the stack~

{{% /section %}}

---

### Simple example
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

### Stack-pivots (extreme!!)
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

* how realistic is this?


```C

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

## Demos
> there are none l0l

---

### One gadgets
> TODO

---

## Walkthroughs
> are there any challenges you want me to demo?

---

## Tutorial
