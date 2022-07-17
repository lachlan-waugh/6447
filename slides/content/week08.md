---
title: "Week08"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at [46]:05

---

{{< slide class="center" >}}
# Week08
### T1[68]A COMP6447 

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: Don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

### Chunkz
{{% section %}}
Stuff about chunks

---

{{% /section %}}

---

### In-use chunks
{{% section %}}

<img src="../img/week08/in-use.png" height="500px" />

---

#### What is the "metadata"
* size of the chunk
* last 3 bits:
    * 1: chunk is in main arena
    * 2: chunk is mmap'd (not in the heap)
    * 3: previous chunk in use

> mixing metadata (control) & user data?

---

<img src="../img/week08/in-use2.png" height="500px" />

{{% /section %}}

---


### Free chunks
{{% section %}}


---

{{% /section %}}

---


---

## `free()`
{{% section %}}


---

{{% /section %}}

---

## Use after free
{{% section %}}

### How does `free()` work
* After a chunk is `free()`'d
    * what happens to a pointer to it?
    * what happens to it's contents?

---

### what happens to a pointer to it?

> Nothing, we can still use the pointer (which is why we needed to `NULL` it)

---

### what happens to it's contents?


---



{{% /section %}}

---

## Double free
{{% section %}}


{{% /section %}}

---

## Demo

---

## Tutorial

---

## Walkthrough