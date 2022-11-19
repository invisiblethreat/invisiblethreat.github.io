---
layout: post
title:      2021- The year in review
date:       2021-12-26
author:     invisiblethreat
thumbnail:  gravatar
summary:    Another strange year in so many ways
categories: general
tags:
 - learning
 - tools
---
# Another year in the books...

There are a few things that I was able to accomplish in 2021 that I'd like to
talk about, and probably a few others that should be mentioned. The things that
I'll choose to omit are most likely gross failures to even get a project
started, so it may get kicked ahead to 2022. Maybe.

## My Internal Conflict

There are not enough hours in the day for me to learn all the things that are
interesting to me. I also find that as a specialize more and more at work, the
more that I want to branch out into other technical realms in order to be more
well rounded. It serves two purposes: I love learning, and I also love to be
self-sufficient. During the year I did find a few places where I could align
some of my technical learning goals with work goals, which was nice. Some of the
things that I wasn't able to justify for work-purposes are getting rolled over
to 2022, but I haven't decided on an approach just yet.

My biggest challenge to learning new technical skills outside of work is the
allocation of time. Spending extra hours in front of a computer after I'm done
work for the day is done can sometimes be a real drain, and I don't feel like
I'm unplugging. It also interferes with other things that are just as important
to me, like jiu jitsu and mountain biking. I don't know how to balance it all.
I've also found that if I attempt to do technical learning first thing in the
morning, that it quickly leads to me starting work early, which has yet to
result in me walking away from the computer any earlier at the end of the day.
Maybe I have boundary issues? Working on a distributed team that has a -5h to
+4h spread means that there's always something going on, or someone to chat with
about something that we can improve. Maybe time management should be at the top
of my list for 2022.

### Start, Stop, Continue, but in a different order.

I find the "start, stop, continue" feedback process the most actionable sort of
way to think about moving forward, but I've never applied it to personal
development, so here we go.

### Stop

* Using R. I started using R in 2017 when I needed programmatic graphs and it
    fit the bill. `ggplot2` can make some beautiful graphs. My main issue is
    that the *I* find the language completely arcane. Between the `tidyverse`,
    CRAN, and the standard language itself, there's just too much variety. Too
    many calling conventions, arbitrary naming and syntax conventions , and and
    general lack of uniformity. RStudio is nice, but I find a lot of the tooling
    weak, and the error messages terse enough that I'd never attempt to code
    without access to the internet.
* Complaining about JavaScript(on the front-end). I haven't denied the utility
    of JS on the front-end, but I have willfully ignored it as something that
    I'm not willing to spend time learning. I maintain that NodeJS, while
    enormously popular, is a mistake.
* Saying "yes" to all requests. The ability to be versatile doesn't always mean
    that you should actually be versatile. The more things that you take on, the
    more obligations and interruptions you accumulate. This can become
    antithetical to deep work and learning.
* Arguing on technical solutions. If I'm not the person doing the work, all I
    can do is offer my perspective and supporting evidence. If I'm not the one
    implementing, this needs to get to "disagree on the implementation, but
    agree that it's the path forward".

### Continue

* Improving at `vim`, more specifically `nvim`. I overhauled my `.vimrc` to be
    an `init.vim` in the last few months as part of the exercise and have really
    enjoyed taking the time to attempt to master some of the core features. I've
    been using `vim` for 15 years, and was still using arrows, and many other
    rookie methods. Leaning motions has been great, and I'm finally starting to
    really unlock the power of the "editing first" principles. I've been doing
    Python development for smaller projects exclusively in `vim` and I hope to
    move my Go development into `vim` as well.
* Learning/relearning Python. I dabbled in Python 2.5ish days and it really felt
    like a more structured version of shell(this is an oversimplification, but
    that was my impression at the time). Watching the train-wreck of the 2 to 3
    migration(and the Perl 5 to 6... um, whatever that has turned in to) let me
    put it on the shelf as a "I'll get back to this at some point" item. I knew
    that web frameworks had popped up, and that the push to Python 3 had picked
    up steam. In coming back in the last year, thing like type checking, and
    overall tooling seem to have really come along. The potential removal of GIL
    is also an exciting possibility moving forward.
* Learning more abstractions in Go. I've spent a bit of time learning
    `interface{}`, however, I don't really find myself using it in projects.
    Generics landing in Go 1.18 mean that there will be more abstractions
    showing up in code bases, and knowing what's going on will be very useful.
* Improving SQL. The last year has had me write some queries that went beyond my
    initial comfort, and some were certainly killed by the DB engine for being
    abusive. Refining queries, and really understanding sub-queries and making
    results sets smaller earlier via constraints seems like an easy win. I've
    also had to translate queries to other engines that don't support all of the
    features that I'm used to which has been interesting. Knowing when something
    is specific to an engine will also be important going forward.
* Knowledge synthesis. I started very deliberate leaning for `vim` and the
    results have been quite good. I plan to expand the technique into other
    technical realms.

### Start

* Learn some JavaScript. This is only for front-end work(see above comments for
    thoughts on Node). It seems that Next.js is quite popular, and when I ask
    front end devs what framework they'd pick if they were able to start over
    today, and Next.js is almost always the answer. I've been doing all sorts of
    work from data generation/collection, to APIs to expose the information, but
    I've never done a modern front end to display the results. My last serious
    front end used PHP and tables for layout.
* Get comfortable with pointers in C. I understand C just fine until folks break
    out multiple levels of indirection with pointers. It's no wonder that
    dangling pointers and "use after free" bugs are a thing. Sadly it's outside
    of my current skills to be effective in that area. Also, it's a good bridge
    to being able to better understand assembly languages and other outputs from
    reverse engineering.


## Onward

Taking the time to reflect on my technical goals for the upcoming year should
help me direct my focus. It also gives me a reference for what I thought was
important to me if these things fail to materialize. Capturing information is
the first step, reviewing and reflecting on it at a later date may actually be
the much more powerful part of the equation.
