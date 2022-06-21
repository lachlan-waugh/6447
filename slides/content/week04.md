---
title: "Week04"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05

---

{{< slide class="center" >}}
# Week04
### T1[68]A COMP6447 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

## Lecture content
* format strings
* where to write
* memory protections

---

{{% section %}}

## printf (and it's siblings)
* `[v,va,s,sn,f]printf`
* `[v,va,s,sn,f]scanf`
* `setproctitle`, `syslog`, and others!

---

## anatomy of a format string
`%<flags><width><precision><modifier><type>`

---

## types
* `%d`: print as signed decimal
* `%x`: print as hex
* `%c`: print as a character
* `%p`: print out a value as a pointer
* `%s`: print as a string?
* `%n`: huh?
* ... more [here](https://www.freecodecamp.org/news/format-specifiers-in-c/)

---

## modifiers
* `h`: print half 
	* `%hd`: print bottom 2 bytes
	* `%hn`: write two bytes
* `hh`: print half half (quarter)
	* `%hhd`: print bottom byte
	* `%hhn`: write one byte

---

## width (minimum width)
* you can pad your input, like `zfill()` in python 
* `%10c` pads the argument to 100 bytes

```C
printf("%10c", 5);
>         5
```

```C
printf("%10c", 10)
>        10
```

---

## index
* not included in the graphic, woops
* which argument we want to print from/to
* e.g. `%10$x` prints the 10th argument as hex

```C
int a = 1, b = 2, c = 3;
printf("%2x", a, b, c);
> 0x2
```

---

## This is a hacking course, why should I care?
* what happens when you don't provide any arguments (apart from the format string)?
* e.g. `printf(buffer);`

{{% /section %}}

---

{{% section %}}

## Where to write
* Overwrite variables
* Overwrite function pointers
	* PLT / GOT
	* function hooks (malloc hook, free hook, \_\_atexit)

---

## Potential issues when writing 
* padding
* writing addresses?

---

## Padding
* 

---

## Writing addresses
* 

{{% /section %}}

---

{{% section %}}

# Protections

---

## recognise leaked addresses
* `0x565...`: binary base (PIE enabled)
* `0x804...`: binary base (PIE disabled)
* `0xf7f...`: library base
* `0xff....`: stack base

{{% /section %}}

---

## Demo

---

## Tutorial

---

## Walkthrough
