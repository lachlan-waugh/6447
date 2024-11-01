---
title: "8: heap"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 18:05

---

{{< slide class="center" >}}
# heap exploitation
### 6447 week8 

---

### chunks
`malloc()` returns chunks (blocks of memory)

* chunks can either be **in-use** or **free**
* each has different metadata associated with it

---

### in-use chunks
{{% section %}}

<img src="../assets/img/week8/in-use.png" height="500px" />

---

#### what is the "metadata"
* size of the chunk
* last 3 bits:
    * 1: chunk is in main arena
    * 2: chunk is mmap'd (not in the heap)
    * 3: previous chunk in use

> mixing metadata (control) & user data?

---

<img src="../assets/img/week8/allocated.png" height="500px" />

{{% /section %}}

---

### free chunks
{{% section %}}
> a bunch of other metadata

* size of the previous chunk
* a pointer to the next / previous chunk
* basically just a bunch of *control* characters
* etc

---

<img src="../assets/img/week8/free.png" height="500px" />

{{% /section %}}

---

## `free()`
{{% section %}}
> after a chunk is `free()`'d, information about it is stored in a 'bin'

* fast bins
* non-fast
    * unsorted bins
    * small/large
* tcache

---

### Fast-bins
* used to store information about <u>small</u> chunks
* chunks are stored in size-specific bins
    * 16, 24, 32, ... 88 bytes (10 total)

* a fast-bin is a singly-linked list
    * new chunks are added to the start (LIFO)
    * chunks aren't combined with adjacent chunks

---

### Unsorted bins
* used to store information about <u>large</u> chunks
* all chunks are stored in a single bin (of various sizes)
* later, chunks are sorted by malloc for quicker re-use.

---

### Other bins
* normal bins are divided into:
    * 62 small bins (chunks of *same* size)
    * 2 large bins (chunks of *similar* sizes)
* chunk sizes may be changed
    * chunks are coalesced with adjacent chunks
    * large chunks may be split on a `malloc()`
    * it's a doubly-linked list to help with this

---

### tcache bins
> [thread-local cache](https://sourceware.org/glibc/wiki/MallocInternals#Thread_Local_Cache_.28tcache.29)
each bin can only store 7 chunks

* ~~pretty insecure tbh (but very fast)~~
* ~~basically doesn't have any checks~~
* actually pretty decent now

{{% /section %}}

---

{{% section %}}
### A quick note
we're attacking heap implementation, not bad programming. So you'll need to use the right version
* depending on your libc version, you might get errors, e.g. double `free()` detected.
* we'll be attacking glibc 2.31

---

### Solution?
* just use docker
```
docker run -d --rm -h banana --name banana -v .:/ctf/work --cap-add=SYS_PTRACE skysider/pwndocker
docker exec -it banana /bin/bash
```
{{% /section %}}

---

## use after free
{{% section %}}

### how does `free()` work
* after a chunk is `free()`'d
    * what happens to pointers to it?
    * what happens to it's contents?

---

### answers
* Q: what happens to a pointer to it?
> nothing, we can still use the pointer

&nbsp;

* Q: what happens to it's contents?
> it gets replaced with that metadata

---

### forging chunks
if we modified the metadata (e.g. the next chunk ptr), then malloc(...) would return memory we tell it to.

```PHP
free(chunk)     // bin: chunk -> NULL
*chunk = "AAAA" // bin: chunk -> 0x41414141 -> ????
malloc(...)     // bin: 0x41414141 -> ????
malloc(...)     // bin: ????
// the second call to malloc returns 0x41414141
```

---

### demo

{{% /section %}}

---

## double free
{{% section %}}
* what happens if we `free()`'d a chunk twice?
    * first time: it's added to the free list
    * second time: it's added to the free list, again?

> doesn't really work this easily anymore, but can still be used sometimes

```PHP
free(chunk)     // bin: chunk -> NULL
free(chunk)     // bin: chunk -> chunk -> NULL

malloc(...)     // bin: chunk -> NULL
malloc(...)     // bin: NULL
```

both calls to `malloc()` return the same chunk?

---

there's basic protections against double `free()`s, and it'll `SIGABORT` when detected
<img src="../img/week08/double_free.png" />

> but what if you just...
```PHP
free(chunk_1)
free(chunk_2)
free(chunk_1)
```

{{% /section %}}

---

## PWNDBG stuff
* `vis_heap_chunks`
* `bins`
* `heap`
* `arena`
