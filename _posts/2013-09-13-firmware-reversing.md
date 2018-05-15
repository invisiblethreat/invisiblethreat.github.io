---
layout: post
date:   2013-09-13T22:53:35-0400
author: "Scott Walsh"
title:  "Firmware Reverse Engineering, an Introduction"
tags:
  - reversing
  - firmware
  - fmk
catagories: reversing
---

 My latest interest has been spawned by an
 [awesome post](http://blog.ioactive.com/2013/09/emulating-binaries-to-discover.html) by
 Ruben Santamarta [@Reversemode](https://twitter.com/reversemode) of IOActive.
always had a rough idea what was going on with applying a firmware image to a
device, but it was never anything that I investigated. After reading the
article, I was ready to go! I conceptually understood what was happening...
how hard could it be? Harder than I thought.

First things first, you need [binwalk](http://code.google.com/p/binwalk/),
which may or may not complain about the right version of 'magic' for Python. If it complains, grab the most recent version of [file](ftp://ftp.astron.com/pub/file/)(build and install, and make sure that you
install the bindings for Python in `python`). Great `binwalk` works, now what?

Now we decide on what to rip apart, and I picked some
[random D-Link firmware](ftp://ftp.dlink.ca/PRODUCTS/DIR-615/DIR-615_REVC_FIRMWARE_3.13.BIN).
I've deployed one of these DIR-615 units somewhere at some point, but don't
have one on hand. The initial scan went something like this:

```shell
$ binwalk DIR-615_REVC_FIRMWARE_3.13.BIN

DECIMAL         HEX             DESCRIPTION
-------------------------------------------------------------------------------------------------------------------
0               0x0             uImage header, header size: 64 bytes, header CRC: 0x8D5601FA, created: Tue Sep 14 04:55:47 2010, image size: 972355 bytes, Data Address: 0x80060000, Entry Point: 0x8030D000, data CRC: 0x9F3F0366, OS: Linu
x, CPU: MIPS, image type: OS Kernel Image, compression type: lzma, image name: &quot;Linux Kernel Image&quot;
64              0x40            LZMA compressed data, properties: 0x5D, dictionary size: 8388608 bytes, uncompressed size: 2949254 bytes
1048576         0x100000        Squashfs filesystem, big endian, version 3.0, size: 2518754 bytes, 580 inodes, blocksize: 65536 bytes, created: Tue Sep 14 04:56:05 2010
```

(that code box is not amazing, but you've already made it this far...)

So the thing that I immediately understood was that I could grab the Squashfs section pretty easily with:

```shell
$ dd if=DIR-615_REVC_FIRMWARE_3.13.BIN bs=1 count=2518754 skip=1048576 of=dir615.sqfs

file dir615.sqfs
 dir615.sqfs: Squashfs filesystem, big endian, version 3.0, 2518754 bytes, 580 inodes, blocksize: 65536 bytes, created: Tue Sep 14 04:56:05 2010
```

That looked promising, right? This quickly turned into a case of me being out
of my depth. I basically thought I'd be able to run `unsquashfs` on that
resulting image, but in reality, it just died:

```shell
$ unsquashfs dir615.sqfs
Reading a different endian SQUASHFS filesystem on a
Parallel unsquashfs: Using 8 processors
zlib::uncompress failed, unknown error -3
read_block: failed to read block @0x266d4a
read_fragment_table: failed to read fragment table block
FATAL ERROR aborting: failed to read fragment table
```

This seems to indicate that I don't know what's going on, and to some extent
this is true. In particular, I don't understand the LZMA component of the
image. I was aware of
[Firmware Mod Kit](http://code.google.com/p/firmware-mod-kit/),
but hadn't used it before. After grabbing FMK, I picked up a few dependencies,
like `liblzma`, I was on my way.

`$ ./extract-firmware.sh ../DIR-615_REVC_FIRMWARE_3.13.BIN demo`

Leads to a fully extracted image. Digging around in the logs of FMK lets me
know that the `unsquasfs-lzma` binary was used, which makes me want to explore
some more. Part 2 to follow, dissecting how FMK got this done.
