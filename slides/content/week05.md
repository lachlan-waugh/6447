---
title: "05: programming errors/fuzzing"
layout: "bundle"
outputs: ["Reveal"]
---

## We'll get started at 1[68]:05

---

{{< slide class="center" >}}
# fuzzing & programming errors
### 6447 week05

---

## Good faith policy

We expect a high standard of professionalism from you at all times while you are taking any of our courses. We expect all students to act in good faith at all times

*TLDR: don't be a ~~dick~~ jerk*

[sec.edu.au/good-faith-policy](https://sec.edu.au/good-faith-policy)

---

{{% section %}}
## Fuzzer (Group Project)
* [[Major Project](https://webcms3.cse.unsw.edu.au/COMP6447/23T3/resources/92851)] on WebCMS

---

### okay
> ramble about fuzzers

---

### due dates
* *midpoint*: end of week07
* *final*: end of week10

---

### Groups
* register [here](https://forms.gle/7As9vpV47JB1KSCU8) (linked on WebCMS)
* each group, just email me whos in your group
* cross-tutorial groups are fine

{{% /section %}}

---

## wargame marks so far
|         |  `avg` |  `3/3` |
| ------- | ------ | ------ |
| `war01` | `2.50` |  `18`  |
| `war02` | `2.25` |  `??`  |
| `war03` | `1.80` |  `??`  |
| `total` | `6.55` |  `??`  |

---

# source Code Auditing

---

### what do these code blocks do?
```C
    int flags = 1;
    if (flags & FLAG){
        printf("TRUE\n");
    } else{
        printf("FALSE\n");
    }
```

{{% fragment %}}
```C
    if (flags & FLAG != 0){
        printf("TRUE\n");
    } else{
        printf("FALSE\n");
    }
```
{{% /fragment %}}

{{% fragment %}}
```C
    if (flags & (FLAG != 0)){
        printf("TRUE\n");
    } else{
        printf("FALSE\n");
    }
```
{{% /fragment %}}

---

### is this code the same?

```C
flags = flags + 1 % 2;
printf("Flags: %d\n",flags);
```

&nbsp;

```C
flags = flags++ % 2;
printf("Flags: %d\n",flags);
```

---

{{% section %}}

### where vuln?

```C
char pt[] = "THISISSOMEDATAOFSOMESORT";
char env_script_name[] = "USER_CONTROLLED_ENV1";
char env_path_info[] =  "USER_CONTROLLED_ENV2";
int ptlen = strlen(pt) - strlen(env_script_name);
int path_translated_len = ptlen + env_path_info
                          ? strlen(env_path_info) : 0;
char *path_translated = NULL;
path_translated = (char *) malloc(path_translated_len + 1);
memcpy(path_translated, pt, ptlen);
if (env_path_info) {
    memcpy(path_translated + ptlen, env_path_info,
           path_translated_len - ptlen);
```

---

### it's here
```C
//                        vvvvvvvvvvvvvvvvvvvvvvvvvvvv
int path_translated_len = ptlen + env_path_info
                          ? strlen(env_path_info) : 0;
//                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
path_translated = (char *) malloc(path_translated_len + 1);
memcpy(path_translated, pt, ptlen);
if (env_path_info) {
    memcpy(path_translated + ptlen, env_path_info,
//         vvvvvvvvvvvvvvvvvvvvvvvvvvvvv
           path_translated_len - ptlen);
//         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

---

### The problem?
```C
ptlen + env_path_info ? strlen(env_path_info) : 0;

// is not the same as
ptlen + (env_path_info ? strlen(env_path_info) : 0);
```

---

### what they wanted
```C
if(env_path_info) {
    path_translated_len = ptlen + strlen(env_path_info);
} else {
    path_translated_len = ptlen;
}
```

### what they got
```C
if (ptlen + env_path_info){
    path_translated_len = strlen(env_path_info);
} else {
    path_translated_len = 0;
}
```

---

> $ man mmap

{{% /section %}}

---

{{% section %}}
### What is the issue here?
```C
if (x == 0) {
    if (y == 0) error();
else {
    z = x + y;
    fclose(&z);
}
```

---

### what they wanted
```C
if (x == 0) {
    if (y == 0) error();
} else {
    z = x + y;
    fclose(&z);
}
```

### what they got
```C
if (x == 0) {
    if (y == 0)
        error();
    else {
        z = x + y;
        fclose(&z);
    }
}
```

{{% /section %}}

---

{{% section %}}
## Order of operations
> which one is calculated first?
```C
a + b * c
> a + (b * c)
> (a + b) * c
```

---

### This is good :)
```C
if (count != 0 && sum/count < smallaverage)
    printf("average < %g\n",smallaverage);
```

&nbsp;

### This, not so much
```C
i = 0
while (i < n)
    y[i] = x[i++];
```

> but why?
{{% /section %}}

---

{{% section %}}

### why is this bad?
```C
u_int strLen = strlen(userinput);
int buffsize = strLen + 11;

char *mem = malloc(buffsize);
strncpy(mem,"this/path/",10);
strncpy(mem[10],userinput,strLen);
```

---

### why is this bad?
```C
u_int strLen = strlen(userinput);
int buffsize = strLen + 11;

char *mem = malloc(buffsize);
strncpy(mem,"this/path/",10);
strncpy(mem[10],userinput,strLen);
```

> its an integer overflow

---

## it's here

```C
u_int strLen = strlen(userinput);
//vvvvvvvvvvvvvvvvvvvvvvvvv
int buffsize = strLen + 11;
//^^^^^^^^^^^^^^^^^^^^^^^^^

char *mem = malloc(buffsize);
strncpy(mem,"this/path/",10);
strncpy(mem[10],userinput,strLen);
```

what if user input is super long, (e.g. INT_MAX?)

{{% /section %}}

---

## format strings
```C
char *var;
printf(var);
fprintf(stderr,var);
vsnprintf(var2, strlen(var2), var);
// etc...
```
> I hope you recognise these lol

---

## Heap
{{% section %}}

### why is this bad?
```C
char *var malloc(10);
free(var);
printf("%s\n", var);
```

---

### why is this bad?
```C
char *var malloc(10);
free(var);
printf("%s\n", var);
```

> use-after-free

---

### why is this bad?
```C
char *var malloc(10);
free(var);
char *var2 malloc(10);
free(var);
```

---

### why is this bad?
```C
char *var malloc(10);
free(var);
char *var2 malloc(10);
free(var);
```
> double-free

{{% /section %}}

---
 
{{% section %}}

### why is this bad?

```C
char *a;
a = NULL;
char b[] = "string";
strcpy(a, b);
```

---

### why is this bad?

```C
char *a;
a = NULL;
char b[] = "string";
strcpy(a, b);
```

> null pointer dereferences

---

### how about this?

```C
char *a, b[] = "string";
// vuln_syscall_sets_a_NULL
// Lets map NULL pointer
mem = mmap(NULL, 0x1000, PROT READ | PROT WRITE | PROT EXEC,
           MAP FIXED | MAP ANONYMOUS | MAP PRIVATE, 0, 0);
if (mem != NULL)
    fatal("[-] UNABLE TO MAP ZERO PAGE!");
    exit(1);

fprintf(stdout, "[+] MAPPED ZERO PAGE!\n");
strcpy(a, b);
printf("%s\n",a);
```

{{% /section %}}

---

{{% section %}}
### why is this bad? 
```C
char *var = malloc(10);
if(var == NULL) return;

for(int i = 0; i <= 10; i++) {
    var[i] = argv[2][i];
}
```

---

### why is this bad? 
```C
//          vvvvvvvvvv
char *var = malloc(10);
//          ^^^^^^^^^^
if(var == NULL) return;

//             vvvvvvv
for(int i = 0; i <= 10; i++) {
//             ^^^^^^^
    var[i] = argv[2][i];
}
```

> off-by-one

---

## The problem
```C
char *var = malloc(10);
//          ^^^^^^^^^^^
if(var == NULL) return;

for(int i = 0; i <= 10; i++) {
//             ^^^^^^^^
    var[i] = argv[2][i];
}
```
{{% /section %}}

---

## Tutorial
> find the vulns [here](https://waugh.zip/6447/demos/src)
* consider the impact of the vulns

