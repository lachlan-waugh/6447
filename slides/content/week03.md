---
title: "Week03"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05

---

{{< slide class="center" >}}
# week03
### T1[68]A COMP6447 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

# Programming? in my security course??
* Last week: jumping to a win() function
* This week: there's no win(), what do?

---

{{% section %}}

```
mov a, b        # a = b
add a, value    # a += value
sub a, value    # a -= value
xor a, b        # a ^= b
and a, b        # a &= b
push a          # push a onto stack, dec esp - 4
pop a           # pop into a from stack, add esp + 4
int 0x80        # syscall
```

{{% /section %}}