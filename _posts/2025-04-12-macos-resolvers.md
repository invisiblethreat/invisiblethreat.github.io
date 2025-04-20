---
layout:     post
title:      Per-domain resolvers in macOS
date:       2025-04-12
author:     invisiblethreat
thumbnail:  gravatar
summary:    macOS has a miserable DNS resolution system
categories: technology
tags:
 - macos
 - technology
 - dns
---
# macOS, DNS, and you

First things first: I don't fully understand the DNS resolution scheme that
Apple has dreamed up in macOS. Furthermore, I don't really want to- I just want
things to work in a manner that let's me get on with my life.

## The Problem

I run a fairly extensive home lab, with lots of projects and resources. I also
run the private DNS suffix `.lan` to access all of these resources. I make
regular use of these resources for work. This comes into direct conflict with
our access control system for work. If I have the ACL software active, my
resolver address is replaced and I'm unable to access my lab via hostnames.

However, this isn't an outright block, I can still resolve things if I specify
the nameserver that I want to use. With this knowledge, I set out to fix access
to my internal hosts. It did not go well. Multiple calls with our ACL provider,
and lots of tampering with things in `/etc/resolv.conf` I was no further ahead.
Deploying `dnsmasq` via `brew` for conditional upstream DNS resolution suffered
from the same issues of being run over when the ACL software was active.

I eventually stumbled across [this article from 2019](https://medium.com/@jamieeduncan/i-recently-moved-to-a-macbook-for-my-primary-work-laptop-7c704dbaff59) about this same thing. I'm not a huge fan of Medium, and the paywall model, so here's the gist of the solution and a handy script to help you out!

## The solution

The solution is available via `/etc/resolver/<Private Namespace>`. In my case,
my internal DNS is using the suffix `.lan`. _Edit: this works for any arbitrary
domain or subdomain. You could employ the same solution for `foo.bar.com` or
`bar.com` and all requests that match the namespace will be routed to that
resolver._

```
sudo mkdir -p /etc/resolver/lan

# 172.18.0.2 is my internal pihole instance, which has an upstream rule that
# points to my authoritative internal DNS server. There are some shell nuances
# about redirection that mean you need to actually either be root, or fully wrap
# the `echo` call in a subshell call to sudo.

echo "nameserver 172.18.0.2" >> /etc/resolver/lan
```

To verify that you now have a private namespace resolver, use the following
command:

```
scutil --dns

# ... many other results ...

resolver #10
  domain   : lan
  nameserver[0] : 172.18.0.2
  flags    : Request A records
  reach    : 0x00000002 (Reachable)

```

As an aside `dig`/`host` are using `/etc/resolv.conf` which makes
troubleshooting difficult. Make sure that you're using `dnscacheutil -q host -a
name` instead.

```
# will use /etc/reslov.conf, which is contains the ACL resolver address
dig pihole.lan +short

# using the resolution chain from scutil --dns
dscacheutil -q host -a name pihole.lan
name: pihole.lan
ip_address: 172.18.0.2
```

That's it! It's done!

## A script

This script is the quickest path to a resolution(!). Enjoy!

```shell
#!/bin/bash

RES_PATH=/etc/resolver
ZONE=$1
NS=$2

if [[ -z $1 || -z $2 ]]; then
  echo "Usage: $0 <zone> <nameserver IP address>"
  exit 1
fi
# Don't clobber an existing configuration
if [ -e "$RES_PATH/$1" ]; then
  RESOLVER=$(cat $RES_PATH/$1| awk '{print $2}')
  echo "$1 already has a custom resolver at $RES_PATH/$1 using $RESOLVER"
  exit 1
fi

# I forget if this exists in a clean install, so make sure it exists
if [ ! -d "$RES_PATH" ]; then
  sudo mkdir -p $RES_PATH
fi

# make the file
sudo touch $RES_PATH/$1

# this needs to be encapsulated because redirection is a shell function of the
# current UID
sudo bash -c "echo \"nameserver $2\" > $RES_PATH/$1"

# verify that things have worked
RESOLVER=$(cat $RES_PATH/$1| awk '{print $2}')
echo "$1 now has a custom resolver at $RES_PATH/$1 using $RESOLVER"
scutil --dns |grep -B1 -A3 $1
```
