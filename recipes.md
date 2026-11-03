# Recipes

Outcome: four jobs done the lazydocker
way, end to end. Every step below is
read-only — selections, tabs and menus
opened, nothing state-changing — and
each recipe says what it proves and
what it cannot.

## 1. The morning health check

*For: one machine, a handful of
containers, two minutes.*

Start `lazydocker`. In the Containers
panel: press `e` until stopped
containers are **shown** (the true
view). Read top to bottom asking three
questions. Is everything that should
be `running`, running? Does any
`exited` row carry a non-zero code?
Does any CPU% look wrong for this hour
— pinned high, or flat on a container
that should be busy? Land on each
suspect and read its Logs tab; for the
busy one, its Stats tab. Quit with
`q`, `y`.

*Proves:* the fleet's state *now*, with
the failure's own words one key away.
*Cannot prove:* anything about last
night — the tool has no memory
(chapter 12), so a container that
failed at 3 a.m. and was restarted by
its policy looks innocent here. Its
log, if the daemon kept it, is the
only witness.

## 2. Auditing a fleet you inherited

*For: a machine someone else set up,
before you touch anything.*

Containers first: names, images,
ports. Every published port is a door;
note each one and ask whether it
should exist. Select each running
container and walk its tabs:
**Config** for the image and labels
(who built this, from what), **Env**
for what it was told — reading with
chapter 6's warning in mind — and
**Top** for what is actually inside.
Then Images for the shelf it came from
and Volumes for where its data lives,
noting every `RefCount: 0` volume as
"unknown, do not delete".

Write down what you found outside the
tool; lazydocker will not remember it
for you. *Proves:* the fleet as the
daemon knows it, in one sitting.
*Cannot prove:* intent — which of these
containers anyone still wants. That
question belongs to people.

## 3. Watching a suspicious container

*For: the job that "sometimes hangs".*

Select the container; `enter` to focus
the main panel; `]` to the **Stats**
tab and leave it there. A working
container's graphs breathe — CPU moves
with requests, memory steps and holds.
The hang has signatures: CPU nailed to
one value with no movement is a loop;
CPU at zero while requests should be
arriving is a wait — on a lock, a dead
dependency, a full disk somewhere
below. Walk back with `[` to **Logs**
and read the last lines before the
silence; in the lab's fixture the log
is five cheerful lines, but the shape
of the reading — *the log stops where
the graph flattens* — is the whole
technique.

*Proves:* whether it is working or
waiting, and when it stopped.
*Cannot prove:* why, beyond what its
own log says. That is the container's
story to tell, and some do not tell it.

## 4. Pointing lazydocker at another machine

*For: the daemon on the small server in
the cupboard, watched from your desk.*

Lazydocker obeys the standard
`DOCKER_HOST`. The lab pointed it at a
fixture endpoint over TCP:

```bash
DOCKER_HOST=tcp://127.0.0.1:18086 lazydocker
```

and the whole fleet on that endpoint
filled the screen (transcript t07). On
your own network the address is the
server's. Two honest warnings ride
with this recipe. The Docker API over
plain TCP is **unencrypted and
unauthenticated** — anyone who can
reach the port owns the daemon, so the
port must never face a network you do
not trust; the safer shapes are an SSH
tunnel or `DOCKER_HOST=ssh://…`, which
the Docker CLI supports and
lazydocker inherits. And the rule from
chapter 1 applies with force: a screen
that looks exactly like your local
fleet may be another machine's. Check
the endpoint before you press anything
but arrows. The read-only recipes
above are safe to run against it; the
changing keys are chapter 5's, and
they act *there*, not here.
