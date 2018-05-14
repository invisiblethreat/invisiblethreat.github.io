---
layout: post
date:   2013-12-13T12:05:59-04:00
title:  "Bypassing Chip & PIN"
author: "Scott Walsh"
tags:
  - chip
  - pin
  - fraud
  - liability
---
'Tis the season, and all that other stuff. What better time for the contact
pad on a "chip and PIN" card to be disconnected from the micro-controller
inside of my credit card. While inconvenient, it has let me know the fallback
modes of various payment system users/providers. It's difficult to say who
decides the variation of fallback methods, the merchant or the processor; both
have incentives to do so.

Fallback modes that I've noted:

* 3 chip failures -> fallback to magnetic stripe, cashier must enter transaction
amount and include CVV.
* 3 chip failures -> fallback to magnetic stripe,
cashier must enter the transaction amount, but no CVV required.
* 3 chip failures -> fallback to magnetic stripe, customer swipes card.
* 1 chip failure -> fallback to magnetic stripe, customer swipes card.

So the mode where the cashier has to enter the entire transaction manually,
including the CVV, means that the vendor will get a better rate on processing,
but it might not be as good as the "chip and PIN". This method also offers the
most scrutiny of the transaction. Note- Most banks make "chip and PIN"
transactions zero liability for the bank and merchant, not for the customer.

All of the "3 chip failure" scenarios are very  interaction-heavy, there's
really no way for the cashier avoid noticing that there's something wrong; your
transaction isn't normal, and it's very slow.

It's the "1 chip failure" scenario, that's the most interesting, and easiest to
test: simply put the card into the reader using the wrong end(if you don't have
a broken card like I do). It seems that there is no conductivity test done, but
a simple physical detection mechanism(a switch, or possibly an IR beam break)
is used. The reason that I learned this is because a grocery store cashier
wanted to generate three failures as fast as possible, to get to the fallback,
so he could continue to do his job.

You're not going to be able to use the wrong end of the card three times, but
you can surely get away with it once, as "an honest" mistake.

What this illustrates is that if you have the physical card, you don't need to
know the PIN. The main goal of the merchant and credit card company is to have
you buy things, so there is a fallback mechanism that will always allow the
transaction to proceed, with the exception of deactivated cards. If you have a
lost/stolen credit card, don't assume that "chip and PIN" will save you, as you
can bypass it with "an honest mistake". Contact your issuer immediately to have
it deactivated.

If someone is more enterprising, they could remove a segment of the contact,
sever the connection and reattach it. (Update 2014-01-17: I missed an easier
method: a physical barrier, like clear nail polish. Credit @info_dox, who
credits UK researchers for finding this.) This allows them to get to the
fallback scenario every time, but will obviously will draw more attention to
the transaction.  There is a way to combat the fallback scenario, which is used
in the US, as "chip and PIN" is not common, and that's to check a photo ID. I
haven't had an ID checked at all during the time that my credit card's "chip
and PIN" has been broken. Not once.

As far as I can tell, the main attraction of "chip and PIN" for credit cards is
to move the liability from the issuer to the cardholder.
