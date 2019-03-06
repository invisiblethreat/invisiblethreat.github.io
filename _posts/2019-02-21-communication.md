---
layout:     post
title:      A quick note about communication
date:       2019-02-21T07:31:19-04:00
author:     invisiblethreat
thumbnail:  gravatar
summary:    Some words that we could do without when communication 
categories: soft-skills
tags:
 - soft-skills
 - communication
 - infosec
---

The more I think about it, and the more that I discuss with others, the more I
like the idea of not using the following two words when talking about technical
things:

- "simply"
- "just"

## "simply" and "just"

These words trivialize the time, effort, and complexity when you use them
communicating an "ask" to someone else.

> Can you just... ?

> You simply add...

Both of these trivialize what might be needed to accomplish a task.

### An Example

> Can't you just add an API call for that?

This seems simple, right? On the surface, it feels like something is totally
reasonable, but it doesn't really take into account what's needed to accomplish
the task. This is a question that doesn't take into account anything other than
the requester getting what they want, and invites very simple answers like "no".

A better way to ask the same thing might look like:

> What would it take to add an API call for that?

This invites the person or team that will do the work to think about the scope
and provide a better answer. A more illustrative list of things that may come
from a more open question:

- The API server is already stressed, it can't take more requests
  - Do we need to scale it up?
  - Do we need to fan out the requests?
  - Is the database the real limiting factor?
  - Are our existing queries taking too long, or could they be simplified?
- The API is read-only and points at a replica database that is read-only. There would need to be changes to make this work.
  - Should the API point to the primary DB so it can write?
  - Should there be another API that does the writes and is separate from this API that is exclusively reading?

Asking questions in a more open-ended form allows for more thoughtful answers,
and also gives the ability to properly estimate the work.
