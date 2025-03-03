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
    # 0.0.0.0 enables preview from other devices (e.g. mobile devices) on the
    # same network.
    dev_addr="0.0.0.0:8000",  # nosec
    open=True,
):
    cmd = " ".join(
        [
            "mkdocs",
            "serve",
            "--open" if open else "",
            f'--dev-addr="{dev_addr}"' if dev_addr else "",
        ]
    )
    context.run(cmd)
