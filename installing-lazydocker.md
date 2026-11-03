# Installing Lazydocker

Outcome: lazydocker on your machine,
from the project's own release, with the
download checked against the project's
checksum and the version command to
prove it runs. You need Docker already
working for the tool to be *useful*,
but — as the lab shows — not for it to
start.

## What you are downloading

Lazydocker is a single static program
written in Go, published by its author
(Jesse Duffield, of lazygit) as release
archives on GitHub. One archive per
operating system and architecture, one
binary inside, no installer, no runtime
to feed it. The lab exercised
**lazydocker 0.25.2** (built 2026-04-19,
commit `7e7aadc`), the current release
on the day of the lab.

## The install, as the lab ran it

Download the archive for your platform
and the release's checksum file, from
the project's releases page:

```bash
curl -sLO https://github.com/jesseduffield/lazydocker/releases/download/v0.25.2/lazydocker_0.25.2_Linux_x86_64.tar.gz
curl -sLO https://github.com/jesseduffield/lazydocker/releases/download/v0.25.2/checksums.txt
```

Check the archive against the checksum
before you open it. The lab's hash
matched the published one exactly
(transcript t01):

```bash
sha256sum lazydocker_0.25.2_Linux_x86_64.tar.gz
# 0d9dbfc26068b218e7ed84b104748cadc6e3cf733c0afd35465306fb39b9523c
grep Linux_x86_64 checksums.txt | sha256sum -c -
# lazydocker_0.25.2_Linux_x86_64.tar.gz: OK
```

Unpack it somewhere on your `PATH` —
`/usr/local/bin` for the whole machine,
`~/bin` for just you:

```bash
tar xzf lazydocker_0.25.2_Linux_x86_64.tar.gz
sudo install -m 0755 lazydocker /usr/local/bin/
```

The archive also carries the project's
own `README.md` and `LICENSE`; the
binary is the only part you need.

Package routes exist — Homebrew on macOS
and Linux, the Arch and Nix package
sets, a Scoop bucket on Windows — and
the project's README keeps the current
list. The release archive is the route
this guide verified; the program is the
same either way, and the check below
cannot tell them apart.

## The checks that prove it

Two commands, both run in the lab
(transcripts t01 and t02):

```bash
lazydocker --version
```

```text
Version: 0.25.2
Date: 2026-04-19T02:51:21Z
BuildSource: binaryRelease
Commit: 7e7aadc2071d58031bf2daafca1fbd4093efc23f
OS: linux
Arch: amd64
```

```bash
lazydocker --help
```

```text
lazydocker - The lazier way to manage everything docker
https://github.com/jesseduffield/lazydocker

  Flags:
       --version   Displays the program version string.
    -h --help      Displays help with available flag, subcommand, and positional value parameters.
    -c --config    Print the current default config
    -d --debug     a boolean
    -f --file      Specify alternate compose files
    -p --project   Specify a docker compose project name
```

The whole flag list fits on one screen,
which tells you something true about the
tool: almost everything it does is done
from inside the interface, not from the
command line. The two flags worth
remembering now are `-p` (open on a
named compose project) and `-f` (name
the compose files to read); chapter 8
uses them. `--config` prints the
built-in defaults and is chapter 9's
starting point.

One more check, the honest one. This
proves the *program* runs. Whether it
has anything to show you is the
daemon's business:

```bash
docker info >/dev/null && echo daemon answers
```

If that fails, install or start Docker
first — the Docker guide in this series
covers it — and read chapter 4 anyway:
it begins with exactly your situation.
