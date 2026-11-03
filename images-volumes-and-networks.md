# Images, Volumes and Networks

Outcome: the other three lists read as
confidently as Containers — what each
row means, what its detail view adds,
and which of its menu keys are safe to
treat casually (fewer than you might
hope: two of the three panels deal in
things that are easy to delete and
hard to undelete).

## Images

The lab's rows (transcript t07):

```text
example/backup-tool 2.0    58.00MB
example/cache       7      31.00MB
example/hello-web   1.4    142.00MB
example/scratch-db  16     388.00MB
<none>              <none> 12.00MB
```

Name, tag, and the image's size on
disk. An **image** is the packaged
filesystem-and-recipe a container is
started from; the panel answers "what
could I run, and what is it costing
me?" Selecting one shows its detail in
the main panel (transcript t07): name,
full ID, tags, size, creation date —
and the **layer history**, the list of
steps that built it, newest first. The
history is the honest X-ray of an
image: whose base it stands on, what
was copied in, what the entrypoint is.

The `<none>` rows are **dangling**
images: layers no tag points at any
more, usually the leftovers of rebuilds
(the tag moved to a newer build). They
run nothing and cost disk. The Images
menu (press `x` on a row) offers the
expected verbs — remove among them —
and the bulk view offers "prune" style
sweeps. Both are documented-only here,
as in chapter 5, and the warning is
sharper than for containers: removing
an image a stopped container still
references turns a restartable thing
into a rebuild. Chapter 12 counts
image removal among the actions to
take slowly.

## Volumes

```text
local backup-store
local db-data
local web-content
```

Driver and name. A **volume** is
Docker-managed storage that outlives
any container — where the database's
data actually lives while containers
come and go. Selecting one shows its
config (transcript t08): driver, scope,
**mountpoint** (the real path on the
host, here
`/var/lib/docker/volumes/backup-store/_data`),
labels, options, and `RefCount` — how
many containers use it, the single most
important number on the screen. The
fixture's backup-store reads
`RefCount: 0`, which is what "safe to
forget about, dangerous to delete"
looks like: nothing uses it, and it
may still be the only copy of
something.

Volumes are the panel where this guide
is most conservative. The menu's remove
key deletes data — not a reference to
data, the data — and no tab in this
program will show you what is *inside*
a volume before you do. Judge a volume
by its mountpoint and its refcount,
back it up by other means, and let
removal be a decision, not a reflex.

## Networks

```text
bridge bridge
bridge harbour_default
```

Driver and name. A Docker **network**
is the virtual wiring containers plug
into; the bridge rows are the ordinary
kind. The detail view (transcript
t08) shows the full configuration:
subnet and gateway under IPAM, the
IPv6/internal/attachable flags, and
the attached containers. It is the
least-visited panel in daily work and
the first one you want when a container
"cannot see" another: the answer is
almost always that they are not on a
network with a shared name, and this
panel is where that is written down.

Its menu, which the lab drew on the
bridge network, is short: `c` a custom
command, `d` remove network, `b` bulk
commands, and the navigation keys
(transcript t08). Removing a network
with containers attached is refused by
the daemon; removing one quietly used
by a stopped container is the kind of
surprise the Config tab on the
container would have warned about.

## The pattern underneath

Three panels, one grammar: a list of
things, a detail view that is the
daemon's own record of the thing, and a
menu whose destructive entries share
one letter, `d`. Learn the grammar on
the panels where mistakes are cheap
(networks you made, images you pulled)
and carry the caution to the panel
where they are not (volumes).
