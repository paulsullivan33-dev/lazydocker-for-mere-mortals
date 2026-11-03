# Limits

Outcome: you know where the tool's
edges are before you lean on them.
Every limit here was either met in the
lab or follows from the architecture
chapter 2 describes.

**It shows the daemon, and only the
daemon.** No daemon, no data: the
interface opens onto empty panels and
an error (transcript t04). Everything
you see has exactly the daemon's
authority and exactly its blind spots.

**An empty screen is not an empty
fleet.** A stopped daemon, a wrong
`DOCKER_HOST`, a dead events stream and
a genuinely idle machine can look
similar at a glance. The error popup is
the tell; train yourself to look for
it before concluding anything from an
empty list.

**It has no memory.** No history, no
recording, no alerts, no "what changed
while I was away". The stats graphs
span your watching session. A fleet
that must be *monitored* — paged at
3 a.m., trended over months — needs a
monitoring system; this is a window,
not a watchman.

**Reading is safe; the same keyboard
acts.** Stop, restart, remove, exec
and bulk commands sit one or two keys
from the arrows, aimed at whichever
daemon is connected. Confirmations
exist, but a confirmation read a
hundred times becomes a keystroke, not
a decision. The tool will not save you
from a confident mistake against the
wrong endpoint.

**It shows secrets because the daemon
reports them.** The Env tab prints
environment variables in plain sight,
including any credentials a container
was started with. Shoulder-surfing, a
shared screen in a video call, a
screenshot for a bug report — all
become disclosures. The tool treats
them as data; you must treat them as
keys.

**Compose actions are only as good as
the compose it can find.** The project
half runs a compose program by name;
the wrong name, or a compose too old
for the project file, fails in-panel
(the lab's `docker-compose: command
not found`, transcript t08) — and the
templates can be edited into shapes
the program will happily run verbatim.
Your templates, your responsibility.

**One daemon, one terminal, one
person.** No multi-host view, no users
or permissions of its own, no audit
log of who pressed what. Anything
requiring those is a different tool's
shape (chapter 11), not a setting.

**Numbers are the daemon's arithmetic,
kept honest only while the stream
lives.** CPU% comes from the stats
stream; when a stream stalls or a
container stops, a displayed number can
be a photograph of the past wearing
the present tense. The lab could verify
its fixture arithmetic exactly; it
could not test staleness against a real
daemon, and says so.

**The version you have is the doc you
can trust.** Panels, keys and templates
evolve between releases; the lab
exercised 0.25.2, and the in-program
menus — not this chapter — are the
authority for yours.
