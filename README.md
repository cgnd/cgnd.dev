# cgnd.dev

Common Ground Electronics website published at https://cgnd.dev

## Local Development Environment

Install `uv` by following the instructions at https://docs.astral.sh/uv/getting-started/installation/

Clone this repository:

```sh
git clone git@github.com:cgnd/cgnd.dev.git
cd docs/
```

Create a Python virtual environment:

```sh
uv venv
```

Activate the virtual environment:

```sh
source .venv/bin/activate
```

Install Python dependencies:

```sh
uv pip install -r requirements.txt
uv pip install -r dev-requirements.txt
```

## Local Build & Preview

Run the builtin development server:

```sh
inv preview
```

## Build & Deploy

[![Netlify Status](https://api.netlify.com/api/v1/badges/4f1dafc4-19c4-4054-b0ea-ccb5b6d71110/deploy-status)](https://app.netlify.com/sites/cgnd-dev/deploys)

## Licenses

See the [LICENSE](LICENSE.md) file for copyright & license information.
