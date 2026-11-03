# Glossary

**Attach** — connecting your terminal
to a running container's own console:
its output becomes your screen, your
keystrokes become its input. Leaving
can be fiddly (the container may read
your detach keys as input), which is
why chapter 5 treats it with respect.

**Bulk commands** — lazydocker's named,
fleet-wide actions (`stop all
containers`, compose `up`, `pull`…),
behind the `b` popup and the config's
`bulkCommands` section.

**Command template** — a line in the
config file with placeholders
(`{{ .DockerCompose }} up -d
{{ .Service.Name }}`) that lazydocker
fills in and runs as a subprocess for
project and service actions.

**Compose project** — the unit Docker
Compose operates: the services declared
in one `docker-compose.yml`, their
containers, networks and volumes, run
and stopped together.

**Container** — a running (or stopped)
instance of an image: the image's
filesystem plus a process, a network
identity and a log, all managed by the
daemon.

**Dangling image** — an image no tag
points at any more, usually the
previous build of something you
rebuilt. Runs nothing, costs disk,
shows as `<none>` in the Images panel.

**Daemon** — the Docker daemon,
`dockerd`: the background program that
creates, runs and destroys containers
and answers the API. The only part of
the system that touches the kernel.

**DOCKER_HOST** — the environment
variable that tells Docker clients,
lazydocker included, which daemon to
talk to: a socket path, a TCP address,
or an SSH address. The steering wheel
of chapter 10's fourth recipe, and of
its warning.

**Docker Engine API** — the HTTP
interface the daemon answers: lists,
inspect, stats, logs, events, and the
write operations. The conversation
chapter 2 transcribes from the lab's
request log.

**Events stream** — the daemon's
announce channel: a held-open API
request over which creations, starts,
stops and deaths are reported as they
happen, so clients do not have to keep
asking.

**Exec** — starting a *new* process
(usually a shell) inside a running
container, as opposed to attach, which
joins the process already there. The
most powerful item on the container
menu.

**Image** — the packaged filesystem and
metadata a container is started from:
built in layers, named with tags,
shared from registries.

**Inspect** — the daemon's full record
of one thing — every field it holds —
returned by `/containers/<id>/json` and
its siblings, and rendered by the
Config tab.

**Layer** — one build step's worth of
an image: images are stacks of layers,
and the Images detail view lists them
as the image's history.

**Main panel** — lazydocker's large
right-hand panel: the selected thing in
detail, with tabs for a container
(Logs, Stats, Env, Config, Top).

**Network** — Docker's virtual wiring:
a named subnet and switch containers
plug into to reach each other and,
through published ports, the outside.

**Panel** — one of lazydocker's six
numbered lists down the left of the
screen: Project, Services, Containers,
Images, Volumes, Networks.

**Published port** — a mapping from a
port on the host to a port in a
container (`8080->80/tcp`): the door
through which the outside reaches in.

**RefCount** — on a volume's detail
view, how many containers use it. Zero
means unused, not unimportant.

**Service** — one declared entry in a
compose file: a role ("the web
server", "the database") that compose
runs as one or more containers.

**Stats stream** — the daemon's live
feed of a container's resource use
(CPU, memory, network, disk), from
which lazydocker draws the CPU column
and the Stats tab's graphs.

**Stub** — this guide's word for its
fixture endpoint: a small program that
answers the Docker API with invented
data, used because the lab had no
daemon. Nothing it "runs" exists.

**Volume** — Docker-managed storage
that outlives containers: where data
that must survive a container's
replacement actually lives.
