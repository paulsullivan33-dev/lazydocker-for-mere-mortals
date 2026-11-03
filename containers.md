# Containers

Outcome: you can read the Containers
panel like a status board — state, load
and exposure at a glance — and you know
exactly which keys act on a container
and what the program asks before it
obeys. The acting keys themselves are
described from the program's own menu,
drawn in the lab; the lab never
executed one (see "What was and wasn't
pressed", below).

## Reading a row

The lab's fixture rows (transcript
t07):

```text
running     cache-box      25.00%
running     hello-web      25.00% 8080->80/tcp
running     scratch-db     25.00%
exited  (0) nightly-backup 25.00%
```

Four facts per row:

- **State.** `running`, or `exited`
  with the exit code in brackets —
  `exited (0)` is a job that finished
  cleanly; a non-zero code is a job that
  failed, and its log (chapter 6) is
  where the story is.
- **Name.** The container's name, not
  its image: the *instance*, which is
  the thing you can stop, follow and
  inspect.
- **CPU%.** Live, from the stats stream
  — the same numbers `docker stats`
  prints, kept current instead of
  printed once. (The fixture stream
  makes every lab container read
  exactly 25.00%; yours will move.)
  One honest caveat the lab could not
  test: an exited container has no
  stream, and the column then shows
  whatever the last poll left — treat a
  still number on a stopped row as a
  photograph, not a pulse.
- **Ports.** Published mappings only,
  `public->private/protocol`. A row
  with no ports is reachable only from
  inside Docker's networks — often the
  right shape for a database, and worth
  noticing when it is *not* what you
  intended for a web service.

The list re-sorts and refreshes itself;
new containers appear, gone ones
vanish, driven by the daemon's events
and lazydocker's own polling (chapter
2). Pressing `e` hides or shows the
stopped containers — the tidy view and
the true view are one key apart, and
for diagnosis you usually want the
true one.

## The menu: what one key offers

Select a container and press `x`. The
lab drew this menu and closed it with
`esc` (transcript t09):

```text
d     remove
e     hide/show stopped containers
p     pause
s     stop
r     restart
a     attach
m     view logs
E     exec shell
c     run predefined custom command
b     view bulk commands
w     open in browser (first port is http)
enter focus main panel
[     previous tab
]     next tab
```

Read it as three groups. **Looking**:
`m` (the Logs tab), `enter`, `[`/`]`,
`w` (opens the container's first port
in your browser — convenient, and
worth a thought about which daemon you
are browsing). **Talking**: `a` attach
(connect your terminal to the
container's own console, the way
`docker attach` does), `E` exec shell
(a new shell inside the container —
the most powerful item on the menu and
the one to be surest about; chapter 12
returns to it). **Changing**: `p`
pause, `s` stop, `r` restart, `d`
remove, `c` a custom command you
defined in the config file (chapter 9).

The changing keys ask first. Stop and
restart confirm; remove confirms and,
for a running container, is refused by
the daemon unless forced through the
follow-up prompt. This guide describes
that behaviour from the program's
menus and documentation — it is
documented-only, deliberately: the
lab's endpoint could not really stop
anything, and a menu photographed is
evidence of the offer, not of the act.

## What was and wasn't pressed

So the record is plain: in the lab,
containers were selected, their logs,
stats, environment, configuration and
process lists read, their menu opened
and closed. No stop, restart, remove,
pause, attach or exec was ever sent —
the stub's request log contains zero
write requests across all sessions
(transcript t10). On a real daemon
those keys do exactly what their names
say, with the confirmations above;
learn them on a container you can
afford to bounce. Chapter 10's recipes
stay on the read-only side throughout.
