# Troubleshooting

Outcome: the failures this tool
actually produces, in the order you
will meet them, each with the check
that separates it from its neighbours.
Most were met in the lab; those that
weren't are marked.

## The screen is empty and there is an error popup

*Lazydocker cannot reach a daemon.* The
popup names the address it tried —
the lab's read `Cannot connect to the
Docker daemon at unix:///var/run/docker.sock`
(transcript t04). Work the list: is the
daemon running (`docker info` fails the
same way — chapter 2's check)? If you
meant another daemon, is `DOCKER_HOST`
set, and set to *that* one? If the
address is a TCP port, is anything
actually listening there? The retry
counter climbing means it is still
trying; a daemon that starts will be
picked up without restarting the tool.

## The fleet on screen is not mine

*You are pointed at the wrong daemon,*
and nothing about the screen will warn
you. This is the most dangerous entry
in the chapter precisely because
nothing is broken. Check `DOCKER_HOST`
in the shell that launched the program
and any config you inherited. Chapter
10's recipe 4 is the full discussion;
the habit to build is naming the target
out loud before acting.

## Lazydocker will not start at all

*Suspect the config file first.* A YAML
error or a wrongly-typed value ends
the program before the interface, with
a timestamped line naming the file line
(transcript t05), exit status 1.
Restore the previous version of
`~/.config/lazydocker/config.yml`, or
rename it away and let the program
create a fresh empty one, then re-apply
your edits one at a time. If the file
is untouched since it last worked,
check the binary itself with
`lazydocker --version`.

## The Project view shows an error but Containers is fine

*The compose half cannot find its
program.* The lab's panel printed
`docker-compose: command not found`
(transcript t08). The API half is
unaffected — different machinery. Fix
by installing the compose program under
the name the view expects, or by
setting the config's `dockerCompose`
template (chapter 9) to the name your
machine has. Documented as the remedy
from the config's own structure; the
lab could demonstrate the failure but,
having no daemon, not the cure.

## A container's log is empty

Three ordinary causes. The container
has been quiet longer than the log
window — `logs.since` defaults to 60m
(transcript t03) and a wider window or
the CLI's `docker logs` settles it. The
container writes to a file instead of
its standard output, in which case the
daemon never sees the lines and
neither can any viewer. Or the
container just started and has not
spoken yet — check the Stats tab: a
live graph with an empty log is a quiet
program, not a broken one.

## The CPU column never moves

The stats stream feeds the column;
for a *stopped* container there is no
stream and the number is a leftover
(chapter 5). For a running one, a
perfectly flat graph over minutes is
itself the finding — something is
looping or waiting with unusual
discipline, and chapter 10's third
recipe is the reading technique.

## Quitting asks a question every time

That is the design: `q` opens a
confirmation (`n/esc: no, y/enter:
yes`). In the lab's first driver script
a lone `q` looked like a hang — the
program was waiting politely at its
own prompt. Answer `y`, or `esc` to
stay. This guide counts the behaviour
as a feature and lists it so your
scripts do not trip on it.

## The trap the lab fell into

Writing this guide's fixture endpoint,
the lab's first stub answered the logs
request and then held the follow stream
open *without sending the buffered
lines first* — lazydocker quite
correctly showed an empty Logs tab, and
for a while the program looked broken
when the fixture was. The general form
is worth keeping: **when a viewer shows
nothing, test the source before
blaming the glass.** One
`curl http://<endpoint>/_ping` and a
look at what the endpoint claims would
have saved the lab ten minutes; the
same courtesy applies to real daemons
and real networks.
