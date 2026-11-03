# Projects and Services

Outcome: you understand lazydocker's
second half — the compose project view —
what it can do, how it does it (by
running compose for you), and the exact
point where this guide's lab had to
stop: the machinery worked, and the
machine it ran on had no compose
daemon-side to complete a single
action. Everything about *actions* in
this chapter is documented-only, and
says so.

## Two panels you may not have seen

Panels **[1] Project** and **[2]
Services** belong to a **compose
project**: the set of services declared
in a `docker-compose.yml`, run as a
unit. The Docker Compose guide in this
series teaches the file itself; here
the project is a thing to *operate*:
see its services and their state, read
the project's combined log, and run the
project verbs — up, down, stop,
restart, rebuild — from menus instead
of the command line.

Which project? By default, the one
whose compose file lives in the
directory you started lazydocker from;
`-f` names other compose files and
`-p` names the project explicitly
(chapter 3's flag list). The containers
of a project also carry compose labels
— the lab's hello-web wore
`com.docker.compose.project: harbour`
in its Config tab (transcript t09) —
and the Services panel groups by them.

In the lab, panels 1 and 2 never
appeared in the side column: no compose
project was detected through the
fixture endpoint, so the column began
at [3]. The panels were not dead —
pressing `1` switched the main panel
to the Project view — but what it drew
there is the chapter's central piece of
evidence.

## How the compose half works

Where the daemon panels speak the API,
the project half **runs the compose
program as a subprocess** and shows you
the result. The default config file
prints the whole arrangement
(transcript t03) as command templates:

```text
upService:        '{{ .DockerCompose }} up -d {{ .Service.Name }}'
restartService:   '{{ .DockerCompose }} restart {{ .Service.Name }}'
stopService:      '{{ .DockerCompose }} stop {{ .Service.Name }}'
serviceLogs:      '{{ .DockerCompose }} logs --since=60m --follow {{ .Service.Name }}'
rebuildService:   '{{ .DockerCompose }} up -d --build {{ .Service.Name }}'
recreateService:  '{{ .DockerCompose }} up -d --force-recreate {{ .Service.Name }}'
down:             '{{ .DockerCompose }} down'
downWithVolumes:  '{{ .DockerCompose }} down --volumes'
```

with `dockerCompose: docker compose`
deciding what `{{ .DockerCompose }}`
means. Every project action is one of
these lines with the names filled in —
which is good news for trust: there is
no hidden machinery, and chapter 9
shows the templates are yours to edit.

## What the lab actually saw

Pressing `1` in the fixture session
put this in the main panel (transcript
t08):

```text
bash: line 1: docker-compose: command not found
```

The Project view went looking for a
compose program under the name
`docker-compose` — the older standalone
binary — and this machine carries only
the newer `docker compose` plugin form.
So the view failed, plainly, in its own
panel, while every API-driven panel
kept working: the two halves of the
program failing independently, exactly
as chapter 2's model predicts. The fix
on a real machine is to give it the
name it expects (install the standalone
binary, or set the config's
`dockerCompose` template to the form
your machine has — a documented remedy,
not one this lab could verify, since
even a found compose program would
have had no daemon behind it here).

Everything beyond that error — the
Services list rendering, the project
log, every up/down/restart — is
documented-only in this guide: read
from the project's documentation and
its keybinding tables, never run. The
Services menu (from those tables)
mirrors the container menu with service
verbs added: `u` up, `S` start, `s`
stop, `r` restart, `d` remove
containers, plus the same logs, attach
and exec entries as chapter 5. Treat
the warnings there as doubled: a
service verb acts on every container
of the service at once, and `down` on
the Project menu stops the *project*.

## The bulk commands

One more piece of the project half is
visible without a daemon's cooperation:
pressing `b` opens the **Bulk Command**
popup (transcript t09) — "stop all
containers", "remove all containers",
and their kin, plus the config's own
bulk list, which by default offers
compose-wide `up`, `up (attached)`,
`stop` and `pull` (transcript t03). The
lab opened the popup and closed it,
twice, without choosing. Read the list
once so its contents never surprise
you; use it, when you use it, the way
you would use a script you did not
write — after reading every line,
against a daemon you have positively
identified.
