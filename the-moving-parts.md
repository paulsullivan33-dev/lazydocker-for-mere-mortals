# The Moving Parts

Outcome: you can name every part of the
system and say which part holds what,
so that when something looks wrong you
know which part to suspect. The check
is at the end: five questions the model
answers.

## The daemon owns the truth

The **Docker daemon** (`dockerd`) is the
background program that creates, runs
and destroys containers. It is the only
part that touches the kernel, the only
part that knows — as opposed to guesses —
what is running. Everything else in this
chapter is a way of asking it questions.

Our lab machine makes the point by
absence: the Docker *client* is
installed there (version 29.1.3) but
there is no daemon and no socket, and
`docker info` answers for the client
and then refuses for the server —
`failed to connect to the docker API at
unix:///var/run/docker.sock`
(transcript t00). Client without daemon
is a telephone without a line.

## The API is the conversation

The daemon answers questions over the
**Docker Engine API**, an ordinary HTTP
interface, usually reached through the
socket file `/var/run/docker.sock`, or
over TCP when `DOCKER_HOST` points
elsewhere. The lab's fake endpoint
logged every question lazydocker asked
(transcript t10), and the list is the
tool's whole curiosity, in order of
appetite:

- a **ping** (`/_ping`, then `/version`)
  to find out who is answering;
- the **lists**: `/containers/json`,
  `/images/json`, `/volumes`,
  `/networks`;
- an **inspect** of every container
  (`/containers/<id>/json`), re-asked
  constantly — nineteen times per
  container in one short session. That
  polling is the refresh you see;
- a **stats stream** per running
  container, which feeds the CPU column
  and the graphs;
- a **log follow** for whichever
  container is selected;
- one **events** stream, so the daemon
  can announce changes instead of
  waiting to be asked.

Two consequences matter. First, anything
that can answer this API can feed
lazydocker — the lab's stub, a few
hundred lines of Python returning
invented JSON, was accepted by both
lazydocker and the real `docker` CLI
(transcript t06). Second, lazydocker's
loyalties are to the endpoint, not the
machine: point `DOCKER_HOST` at another
daemon and the same screen shows that
machine's fleet. Chapter 10's last
recipe uses this on purpose; chapter
12 counts it as a risk as well.

## The six panels

The screen lazydocker draws is six
numbered panels down the left and one
large main panel. From the lab's runs:

- **[1] Project** and **[2] Services** —
  the compose half (chapter 8). They
  read a compose project: its services,
  their state, and the project's own log.
- **[3] Containers**, **[4] Images**,
  **[5] Volumes**, **[6] Networks** —
  the daemon's four lists, always
  present. In the lab's renders they
  fill the left column; panels 1 and 2
  stayed folded away there (no compose
  project was detected through the stub)
  but still answered to their number
  keys — pressing `1` switched the main
  panel to the Project view and produced
  its error (transcript t08).

Selecting a row anywhere asks the daemon
for that thing's detail, which is what
the main panel is for.

## The main panel and its five tabs

For a container, the main panel carries
five tabs, cycled with `[` and `]` when
the main panel has focus (press `enter`
to give it focus): **Logs**, **Stats**,
**Env**, **Config** and **Top**. Every
one of them was rendered in the lab
(transcript t09): the followed log, the
CPU and memory graphs drawn from the
stats stream, the environment variables
from inspect, the inspect data itself,
and the process list from the daemon's
top endpoint. Images get a detail view
with their layer history; volumes and
networks get a config view. Chapter 6
and 7 walk them.

## The compose side shells out

Half of lazydocker does not use the API
at all. For project work it runs the
compose program as a subprocess — the
default configuration (printable with
`lazydocker --config`, transcript t03)
is a page of command templates:
`docker compose up -d`, `docker compose
restart`, `docker compose logs
--follow`, and so on. The lab caught
the seam precisely: the Project view
printed `bash: line 1: docker-compose:
command not found` (transcript t08),
because that view looked for a compose
binary this machine does not carry.
When a lazydocker action surprises you,
it is usually worth asking which of the
two halves — API or subprocess — you
are looking at.

## The config file

One YAML file steers the program:
`~/.config/lazydocker/config.yml`. The
first run creates it *empty* — the lab
verified: created, zero lines, meaning
"all defaults" (transcript t04). The
defaults themselves are printable
without starting the interface
(`lazydocker --config`, transcript t03):
theme colours, panel widths, the log
window (`logs.since: 60m`), the compose
command templates, and the bulk
commands. Chapter 9 is about changing
it — and about how an invalid file
stops the program cold, with the YAML
error as its only output.

## The check

1. `docker ps` fails but lazydocker
   opens — what is each program missing?
   (The daemon; the client inside both
   has nothing to talk to.)
2. Your screen shows a container you
   deleted an hour ago. Which stream
   should have told lazydocker, and what
   does its polling do if the stream
   dies? (Events; the inspect polling
   keeps the lists honest regardless.)
3. A panel shows different numbers from
   `docker stats`. Which program is
   wrong? (Neither by definition — both
   read the same stats stream; check
   you are pointed at the same daemon.)
4. The Project view errors but
   Containers is fine. Which half of the
   tool is unhappy? (The subprocess
   half — compose — not the API half.)
5. You set `DOCKER_HOST` and the fleet
   on screen is not yours. What happened,
   in one sentence? (Lazydocker shows
   whichever daemon the endpoint names;
   the endpoint is the loyalty.)
