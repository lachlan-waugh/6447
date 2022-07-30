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
{{% section %}}
*`3` section (each worth `33%`)*
* `pwn`
* `reversing`
* `source auditing`

> each has `3-4` challenges

---

{{% /section %}}

---

## tips/how2hack
{{% section %}}

### general
* Practice, practice, practice
    * Time pressure makes the exam suck
    * You've seen this from the midterm
* You should be able to solve all wargames in `<20` minutes by now (minus heap lol)

---

### pwn
* not all challenges are a single vulnerability
    * e.g. could be format string -> shellcode
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

## ~~Tutorial~~

---

## Wargames
* harder ROP