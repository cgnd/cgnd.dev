---
title: "USB-over-IP in Docker Containers"
authors:
- "Chris Wilson"
date: "2024-12-06"
draft: false
slug: usb-over-ip-in-docker-containers
images:
- images/usb-docker.webp
description: "Today I learned Docker recently introduced USB/IP protocol support in Docker Desktop version 4.35.0."
series:
- "Today I learned"
tags:
- "TIL"
- "Docker"
- "VirtualHere"
- "USB/IP"
disableComments: false
typora-copy-images-to: ./images
---

![usb-docker](images/usb-docker.webp)

**[Today I learned](/series/today-i-learned/)** Docker recently introduced [USB/IP protocol support](https://docs.docker.com/desktop/features/usbip/) in Docker Desktop version [4.35.0](https://docs.docker.com/desktop/release-notes/#4350). Since Docker containers do not support native USB passthrough, this feature makes it possible for Docker containers to remotely access USB devices attached to a machine running Docker Desktop. This is exciting because it opens the door to using Docker containers for embedded development workflows that need to access real hardware via USB.

There is a great introductory article on the Golioth blog by founder and CEO Jonathan Beri, where he describes how he worked with the Docker team to integrate USB/IP support into Docker Desktop. The article walks through setting up a USB/IP server and how to connect to USB devices from a Docker container running in Docker Desktop.

https://blog.golioth.io/usb-docker-windows-macos/

In that article, Jonathan points out a couple limitations of the USB/IP approach on macOS:

> Unfortunately, macOS doesn’t have a complete server but I was able to use [this Python library](https://github.com/tumayt/pyusbip) to program a development board (I also tried this [Rust library](https://github.com/jiegec/usbip) but it’s [missing support](https://github.com/jiegec/usbip/issues/55) for USB to serial devices). Developing a USB/IP server for macOS is certainly one area the community can contribute!

I'm hopefully optimistic that there will eventually be a robust open-source USB/IP server for macOS.

But, if you need a cross platform solution that works today, and you are OK paying for a commercial product, a good alternative is [VirtualHere](https://www.virtualhere.com/). VirtualHere is a mature USB-over-IP solution that supports Mac, Windows, and Linux. I put together a simple test repository with an example `Dockerfile` showing how to connect to USB devices from within a Docker container.

Check it out here: https://github.com/cgnd/docker-virtualhere-client

In theory, this all seems pretty neat. However, after testing both of the USB-over-IP solutions above, I found that the current limitations/setup overhead are still too much of an annoyance for me to integrate them into my normal day-to-day development workflow.

If you're successfully using tools like these for interacting with USB devices in Docker containers, let me know in the comments below!
