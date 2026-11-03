# Configuration and Keys

Outcome: you can shape lazydocker with
its one config file, you know how to
see every default without guessing, and
you have met the small set of keys that
covers almost all daily work. The
config behaviours in this chapter —
creation, rejection, and a value taking
effect — were all run in the lab.

## The file, and its strange beginning

The config lives at
`~/.config/lazydocker/config.yml`. The
first run creates it **empty**
(transcript t04): zero lines, which the
program reads as "defaults, all of
them". You do not write a whole config;
you write only the lines you are
changing, and everything you omit keeps
its default. That is a kind design with
one sharp edge — an empty file and a
missing file behave the same, so "did
my edit load?" is a real question,
answered below.

## Seeing the defaults

```bash
lazydocker --config
```

prints the built-in configuration
without opening the interface
(transcript t03). Keep the output; it
is the reference for every key you
might set. The sections:

- **`gui`** — theme colours, border
  style, `sidePanelWidth` (0.3333: the
  list column's share of the screen),
  `screenMode`, whether the bottom line
  shows, how container health is
  spelled (`containerStatusHealthStyle:
  long`).
- **`logs`** — `since: 60m`, the window
  the Logs tab asks for on arrival.
- **`commandTemplates`** — the compose
  command lines of chapter 8, including
  `dockerCompose: docker compose`, the
  name of the compose program itself.
- **`bulkCommands`** — the named
  fleet-wide commands behind the `b`
  popup.

## Changing something, and proving it

The lab's change (transcript t05):

```yaml
gui:
  sidePanelWidth: 0.5
```

Run against the same screen as the
default run, the side column visibly
widened from a third of the 140-column
terminal to half. That is the pattern
for every config edit in this guide:
change one thing, restart the program,
look for the difference. Two more
edits worth considering early: a
`gui.theme.activeBorderColor` you can
spot across a room (the colour of the
focused panel's border is your "where
am I" signal), and `logs.since` widened
if your containers are quiet talkers.

## The broken file stops everything

Config errors are not warnings.
A YAML syntax error (transcript t05):

```text
2026/11/03 02:18:51 yaml: line 2: did not find expected ',' or ']'
```

and a value of the wrong type:

```text
2026/11/03 02:18:51 yaml: unmarshal errors:
  line 2: cannot unmarshal !!str `wide pl...` into float64
```

Both end the program before the
interface draws, exit status 1, the
timestamped line as the whole output.
The discipline this teaches: edit the
file while lazydocker is closed, keep
the previous version (one `cp` is
enough), and if the program will not
start, suspect the file before the
binary — the error names the line.
The full reference of settable keys is
the project's `docs/Config.md`, read
for this guide but not reproduced
here; the `--config` output is the
short version that cannot drift from
your binary.

## The keys worth learning first

Everything below was either drawn by
the program in the lab (the menus and
the bottom line) or matches its
published keybinding tables, which the
lab cross-checked against those menus
— the Containers table and the lab's
`x` menu agree line for line.

**Moving** — `↑` `↓` within a list;
`←` `→` between panels; `1`–`6` jump
to a panel; `enter` focus the main
panel; `esc` back out of anything;
`PgUp`/`PgDn` scroll the main panel;
`[` and `]` walk its tabs; `/` filters
a list by typing.

**Looking** — `m` view logs; `e`
hide/show stopped containers; `w` open
the container's first port in a
browser.

**The menu** — `x` opens the selected
thing's own menu, which is the honest
way to learn any panel: its keys are
listed there, in context, including
the ones this guide deliberately never
pressed. `b` opens the bulk commands
from anywhere.

**Leaving** — `q`, then `y` at the
confirmation. The confirmation is on
purpose; chapter 12 says why it still
isn't a safety net.

Full tables for every panel live in
the project's `docs/keybindings/`
pages. Learn the moving keys by hand
and let the menus teach you the rest
as you need it — that is how the tool
was designed to be learned, and its
author's other program (lazygit, next
chapter's neighbour) teaches the same
way.
