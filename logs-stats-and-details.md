# Logs, Stats and Details

Outcome: for any container you can pull
up its voice (the log), its appetite
(the stats graphs), its settings (Env
and Config) and its contents (Top) —
all five tabs, all rendered live in the
lab against the fixture endpoint.

Give the main panel focus with `enter`
from a selected container, then walk
the tabs with `]` and `[`. The tab bar
reads:

```text
Logs - Stats - Env - Config - Top
```

## Logs — the container's voice

The default tab, and the one the main
panel opens on. Lazydocker follows the
selected container's log the way
`docker logs --follow` does: the recent
lines on arrival, new lines as they
come. The lab's capture shows the
fixture lines arriving for two different
containers as the selection moved
(transcript t07, t08) — five invented
lines each, standing in for whatever
yours would say.

Two settings matter. The default config
asks the daemon for the last hour
(`logs.since: 60m`, transcript t03); a
container that has been quiet for
longer opens with an empty log that is
*old*, not broken. And the follow is a
live stream: leave the tab and the
stream closes (the lab's request log
shows one follow per selection,
transcript t10). `PgUp`/`PgDn` scroll
back through what has arrived.

## Stats — appetite as graphs

The Stats tab draws two graphs from the
same stream that feeds the CPU column:
CPU percent and memory percent, plotted
over the last stretch of samples.
The lab's version (transcript t09):

```text
 25.00 ┤
 25.00 ┼───────────────────────
          CPU (%): 25.00 (16s)
 0.51 ┤
          (memory graph below)
```

Because the fixture stream is honest
arithmetic, the lab could check the
graph against its inputs: a CPU delta
of 0.5 seconds over a 2.0-second system
delta is 25.00%, and 42 MB used of an
8.3 GB limit is 0.51% — both exactly as
drawn. On a real fleet these graphs are
the fastest answer to "is it busy, or
is it stuck?": a flat line at a round
ceiling usually means a limit, a saw
tooth means a batch job breathing, and
a line that stops entirely while the
container still claims `running` is a
story the Logs tab should be asked to
explain.

Remember the shape of the evidence: the
graphs show *since you started
watching*. There is no yesterday in
them — chapter 12 counts this among
the tool's real limits.

## Env — what it was told

The Env tab lists the environment
variables from the container's inspect
record. The lab's fixture carries one
line (transcript t09):

```text
PATH: /usr/local/bin:/usr/bin:/bin
```

Yours will carry more, and this tab
deserves a careful read on any
inherited fleet: it is where database
addresses, feature flags — and,
embarrassingly often, passwords passed
the easy way — sit in plain sight.
Lazydocker shows them because the
daemon reports them; chapter 12 treats
that as a handling warning, not a
feature to celebrate.

## Config — the whole inspect record

The Config tab renders the inspect
answer as readable fields: ID, name,
image, command, labels, and the rest.
The lab's capture of hello-web shows
its compose labels
(`com.docker.compose.project: harbour`)
— which is how the program knows this
container belongs to a project
(transcript t09). When the Panels and
`docker inspect` disagree about a
container, this tab is the tiebreaker:
it is the inspect data itself, without
the JSON thicket.

## Top — who is inside

The Top tab asks the daemon for the
container's process list
(`/containers/<id>/top`, transcript
t10) and draws it as a table:

```text
UID  PID  TIME CMD
root 1234 2h   /start.sh
```

One row for a healthy single-purpose
container is the expected sight. Twenty
rows, or a shell you do not recognise,
is a finding. It is the read-only
cousin of the exec shell: it shows the
processes without joining them.

`esc` returns focus to the list when
you are done. The next chapter gives
the other three panels the same
treatment.
