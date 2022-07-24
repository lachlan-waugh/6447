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
`malloc()` returns chunks (blocks of memory)

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

<img src="../img/week08/allocated.png" height="500px" />

{{% /section %}}

---

### Free chunks
{{% section %}}
> A bunch of other metadata

* Size of the previous chunk
* A pointer to the next / previous chunk
* basically just a look of *control* characters
* etc

---

<img src="../img/week08/free.png" height="500px" />

{{% /section %}}

---

## `free()`
{{% section %}}
> After a chunk is `free()`'d, information about it is stored in a 'bin'

* Fast bins
* Non-fast
    * Unsorted bins
    * Small/Large
* TCache

---

### Fast-bins
* Used to store information about <u>small</u> chunks
* Chunks are stored in size-specific bins
    * 16, 24, 32, ... 88 bytes (10 total)

* A fast-bin is a singly-linked list
    * New chunks are added to the start (LIFO)
    * Chunks aren't combined with adjacent chunks

---

### Unsorted bins
* used to store information about <u>large</u> chunks
* all chunks are stored in a single bin (of various sizes)
* later, chunks are sorted by malloc for quicker re-use.

---

### Other bins
* Normal bins are divided into:
    * 62 small bins (chunks of *same* size)
    * 2 large bins (chunks of *similar* sizes)
* chunk sizes may be changed
    * chunks are coalesced with adjacent chunks
    * large chunks may be split on a `malloc()`
    * it's a doubly-linked list to help with this

---

### Tcache bins
> [thread-local cache](https://sourceware.org/glibc/wiki/MallocInternals#Thread_Local_Cache_.28tcache.29)

* pretty insecure tbh (but very fast) 
* basically doesn't have any checks
* each bin can only store 7 chunks

{{% /section %}}

---

{{% section %}}
### A quick note
* *we're attacking the heap implementation, not bad programming. So different systems/versions may change how the program acts (& if your exploit works)*

* Depending on your OS/LIBC version/~~the orientation of the sun~~, you might get errors, e.g. double `free()` detected blah blah.

---

### Solution?
* Just use docker
    * `docker run -d --rm -h banana --name banana -v $(pwd):/ctf/work --cap-add=SYS_PTRACE plsiamlegit/6447-ubuntu:pwndocker`
    * `docker exec -it banana /bin/bash`

{{% /section %}}

---

## Use after free
{{% section %}}

### How does `free()` work
* After a chunk is `free()`'d
    * what happens to pointers to it?
    * what happens to it's contents?

---

### what happens to a pointer to it?

> Nothing, we can still use the pointer

---

### what happens to it's contents?
> it gets replaced with that metadata

---

### Exploiting this?

if we modified the metadata (e.g. the next chunk ptr), then malloc(...) would return memory we decide.

```PHP
free(chunk)     // bin: chunk -> NULL
*chunk = "AAAA" // bin: chunk -> 0x41414141 -> ????
malloc(...)     // bin: 0x41414141 -> ????
malloc(...)     // bin: ????
// the second call to malloc returns 0x41414141
```

{{% /section %}}

---

## Double free
{{% section %}}
* What happens if we `free()`'d a chunk twice?
    * first time: it's added to the free list
    * second time: it's added to the free list, again?

```PHP
free(chunk)     // bin: chunk -> NULL
free(chunk)     // bin: chunk -> chunk -> NULL

malloc(...)     // bin: chunk -> NULL
malloc(...)     // bin: NULL
```

Both calls to `malloc()` return the same chunk?

---

There's basic protections against double `free()`s, and it'll `SIGABORT` when detected
<img src="../img/week08/double_free.png" />

> But what if you just...
```PHP
free(chunk_1)
free(chunk_2)
free(chunk_1)
```

{{% /section %}}

---

## Demo
* *Double free*
* *Use-after free*

---

## PWNDBG stuff
* `vis_heap_chunks`
* `bins`
* `heap`
* `arena`


---

## Tutorial

---

## Walkthrough