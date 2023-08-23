---
title: Enforce Zephyr code quality with pre-commit
authors:
- Chris Wilson
date: "2023-07-16"
draft: false
slug: enforce-zephyr-code-quality-pre-commit
tags:
- Zephyr
- pre-commit
- code quality
- code style
disableComments: false
typora-copy-images-to: ./images
---

![kites_on_hooks](images/kites_on_hooks.png)

In this article, I'll describe how embedded firmware developers can leverage [`pre-commit`](https://pre-commit.com/) to automate and enforce code quality checks in their Zephyr RTOS embedded firmware projects.

{{< notice note >}}

An earlier revision of this article recommended running `clang-format` as a pre-commit hook. While this is still possible, there are some downsides to running `clang-format` automatically via `pre-commit` (for example, `clang-format` formatting [does not 100% align](https://github.com/zephyrproject-rtos/zephyr/issues/52712#issuecomment-1516541794) with the Zephyr project coding style and needs some manual fixing).

I have updated this article to focus on using `pre-commit` to automatically run the Zephyr `checkpatch.pl` script as recommended by the [Zephyr project coding style](https://docs.zephyrproject.org/latest/contribute/guidelines.html#coding-style).

{{< /notice >}}

## What's the problem?

To prevent back-and-forth discussions over code style and improve code quality, many embedded development teams have adopted a set of "coding style" guidelines. However, if these style guidelines are simply written down in a README or some other project documentation, it's inevitable that those guidelines will be ignored.

Phillip Johnston from [Embedded Artistry](https://embeddedartistry.com/) wrote an excellent article [Creating and Enforcing a Code Formatting Standard with clang-format](https://embeddedartistry.com/blog/2017/10/23/creating-and-enforcing-a-code-formatting-standard-with-clang-format/) with this quote from MongoDB that bears repeating here:

> **A formatting process which is both manual and insufficient is doomed to be abandoned.**

Phillip's article is a fantastic deep-dive on how to use the [`clang-format`](https://clang.llvm.org/docs/ClangFormat.html) tool to automatically format code to comply with code formatting guidelines encoded in a `.clang-format` config file. In a [follow up article](https://embeddedartistry.com/blog/2017/11/02/a-strategy-for-enforcing-formatting-with-your-build-server/), he describes how to enforce these rules on a build server in a CI environment to ensure that all changes are checked for formatting before they are merged into the main branch.

He also mentions that it's possible to enforce formatting checks in a local development environment using [git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks), but points out the following caveat:

> […] the use of `git` hooks requires users to install the hooks on their end. It’s hard to fully enforce that flow, especially since you’re relying on developers to remember that hooks need to be installed.

The reality is that managing git hooks manually is painful and it's hard to enforce consistency across multiple developers, especially as those hooks change over time.

How do you make sure that everyone on your team is running the same set of pre-commit checks?

## A case for using `pre-commit` in Zephyr projects

Fortunately, there is a fantastic tool called [`pre-commit`](https://pre-commit.com/) that can automatically install, manage, and run `git commit` hooks, without requiring individual developers to manage these hooks manually. By shipping a single `.pre-commit-config.yaml` config with your embedded project, you can make it trivially easy for individual developers to run code quality checks and automatically enforce code style rules in their development environment. *And this all happens before the code is checked into git*. This can help ensure that code submitted for peer review is consistently formatted and matches the agreed-upon code style for the project, allowing discussions to focus on the actual content of the changes without devolving into code style arguments.

In addition to checking for code style issues such as formatting and linting, `pre-commit` can be configured to run other types of checks (linting, line-endings & whitespace, YAML file syntax issues, common code security issues, etc). There is a growing set of custom community-provided hooks in addition to the [ones provided out-of-the-box](https://github.com/pre-commit/pre-commit-hooks) by the developers.

For a great introduction to using `pre-commit` for embedded development in general, Noah Pendleton published an article on the Interrupt blog about how they [Automatically format and lint code with pre-commit](https://interrupt.memfault.com/blog/pre-commit) at Memfault.

At this point, you might be thinking "*I don't want to learn a new tool*" or "*I don't want to introduce additional dependencies*". However, I would argue that `pre-commit` actually simplifies the setup process for new developers vs. a manual approach.

First, if you're using Zephyr, you're probably already setting up a python virtual environment. Installing `pre-commit` for a Zephyr project is just two commands:

```sh
pip install pre-commit
pre-commit install
```

That's it! Once `pre-commit` is installed, the code quality checks will run automatically whenever a developer runs `git commit` in their local development environment. No more having to manually run checks before committing!

Second, if you're already using west manifest files to manage dependencies for your project's source code, you will find `.pre-commit-config.yaml` to be familiar in concept. Just as `west.yml` can be used to lock the specific revision for each source code dependency, the `.pre-commit-config.yaml` file is used to lock the specific revision for each code quality check you want to run. Just check this file into the git repo for your project, and all developers on your team will run the exact same set of checks.

## What checks should I run?

The Zephyr project [Coding Style](https://docs.zephyrproject.org/latest/contribute/guidelines.html#coding-style) recommends using a modified version of the Linux kernel  [`checkpatch.pl`](https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/checkpatch.pl) tool shipped with Zephyr, along with the provided [`.checkpatch.conf`](https://github.com/zephyrproject-rtos/zephyr/blob/main/.checkpatch.conf) file. This is a good place for us to start when setting up pre-commit checks in our Zephyr application.

The remainder of this article is going to describe how to configure `pre-commit` to automatically run Zephyr's `checkpatch.pl` before each `git commit`. This will flag any code style issues present in our project code before we commit any changes.

If you don't already have existing code style guidelines required by your team or project, I would recommend simply copying [`.checkpatch.conf`](https://github.com/zephyrproject-rtos/zephyr/blob/main/.checkpatch.conf) from the Zephyr project as a starting point. For example, if your project follows the recommended layout in the Zephyr [example-application](https://github.com/zephyrproject-rtos/example-application), you can copy this file into your application as follows:

```sh
cd example-application-workspace/
cp zephyr/.checkpatch.conf example-application/.checkpatch.conf
```

{{< notice note >}}

You'll need to change the following line in `.checkpatch.conf` to match the location of the `typedefsfile` file in your project (in this example, I'm just using the one included in the Zephyr repository):

```plaintext
--typedefsfile=../zephyr/scripts/checkpatch/typedefsfile
```

If this path is set up incorrectly, you'll get an error that looks like this:

```plaintext
No additional types will be considered - file '../foo/bar/typedefsfile': No such file or directory
```

{{< /notice >}}

Check these config files into the root of your project's git repository.

## How to configure `pre-commit` in a Zephyr project

Now that we've got the `.checkpatch.conf` config file in our project repo, we can create a `pre-commit` config to run these checks. For the remainder of this article, I'm going to assume your project follows the recommended layout in the Zephyr [example-application](https://github.com/zephyrproject-rtos/example-application), but it should be simple to adapt this to your project layout.

First, we need to add an empty `pre-commit` config file to our project repo:

```plaintext
example-application-workspace/example-application/.pre-commit-config.yaml
```

`pre-commit` hooks are just git repositories and they are specified in the `.pre-commit-config.yaml` file as a list of values under the `repos` key. Each hook has a:

- `repo` key that contains the URL of the git repository
- `rev` key that contains the specific revision of the hook
- `hooks` key that describes the hooks to run (repos can contain multiple hooks)

Next, we'll add a hook that runs Zephyr's `checkpatch.pl` (using the `.checkpatch.conf` config file we added earlier):

```yaml
repos:
  - repo: https://github.com/cgnd/zephyr-pre-commit-hooks
    rev: v1.0.0
    hooks:
    - id: zephyr-checkpatch-diff
```

{{< notice note >}}

Unfortunately, Zephyr's checkpatch does not currently work on Windows 😿

{{< /notice >}}

Finally, check in the `.pre-commit-config.yaml` file into your project's git repository.

Now we're ready to install and run pre-commit.

## How to install and run pre-commit

As mentioned earlier, it's simple to install the `pre-commit` tool:

```sh
pip install pre-commit
```

Next, run the following command to install the git hooks:

```sh
cd example-application-workspace/example-application/
pre-commit install
```

{{< notice note >}}

NOTE: The `zephyr-checkpatch-diff` hook we added requires that the [Zephyr environment scripts](https://docs.zephyrproject.org/latest/develop/env_vars.html#zephyr-environment-scripts) have been run. Run the following command to set up the Zephyr environment variables (this must be run for each new terminal session):

```sh
source example-application-workspace/zephyr/zephyr-env.sh
```

{{< /notice >}}

The `zephyr-checkpatch-diff` hook we added will run checks on any staged changes that we're trying to commit (i.e. it will only check the output of `git diff --cached` and does NOT check entire files).

To show how this works, let's make some changes in the project's `main.c` to violate Zephyr's coding style:

```diff
 #include <zephyr/logging/log.h>
 LOG_MODULE_REGISTER(main, CONFIG_APP_LOG_LEVEL);

-int main(void)
-{
-       int ret;
+int main(void) {
+       int new;
        const struct device *sensor;

        printk("Zephyr Example Application %s\n", APP_VERSION_STRING);
```

Let's see what happens when we try to commit this change:

```plaintext
❯ git add app/src/main.c
❯ git commit -m "Change variable name"
Run Zephyr's checkpatch.pl...............................................Failed
- hook id: zephyr-checkpatch-diff
- exit code: 1

-:12: ERROR:OPEN_BRACE: open brace '{' following function definitions go on the next line
#12: FILE: app/src/main.c:13:
+int main(void) {

- total: 1 errors, 0 warnings, 11 lines checked
```

In this example, `checkpatch.pl` checks failed because the Zephyr coding style requires that open braces go on the next line after function definitions.

After fixing the error (by moving the open brace to the next line), we can `git add` the modified files:

```plaintext
❯ git add app/src/main.c
```

When we try to commit again, all the checks pass!

```plaintext
❯ git commit -m "Change variable name"
Run Zephyr's checkpatch.pl...............................................Passed
[test 689d9c0] Change variable name
 1 file changed, 1 insertion(+), 1 deletion(-)
```

## Tips & Tricks

#### What to do when `clang-format` and `checkpatch.pl` disagree

You may run into cases where Zephyr's `.clang-format` and `.checkpatch.conf` disagree on code style (in the Zephyr project, `clang-format` is [not intended to be a one-stop solution to all the code style issues](https://github.com/zephyrproject-rtos/zephyr/issues/52712#issuecomment-1516541794)).

For example, here's how `clang-format` will format the following code using Zephyr's `.clang-format`:

```C
static const struct divider_config divider_config = {
	.io_channel =
		{
			DT_IO_CHANNELS_INPUT(VBATT),
		},
	.power_gpios = GPIO_DT_SPEC_GET_OR(VBATT, power_gpios, {}),
	.output_ohm = DT_PROP(VBATT, output_ohms),
	.full_ohm = DT_PROP(VBATT, full_ohms),
};
```

If we try to commit this, `checkpatch.pl` will fail because it thinks that the `{` should be on the same line as `.io_channel =`:

```plaintext
Run Zephyr's checkpatch.pl...............................................Failed
- hook id: zephyr-checkpatch-diff
- exit code: 1

-:15: ERROR:OPEN_BRACE: that open brace { should be on the previous line
#15: FILE: src/battery_monitor/battery.c:87:
+       .io_channel =
+               {

- total: 1 errors, 0 warnings, 24 lines checked
```

You can resolve this conflict by using special comments to tell `clang-format` to skip formatting on certain lines in the file:

```C
static const struct divider_config divider_config = {
	/* clang-format off */
	.io_channel = {
		DT_IO_CHANNELS_INPUT(VBATT),
	},
	/* clang-format on */
	.power_gpios = GPIO_DT_SPEC_GET_OR(VBATT, power_gpios, {}),
	.output_ohm = DT_PROP(VBATT, output_ohms),
	.full_ohm = DT_PROP(VBATT, full_ohms),
};
```

Now, if you try to commit this, `checkpatch.pl` checks will pass.

#### How to skip running `pre-commit` hooks if necessary

There may be times when `pre-commit` is failing but you need to commit anyway.

To skip all `pre-commit` hooks, add the `--no-verify` switch to the `git commit` command:

```sh
git commit --no-verify -m "foo"
```

To skip one or more hooks, you can set the `SKIP` environment variable to a comma separated list of hook ids:

```sh
SKIP=zephyr-checkpatch-diff git commit -m "foo"
```

#### Automatically install `pre-commit` hooks when a repo is cloned

You can configure `git init` to automatically install `pre-commit` hooks when a new repository is cloned (rather than having to run `pre-commit install` manually).

Follow the recommended setup instructions at https://pre-commit.com/#pre-commit-init-templatedir

## Example Repo

If you would like to check out an example Zephyr application with a `pre-commit` config, I've added a [pre-commit branch](https://github.com/cgnd/example-application/tree/pre-commit) to my fork of the Zephyr `example-application` repo. Here's a direct link to the `.pre-commit-config.yaml` file:

https://github.com/cgnd/example-application/blob/pre-commit/.pre-commit-config.yaml

## Revision History

| **Revision** | **Date**   | **Description**            |
| ------------ | ---------- | -------------------------- |
| 1            | 2023-07-16 | Initial release            |
| 2            | 2023-08-23 | Remove `clang-format` hook |

## Feedback

If you are using `pre-commit` (or something like it) as part of your embedded development workflow, let me know in the comments below! I'd love to learn more about how other embedded teams are using tools like this in their workflow.
