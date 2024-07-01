---
title: Array initialization with ranges in C
authors:
- Chris Wilson
date: "2024-07-01"
draft: false
slug: array-initialization-with-ranges-in-c
series:
- Today I learned
tags:
- TIL
- C
- GNU C extensions
- GCC
disableComments: false
typora-copy-images-to: ./images
---

{{< notice note >}}

This post is part of a new series of short-form posts titled **[Today I learned](/series/today-i-learned/)**. These posts are intended to be short and more informal—my goal is for you to learn one thing quickly.

{{< /notice >}}

**[Today I learned](/series/today-i-learned/)** there is a [GNU C extension](https://gcc.gnu.org/onlinedocs/gcc/C-Extensions.html) for [designated initializers](https://gcc.gnu.org/onlinedocs/gcc/Designated-Inits.html) that makes it possible to initialize a *range* of elements in an array.

![range-example](images/range-example.webp)

If you happen to be using GCC (or another compatible compiler that supports this GNU extension, like Clang), you can specify a *range* (`[first ... last]`) in the designated initializer list.

Using the example in the diagram above, we can initialize the range of elements `[2, 4]` to the value `1` and the range  `[7, 9]` to the value `2` using the following syntax:

```c
int a[10] = {[2 ... 4] = 1, [7 ... 9] = 2};
```

All the other array elements that are not initialized explicitly are implicitly initialized to zero.

As a result, the example above is equivalent to:

```c
int a[10] = {0, 0, 1, 1, 1, 0, 0, 2, 2, 2};
```
