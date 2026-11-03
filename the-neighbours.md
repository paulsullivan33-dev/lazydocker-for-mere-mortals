# The Neighbours

Outcome: you can place lazydocker among
its neighbours without folklore — what
each does that it doesn't, and the one
thing it does that none of them quite
do. Except for the Docker CLI (run in
the lab), these tools are characterised
from their documentation, not run, and
the text does not claim otherwise.

## The Docker CLI — the ground it stands on

`docker ps`, `docker logs -f`,
`docker stats`, `docker inspect`: the
daemon's own command line, and the only
neighbour this guide ran. It does
everything lazydocker does and a great
deal more — creating, building,
networking, volumes, the whole API in
flag form — one question per command,
in output that freezes as it prints.
Lazydocker's entire proposition is the
inverse trade: fewer verbs, living
output, the questions pre-asked. Most
people keep both: the screen for
watching, the CLI for surgery and for
scripts. A script cannot press `x`,
and a screen cannot be piped; the
tools are complements wearing similar
names.

## docker compose — the project as a file

Compose is not a viewer at all: it is
the declarative half — a YAML file that
says what a project *should* be, and a
command that makes it so. Lazydocker's
project panels literally run it
(chapter 8). If your work is authoring
stacks, compose is the primary tool
and lazydocker the window onto the
result; if your work is operating a
stack someone else authored, the
balance tips.

## Portainer — the web console

Portainer puts the same fleet in a
browser: dashboards, point-and-click
management, and — the decisive
difference — **user accounts and access
control**, so a team can share a daemon
with permissions and an audit trail.
It is a server you install (as a
container, naturally) rather than a
program you run. Choose it when more
than one person needs in, or when the
watching must happen from machines you
cannot install a terminal tool on.
Choose lazydocker when it is one
person, one terminal, and speed
matters. The Portainer guide in this
series gives it a full lab.

## Dockge — compose stacks in a browser

Dockge (by the author of Uptime Kuma)
narrows the web idea to compose:
your stacks as folders of YAML, edited
and operated from a browser page, with
a live terminal and logs. Where
lazydocker's project half is a guest
in a daemon-shaped house, Dockge is
compose all the way down — and, being
a web service, it is reachable from
anywhere you let it be, with the
security questions that raises. If
your world is stacks and you want them
in a browser, it is the closer cousin;
if your world is the daemon as a
whole, it deliberately sees less.

## ctop — the narrow specialist

ctop is a top-style screen for
containers only: one dense table of
live metrics, sortable, with a
single-container view — and nothing
else. No images, no volumes, no
compose, minimal acting. It starts
faster, fits in less screen, and tells
you less. On a tiny terminal or a
machine where lazydocker is not
installed, it is the honest pocket
version of the same idea.

## dive — the image pathologist

dive explores one image layer by
layer: what each build step added,
which bytes are wasted, where the fat
is. Lazydocker's image panel shows a
history list; dive shows the *contents*
and scores the waste. They meet at the
Images panel and go opposite ways —
lazydocker back to the fleet, dive
down into the artefact.

## lazygit — the sibling

Lazydocker is Jesse Duffield's second
program, built after lazygit taught a
generation that a terminal interface
could make git feel small. The family
resemblance is total: panels on the
left, detail on the right, `x` for the
menu, `q` with a confirmation, one YAML
config, and the philosophy that the
program should teach its own keys in
context. If you know one, the other's
hands are already trained — and the
lazygit guide in this series is the
natural companion read. What the
siblings share most is a stance: the
underlying tool stays the authority
(git there, the daemon here), and the
interface's job is to make the
authority legible, never to replace
it.
