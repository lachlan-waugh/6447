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

#### In-use chunks
<img src="../img/week08/in-use.png" style="zoom:40%"/>
<!-- ![](../img/week08/in-use.png) -->

---

### Free chunks


---

{{% /section %}}

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