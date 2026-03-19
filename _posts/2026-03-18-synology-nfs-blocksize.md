---
layout:     post
title:      Bypassing Synology's 32K NFS Block Size Limit with systemd 
date:       2026-03-18
author:     invisiblethreat
thumbnail:  gravatar
summary:    Something is coming, and maybe the argument is around scale
categories: technology
tags:
 - synology
 - nfs
---


The Synology DSM GUI caps NFS read/write packet size at 32K. For a fileserver doing large sequential transfers — media files, backups, VM disk images — that's leaving throughput on the table. The kernel supports up to 1MB block sizes, and the GUI limit is purely artificial.

This post documents how to push past it on DSM 7, which uses `systemd` under the hood.

---

## What the setting actually controls

The NFS block size (`rsize`/`wsize`) determines how much data the client and server exchange in a single NFS operation. Larger blocks mean fewer round trips for the same transfer, which matters most for large sequential reads and writes over a local network.

The server-side maximum is controlled by a kernel procfs entry:

```
/proc/fs/nfsd/max_block_size
```

The DSM GUI writes a value into this at boot, but caps it at 32768 (32K). The kernel itself supports 1048576 (1MB).

---

## Why you can't just echo a value at boot

The obvious approach — write `1048576` to `max_block_size` at startup — hits two problems:

**Problem 1:** Once `nfsd` threads are running, the file is locked:

```
# echo 1048576 > /proc/fs/nfsd/max_block_size
-ash: echo: write error: Device or resource busy
```

**Problem 2:** Even if you write before `nfsd` starts, DSM's NFS service resets the value during its own initialization. The kernel calculates a default block size based on available RAM when `rpc.nfsd` starts, and that write clobbers yours.

The window you need is: **after `/proc/fs/nfsd` is mounted, but before `nfsd` threads spawn.**

---

## How DSM 7 starts NFS

DSM 7 uses systemd. The NFS startup sequence involves three units:

```
proc-fs-nfsd.service   →   [your hook goes here]   →   nfs-server.service
```

- `proc-fs-nfsd.service` mounts the `nfsd` filesystem at `/proc/fs/nfsd`
- `nfs-server.service` calls `/usr/syno/lib/systemd/scripts/nfsd.sh start`, which runs `rpc.nfsd` and spawns the kernel threads

Once `nfs-server.service` runs, `max_block_size` is locked. You need to write your value between these two units.

---

## The fix

Create a systemd drop-in unit that slots between `proc-fs-nfsd.service` and `nfs-server.service`:

```bash
cat > /etc/systemd/system/nfs-blocksize.service << 'EOF'
[Unit]
Description=Set nfsd max_block_size before NFS server starts
After=proc-fs-nfsd.service
Before=nfs-server.service
Requires=proc-fs-nfsd.service

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'echo 1048576 > /proc/fs/nfsd/max_block_size'
RemainAfterExit=yes

[Install]
WantedBy=nfs-server.service
EOF
```

Enable it:

```bash
systemctl enable nfs-blocksize.service
systemctl daemon-reload
```

Verify the ordering was picked up:

```bash
systemctl show nfs-server.service | grep -i after
```

You should see `nfs-blocksize.service` in the `After=` chain for `nfs-server.service`.

Reboot, then confirm:

```bash
cat /proc/fs/nfsd/max_block_size
# 1048576
```

---

## Client side

The server-side change only sets the ceiling. Clients still need to request larger block sizes at mount time. On Linux clients, update `/etc/fstab`:

```
nas:/volume1/share  /mnt/nas  nfs  rsize=1048576,wsize=1048576,vers=4  0  0
```

Or test before making it permanent:

```bash
mount -t nfs -o rsize=1048576,wsize=1048576,vers=4 nas:/volume1/share /mnt/nas
```

Verify what was negotiated after mounting:

```bash
nfsstat -m | grep rsize
```

---

## Notes

- This survives reboots. The systemd unit is persistent.
- DSM updates may overwrite files in `/usr/lib/systemd/system/` but should leave `/etc/systemd/system/` alone. If an update breaks it, just re-run `systemctl enable nfs-blocksize.service && systemctl daemon-reload`.
- If you're using NFSv4 exclusively (likely on a modern Linux-only homelab), you only need port `2049/tcp` open in your firewall. The additional ports required by NFSv3 (mountd, statd, lockd) are not needed.
- The DS918+ ships with 4GB of RAM. The kernel's default block size calculation targets 1MB on machines with that much memory, but DSM's NFS init script overrides it. This fix restores what the kernel would have chosen anyway.
