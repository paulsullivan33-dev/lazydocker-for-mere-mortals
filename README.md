# Lazydocker for Mere Mortals

Docker's own commands are a fine set of
tools, but they answer one question at a
time: `docker ps` for what is running,
`docker logs` for what it said,
`docker stats` for what it is eating —
each in its own terminal, each stale the
moment it prints. **Lazydocker** is the
other shape: a single terminal screen
that shows your containers, images,
volumes and networks all at once, keeps
them current, and lets you read logs,
watch live statistics and act on what
you see, one keystroke at a time. It is
a small program you run on the machine
(or against the daemon) you already
have. Nothing is installed into Docker
itself, and nothing phones home.

This guide explains how lazydocker
thinks about Docker, how to install it,
and how to read everything on its
screen. Then it is honest about
something most tool guides never have to
say: **the lab behind this guide had no
Docker daemon at all** — the sandbox it
ran in has the Docker *client* installed
but no working daemon, and a bounded
attempt to start one was refused by the
kernel (`iptables … Permission denied`,
transcript t00). So the lab did the next
honest thing. It ran lazydocker against
the missing daemon and recorded exactly
what the program does then — it opens
its whole interface, shows empty panels,
and raises an error popup with a retry
counter. And it built a tiny **fake
Docker endpoint**: a stub program that
answers the Docker API over HTTP with an
invented fleet of four containers, five
images, three volumes and two networks.
Lazydocker — and, as a cross-check, the
real `docker` CLI — accepted the stub as
a daemon, and every panel, tab, log
stream and statistics graph in this
guide was rendered from that
conversation (transcripts t06–t10).

Two limits follow from that, and the
guide never hides them. Everything
*read-only* — the panels, the logs, the
stats graphs, the menus — is shown from
real runs. Everything that *changes*
state — stopping, restarting, removing,
attaching, exec — was never executed:
the lab opened the menus, read the keys,
and closed them again (the stub's
request log shows not one write request
in any session). Those operations are
taught from the program's own menus and
documentation and labelled
documented-only wherever they appear.
`criteria.md` keeps the full ledger.

## What this guide covers

- [**What lazydocker is**](what-lazydocker-is.md) —
  the mental model: one live screen
  over Docker's API, instead of one
  command per question
- [**The moving parts**](the-moving-parts.md) —
  the daemon that owns the truth, the
  API lazydocker speaks, the six panels,
  the main panel's five tabs, and the
  compose side that shells out
- [**Installing lazydocker**](installing-lazydocker.md) —
  the release download, the checksum
  check, and the version and help
  output that prove it runs
- [**Your first run**](your-first-run.md) —
  the opening screen, what each panel
  holds, and what the program does when
  there is no daemon to talk to
- [**Containers**](containers.md) —
  the container list read line by line:
  state, name, live CPU, published
  ports, and the menu of things you can
  do to one
- [**Logs, stats and details**](logs-stats-and-details.md) —
  the main panel's five tabs: following
  a log, the CPU and memory graphs,
  environment, full configuration, and
  the process list
- [**Images, volumes and networks**](images-volumes-and-networks.md) —
  the other three lists, what their
  detail views show, and what their
  menus offer
- [**Projects and services**](projects-and-services.md) —
  the compose half of the program: the
  Project and Services panels, and the
  compose commands lazydocker runs on
  your behalf
- [**Configuration and keys**](configuration-and-keys.md) —
  the one config file, printing the
  defaults, what a broken file does,
  and the keybindings worth learning
  first
- [**Recipes**](recipes.md) — a morning
  health check, auditing a fleet you
  inherited, watching a suspicious
  container, and pointing lazydocker at
  another machine's daemon
- [**The neighbours**](the-neighbours.md) —
  the Docker CLI itself, Portainer,
  Dockge, ctop and the lazygit family:
  what each does that lazydocker
  doesn't, and vice versa
- [**Limits**](limits.md) — a viewer
  with leverage but no memory, no
  alerts and no mercy for typos, and
  the rest of the honest list
- [**Troubleshooting**](troubleshooting.md) —
  the daemon that is not there, the
  config file that stops the program
  cold, the compose program it cannot
  find, and the traps this guide's lab
  fell into
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Running Docker itself: installing the
daemon, writing Dockerfiles and keeping
containers healthy are the Docker and
Docker Compose guides in this series,
and this one assumes a daemon exists
somewhere for lazydocker to watch.
Multi-machine fleets and access control
— who may point a dashboard at a
production daemon is a real question,
and chapter 12 explains why this tool
leaves it to you. And nothing here
teaches the state-changing keystrokes by
doing them: they are described from the
menus, with their confirmations, and
the doing is left to your machine and
your judgement.

## How to use this guide

Read chapter 1 for the model, and
chapter 2 before installing anything —
knowing which part holds what turns
later confusion into a named problem.
Chapter 3 installs; chapter 4 has the
screen in front of you in the same
sitting, even if your daemon is missing,
because chapter 4 starts with exactly
that case. Chapters 6 and 7 are the
daily-driving chapters; chapter 9 is
the one to read before you lend the
tool your habits. The lab's transcripts
live in `lazydocker-lab/transcripts/`;
the fake endpoint is
`lazydocker-lab/docker-stub.py`, the
terminal driver that captured the
screens is `lazydocker-lab/tui-driver.py`,
and the fixture compose file is
`lazydocker-lab/docker-compose.yml`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Docker for Mere Mortals](https://paulsullivan33-dev.github.io/docker-for-mere-mortals/)
- [Docker Compose for Mere Mortals](https://paulsullivan33-dev.github.io/docker-compose-for-mere-mortals/)
- [Portainer for Mere Mortals](https://paulsullivan33-dev.github.io/portainer-for-mere-mortals/)
- [lazygit for Mere Mortals](https://paulsullivan33-dev.github.io/lazygit-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/lazydocker-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/lazydocker-for-mere-mortals/blob/main/LICENSE-CODE).
