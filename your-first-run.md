# Your First Run

Outcome: the interface open in front of
you, every panel named, and — if your
daemon is missing or stopped — a clear
view of what the program does about it,
which the lab recorded verbatim.

## Starting it

```bash
lazydocker
```

There is nothing else to type. The
program takes over the terminal (your
shell comes back when you quit) and
draws its screen. The first run also
creates its config file,
`~/.config/lazydocker/config.yml` —
empty, meaning "every default"
(transcript t04; chapter 9 is about
writing in it).

## If there is no daemon

This is not a hypothetical in this
guide; it is the lab's own first run
(transcript t04). Lazydocker does not
refuse to start. It draws the complete
interface — all four daemon panels,
correctly titled, all empty — and puts
an error popup in the middle:

```text
Docker event stream returned error: Cannot connect to the Docker
daemon at unix:///var/run/docker.sock. Is the docker daemon running?
Retry count: 2
```

The retry count climbs while it waits:
the program keeps knocking. Start the
daemon and the panels fill on their
own; quit with `q` (it asks first —
the bottom line reads `n/esc: no,
y/enter: yes` — then `y`) and it exits
cleanly, status 0. Two lessons are
worth keeping. The program's *own*
health and the *daemon's* health are
different facts, and this screen reports
both honestly. And an empty fleet on
screen means "no answer", never "no
containers" — the distinction chapter
12 insists on.

## The screen when the daemon answers

Against an answering endpoint — the
lab's fixture stub — the same screen
fills (transcript t07). Down the left,
the lists:

- **Containers**: state, name, live
  CPU%, published ports
  (`8080->80/tcp` on the fixture
  hello-web).
- **Images**: name, tag, size —
  including the `<none>` rows, images
  whose tag moved away from them.
- **Volumes**: driver and name.
- **Networks**: driver and name.

The wide panel on the right is the main
panel: it belongs to whatever row is
selected on the left, and for a
container it opens on the **Logs** tab,
already following. In the lab's capture
the selected container's log lines were
on screen within seconds of starting.

The left column numbers run [3] to [6]
on a plain daemon. Panels [1] Project
and [2] Services belong to the compose
half; they stay folded away until a
compose project is in scope, but their
number keys still work — chapter 8
shows what pressing `1` produced in the
lab.

## Moving around

Four keys do most of the work, and the
bottom line of the screen says so:

```text
PgUp/PgDn: scroll, b: view bulk commands, q: quit, x: menu, ← → ↑ ↓: navigate
```

- `↑` / `↓` move within a list.
- `←` / `→` move between panels.
- A panel's number (`3`, `4`, `5`, `6`)
  jumps straight to it.
- `enter` moves focus into the main
  panel; there, `[` and `]` walk its
  tabs, and `esc` comes back.
- `x` opens the selected thing's menu;
  `esc` closes any menu or popup.
- `q` quits, after the confirmation
  above.

Try the round trip now: arrows down
the container list and watch the main
panel follow the selection — logs for
each container as you land on it. That
one gesture, list on the left and truth
on the right, is the entire tool in
miniature. The next three chapters take
the panels one at a time.
