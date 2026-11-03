# What Lazydocker Is

You run a handful of containers — a web
server, a database, a backup job — and
the questions you ask about them are
always the same few. What is running?
What did it just say? Why is it eating
the processor? Did the thing I restarted
actually come back? Docker's command
line answers each question well, one at
a time, in a fresh printout that starts
going stale immediately. Keeping watch
means re-typing.

**Lazydocker is the watch, kept for
you.** It is a program that draws your
whole Docker setup on one terminal
screen and keeps it current: containers
on the left with their state and live
processor use, images, volumes and
networks below them, and a large main
panel that shows the selected thing in
detail — its log as it grows, its CPU
and memory as graphs, its environment,
its full configuration. You move around
with the arrow keys, act with single
letters, and quit with `q`. It does
nothing a Docker command cannot do; it
just refuses to make you re-ask.

Underneath, lazydocker is a *client*. It
holds no containers and keeps no state
of its own. Everything on its screen
comes from the **Docker daemon** — the
background program that actually runs
your containers — asked over the
**Docker API**, the same questions the
`docker` command asks. Chapter 2 makes
that relationship precise, because it
explains both the tool's reach and its
limits: unplug the daemon and
lazydocker has nothing to show you, as
this guide's lab demonstrates on
purpose.

## A first taste

With Docker running and lazydocker
installed (chapter 3), the whole tool is
one word:

```bash
lazydocker
```

The screen that opens is the subject of
chapter 4. Its left edge, from the
lab's own run, looks like this
(transcript t07):

```text
╭─[3]─Containers──────────────────╮
│running     cache-box      25.00%│
│running     hello-web      25.00%│
│running     scratch-db     25.00%│
│exited  (0) nightly-backup 25.00%│
╰─────────────────────────────────╯
```

Four containers with their state, name,
live CPU and — for hello-web — its
published port, refreshing on their
own. The names are the lab's invented
fixtures; yours will be your own fleet.

## The line it walks, stated early

Lazydocker is a viewer with leverage.
Reading is safe, but the same screen
that shows you a container's log offers,
one key away, to stop it, restart it, or
remove it — against whichever daemon it
is connected to, including a production
one you reached by setting one
environment variable. The program does
ask before the destructive choices, and
chapter 5 shows those menus as they
were drawn in the lab. But the honest
rule belongs here, before any procedure
depends on it: **know which daemon you
are pointed at before you press
anything but an arrow key.** The last
line of every screen names the version,
not the target; the target is your
responsibility. Chapter 10 shows how to
check, and chapter 12 returns to it.

## What it is not

It is not a Docker replacement: it
cannot run a single container without
the daemon, and when the daemon is gone
it shows you empty panels and an error
(transcript t04). It is not a monitoring
system: it keeps no history, sends no
alerts, and forgets everything when you
quit — chapter 12 is plain about the
difference between *watching* and
*monitoring*. It is not a web console:
for a browser interface with user
accounts, that is Portainer's shape
(chapter 11). And it is not an image
builder or a compose editor: it *runs*
compose commands for a project it finds,
but the files themselves are written
with your editor, as the Docker Compose
guide teaches.

## Who it is for

The person with one machine and a
handful of containers who is tired of
typing `docker ps`, `docker logs`,
`docker stats` in rotation. The person
who inherited a small fleet and wants to
see all of it before touching any of it.
The compose user who restarts services
often enough that a menu beats a
command line. If your containers are
spread over a cluster with its own
dashboards, or your organisation needs
an audit trail of who stopped what,
chapter 11 points at the shapes that
fit better.
