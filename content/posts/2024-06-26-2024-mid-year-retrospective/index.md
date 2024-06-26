---
title: 2024 mid-year retrospective
authors:
- Chris Wilson
date: "2024-06-26"
draft: false
slug: 2024-mid-year-retrospective
tags:
- consulting
- retrospective
- Common Ground Electronics
- Golioth
disableComments: false
typora-copy-images-to: ./images
---

We're half-way through 2024 and summer is affording me some additional time to pause and reflect on my first year of consulting.

I figured it might be interesting to do a short post on how this business came into existance and what I've been up to over the last year.

# Starting Common Ground Electronics

I started [Common Ground Electronics](https://cgnd.dev/) back in November of 2022 as a part-time project.

If I'm being totally honest, I was initially just trying to figure out how I could start building out an electronics lab and write it off as a business expense. But, business expenses imply that some business is *actually being done*, so I started looking for my first part-time consulting client.

Serendipitously, I ran across [a post](https://chaos.social/@chris_gammell/109389167641322097) from [Chris Gammell](https://chrisgammell.com/) announcing a free developer training that [Golioth](https://golioth.io/) would be offering the following month. At the time, I had no previous experience working with Zephyr or Golioth, but this seemed like a good introduction to both–so I signed up!

Chris and I chatted after the training and he asked if I was interested in doing some contract engineering work for the developer relations team at Golioth. It had been a while since I had worked on anything IoT related, and I was excited for the opportunity to [get back to working on embedded systems](https://x.com/chrismakesstuff/status/1527045357414191104).

I registered an LLC, found an accountant, and started doing contract work for Golioth in early 2023. (BTW, let me know in the comments below if there is any interest in a follow-up post on starting an electronics consulting business.)

# Working for Golioth

This month wraps up just over a year of contract work for Golioth, so it seems like a good time for a quick retrospective. Luckily, most of the stuff I worked on is already public, so I can talk about it here.

Over the past year, I built and documented a [series of reference designs](https://projects.golioth.io) intended to help jumpstart new IoT product designs using the [Golioth Firmware SDK](https://docs.golioth.io/firmware/golioth-firmware-sdk/). This included spearheading Golioth's [Follow-Along Hardware](https://blog.golioth.io/instantly-recreate-sophisticated-iot-designs-with-follow-along-hardware/) initiative to support building reference designs with widely available off-the-shelf hardware. There's a nice summary discussion of a couple of of the projects I worked on in this [partner webinar with Nordic Semiconductor](https://www.youtube.com/watch?v=89Q4VwlqrJk).

I also helped the DevRel team bring up the new Aludel Elixir boards that [Golioth announced at EW2024](https://blog.golioth.io/demos-well-have-at-embedded-world-2024/). This included schematic review of the hardware design, writing all the [devicetree definitions](https://github.com/golioth/golioth-zephyr-boards/tree/main/boards/arm/aludel_elixir) for [multiple revisions of the board](https://blog.golioth.io/managing-board-revisions-in-zephyr/), and adding support for the board as a build target in the reference design firmware.

A big part of [Demo Culture at Golioth](https://blog.golioth.io/demo-culture-at-golioth/) is blogging about what you're working on. Zephyr has a pretty steep learning curve and I found myself frequently referencing the Golioth blog for guidance on a variety of Zephyr-related topics. Over my time working for Golioth, I was able to contribute a variety of Zephyr-related articles for their blog; you can see the full list of articles at https://blog.golioth.io/author/cdwilson/

Finally, I helped the Golioth DevRel team run [monthly Zephyr trainings](https://golioth.io/training-signup) designed to get embedded developers up to speed on the basics of Zephyr and Golioth. This was really fun to be a part of the same training that introduced me to Zephyr and Golioth in the first place!

# Open Source

As part of an [exploration into the use of pre-commit for embedded development](https://cgnd.dev/posts/enforce-zephyr-code-quality-pre-commit/), I open sourced https://github.com/cgnd/zephyr-pre-commit-hooks which is a collection of [pre-commit](https://pre-commit.com/) hooks for use with Zephyr.

I also made my first small contributions to upstream Zephyr in the last few months:

- [boards: shields: Add MikroElektronika Weather Click shield](https://github.com/zephyrproject-rtos/zephyr/pull/71076)
- [boards: shields: Add nRF9160 DK overlay for arduino_uno_click shield](https://github.com/zephyrproject-rtos/zephyr/pull/71106)

You can check out all of our open source projects on GitHub at https://github.com/cgnd/

# Looking Forward

In addition to authoring technical content for clients, I'm also starting to write about embedded systems and IoT-related topics on the [Common Ground Electronics blog](https://cgnd.dev/posts/). If there are topics of interest that you'd like me to write about, let me know in the comments below.

If you're interested in hiring me for technical writing (or other engineering related work), feel free to [reach out](https://cgnd.dev/contact/).
