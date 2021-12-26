---
layout: post
title:      Investing in Tools
date:       2021-06-03T18:47:19-04:00
author:     invisiblethreat
thumbnail:  gravatar
summary:    Sharpen the axe, then cut the tree down
categories: books
tags:
 - learning
 - tools
 - vim
 - vscode
---

> Give me X hours to cut down a tree, and I will spend the first Y sharpening the axe - Lincoln

## High Leverage Activities

After reading _Limitless_ by Jim Kwik, it made me think more about investing in
the tools that I use every day. There are a few things that I know how to use
pretty well, but I never really thought about optimizing my usage. Part of this
came from a coworker posting about a cool new way to set up containers for
development environments using a VSCode extension called "devcontainer". Take a
few minutes to check it out- [The Magic of VSCode](https://www.iannelson.dev/vscode/the-magic-of-vscode/).

I use VSCode pretty regularly, and if you're coding in Go, it's a pretty great
IDE. I prefer it to all others these days. However, I've been helping out the
SRE efforts at work, and this has me spending lots of time on the command line,
which I love. This has really reminded me of how much I've been neglecting my
Vim skills. Part of not investing in my Vim setup was the fact that I've been
using a "good enough" setup for the last few years- I've been coasting. For any
new install, I've been able to get to my desired state with two commands:

```
git clone https://github.com/invisiblethreat/dotfiles
dotfiles/setup
```

[My "dotfile" setup](https://github.com/invisiblethreat/dotfiles) setup has
been serving me well for the better part of a decade, and as soon as I have
access to `git` on a machine, I get to my personal baseline in seconds. With
this said, I've been coasting. It's time to improve my Vim configuration.

## The Great `.vimrc` refactor of 2021

It turns out that I've been adding to my `.vimrc` and never taking time to clean
up when warranted. I still had references to custom binaries in functions from
two jobs ago. This is a super safe way to manage the file, but also leads to
more than zero "WTF is this?" moments.
