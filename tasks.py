# SPDX-FileCopyrightText: Common Ground Electronics <https://cgnd.dev>
#
# SPDX-License-Identifier: MIT OR Apache-2.0

import sys

if sys.version_info >= (3, 11):
    import inspect

    if not hasattr(inspect, "getargspec"):
        inspect.getargspec = inspect.getfullargspec

from invoke import task


@task(
    auto_shortflags=False,
)
def preview(
    context,
    fast_render=False,
    build_drafts=True,
    # default bind address is 127.0.0.1, 0.0.0.0 enables preview from other
    # devices (e.g. mobile devices) on the same network.
    bind_addr="0.0.0.0",  # nosec
    base_url="",
    port="",
):
    cmd = " ".join(
        [
            "hugo",
            "server",
            "" if fast_render else "--disableFastRender",
            "--buildDrafts" if build_drafts else "",
            f'--bind="{bind_addr}"' if bind_addr else "",
            f'--baseURL="{base_url}"' if base_url else "",
            f'--port="{port}"' if port else "",
        ]
    )
    context.run(cmd)
