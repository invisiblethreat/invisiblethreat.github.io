---
layout: post
title: VSCode, GOOS, and you.
date:       2021-09-21T18:47:19-04:00
author:     invisiblethreat
thumbnail:  gravatar
summary:    Cross-OS gopls issues got you down?
categories: books
tags:
 - golang
 - goos
 - vscode
 - windows
 - darwin
---
## VSCode & `gopls`: friends or foes?

I've had issues with VSCode and `gopls` on macOS since it's been a thing. I was
really excited about it at first, and then the problems started coming:

- unresponsiveness
- no imports
- no code hints
- no IntelliSense

This generally made the language server not worth using to me, and I reverted to
`goimports` and friends. I had the feeling of always knowing that a day would
come when the language server would be foisted upon me and I'd have limited
options of what to do about it.

When leaving my last job I took the time to drag my `settings.json` along with
me, just in case, but I tried a fresh install. Things just worked and life was
great. I didn't give another thought to it, because I had no need to. This all
changed when I found out that I'd be targeting Windows on a project- everything
went sideways.

The error was opaque and I was back to the above list of issues, minus the
unresponsiveness because most things just weren't loading. Even the smallest
thing, like not knowing how many return values a function had ground my coding
to a halt. I then truly realized how heavily I depended on the Go toolchain to
help me get to workable code.

Does this scream "I have a cross-compile issue when starting the language
server?". It sure didn't to me.

[terse error message](/images/code-error.png)

That message didn't return useful search results, so the debugging continued. On
a whim I tried `GOOS=windows code .` and everything was magical. Things just
worked.

So it seems when dealing with build constrained packages, there needs to be
something that happens when the above situation occurs.

I ended up testing workspace settings and all was revealed. It feels like there
should be a much more friendly way of getting to this solution through some sort
of detection, but I ended up scripting a solution instead.

```shell
#!/bin/bash
if [ -d .vscode ]; then
  echo ".vscode directory exists- refusing to overwrite."
  exit 1
fi

mkdir .vscode

cat << EOT > .vscode/settings.json
{
    "go.toolsEnvVars": {
        "GOOS": "windows"
    }
}
EOT
```
