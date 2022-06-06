---
title: "week02"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05
People b late

---

{{< slide class="center" >}}
# week02
### COMP6447 T1[46]A 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

{{% section %}}

## Lecture content
* Register layout
* The stack
* Assembly instructions
* ASLR

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

## Lab
* There is one binary, with 2 vulnerabilities
* Don't look at the source code!!1

---

# Walkthrough
