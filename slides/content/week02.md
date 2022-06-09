---
title: "week02"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05

---

{{< slide class="center" >}}
# week02
### COMP6447 T1[46]A
Buffer Overflowssssssssssssssssssssssssssssssssssssssssssss\xef\xeb\ad\ed

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

{{% section %}}

## Lecture content
* Register layout
* Stack frames
* Reverse engineering
* The stack
* Assembly instructions
* ASLR

---

## Register layout
* AX is actually the bottom half of EAX (it's AH and AL), not the top half
![](/img/week02/registers.png)

---

## Stack frames
![](/img/week02/stack-grows-up.png)
* what register stores the stack pointer, and frame pointer?
* Why are the parameters stored *below* the frame pointer?

---

## Actually it grows down
The stack grows from high address to low addresses
![](/img/week02/stack-grows-down.png)

---

## ASLR
```bash
# turn aslr off
sudo sysctl kernel.randomize_va_space=0

# check if it's on
cat /proc/sys/kernel/randomize_va_space
```

{{% /section %}}

---

{{% section %}}

## Demo


---


{{% /section %}}

---

## Lab
* There is one binary, with 2 vulnerabilities (both trivial)
    * Don't look at the source code, later on you won't be given it!
    * Hop into groups of 2, give it a shot!

---

# Walkthrough

---

## Stack canaries
They save the day and make everything impossible to crack! :)

---