# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's fleet is invented: four containers, five images,
   three volumes, two networks, stock log lines.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 12 names what the tool
   cannot do: it shows only the daemon it can reach and cannot
   tell an empty fleet from a dead one without its error popup;
   it has no memory, no history and no alerts; its read-only
   keyboard and its destructive keyboard are the same keyboard,
   aimed at whichever daemon `DOCKER_HOST` names; it prints
   container environment variables, secrets included, in plain
   sight; its compose half depends on finding a compose program
   under the name it expects; and a stats number can outlive
   the stream that fed it.
8. **The ethics rule is in the text, early.** Lazydocker is a
   viewer with leverage over other people's machines the moment
   it is pointed at them, so chapter 1 states the rule before
   any procedure depends on it — know which daemon you are
   pointed at before pressing anything but an arrow key — and
   chapter 12 returns to the two handling duties it creates:
   the Env tab's plain-sight secrets are keys, not data, and a
   production daemon is not a playground for unfamiliar keys.
   The lab itself worked only against a fixture endpoint of its
   own invention, on loopback, and sent it no write requests.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox,
shared with other work while the lab ran. Lazydocker **0.25.2**
was installed from the official release archive
`lazydocker_0.25.2_Linux_x86_64.tar.gz` (SHA-256 checked against
the release's `checksums.txt`: `0d9dbfc2…b9523c`, OK) and run
unmodified. All transcripts live in
`lazydocker-lab/transcripts/`; the terminal driver that
captured the TUI screens is `lazydocker-lab/tui-driver.py`
(a pty driver with a pyte renderer, 140×44 screen), and the
screens it saved are quoted trimmed to 132 columns.

**The sandbox has no Docker daemon, and the guide is built
around that fact rather than around pretending otherwise.**
The Docker client is installed (29.1.3) but there is no
socket; `docker info`'s server section refuses (t00), and one
bounded attempt to start `dockerd` (12 s, its own data root)
failed at network setup: `failed to start daemon: …
iptables … Permission denied (you must be root)` (t00). No
daemon was ever available to any part of this lab.

To exercise the interface anyway, the lab wrote a **fake
Docker endpoint** (`lazydocker-lab/docker-stub.py`, Python
standard library only): a stub that answers the subset of the
Docker Engine API lazydocker asks for — ping, version, info,
container/image/volume/network lists and inspects, image
history, container stats streams, container logs in the
daemon's framed format, process top, and an events stream held
open — with an invented fleet (containers hello-web,
scratch-db, cache-box, nightly-backup; five images; volumes
web-content, db-data, backup-store; networks bridge and
harbour_default; fixture timestamps October–November 2025).
Write requests (POST/DELETE/PUT) are logged and answered 204;
across all sessions **none were ever sent** (t10). The stub
listened on loopback port 18086 only, and was stopped when the
lab ended. The Docker CLI itself accepted the stub as a
daemon (`docker ps -a` rendered the fleet, t06), which is the
lab's evidence the fixture spoke the API faithfully.

Run for real, with transcripts as evidence:

- The daemon's absence itself: `which`, `docker info`,
  `docker ps`, and the bounded `dockerd` attempt and its
  verbatim kernel refusal (t00).
- Download, checksum verification, `--version` in full (t01);
  the complete `--help` (t02); `lazydocker --config` printing
  the whole built-in default configuration, including the
  compose command templates and bulk commands (t03).
- The first run with no daemon: full interface drawn, all
  panels empty, the error popup verbatim ("Cannot connect to
  the Docker daemon at unix:///var/run/docker.sock… Retry
  count: 2"), the two-key quit (q asks, y confirms, exit 0),
  and the empty `config.yml` the first run creates (t04).
- Config behaviour: a YAML syntax error and a wrongly-typed
  value each aborting startup with the verbatim messages and
  exit 1; a valid `gui.sidePanelWidth: 0.5` measurably
  widening the side column (t05).
- Against the stub: the Containers panel with states, CPU%
  and published ports; the selected container's Logs tab
  following; the Images list and an image's detail view with
  layer history; the Volumes and Networks lists and their
  config views; the Project view's verbatim
  `docker-compose: command not found` (t07, t08).
- The container `x` menu drawn in full; all five main-panel
  tabs rendered for a fixture container — Logs, Stats (CPU
  25.00% and memory 0.51% graphs, both arithmetically checked
  against the fixture stream), Env, Config (compose labels
  included), Top; the Bulk Command popup opened and closed
  (t09). Menus and popups were only ever opened and closed
  with `esc`; no menu action was chosen.
- The API conversation itself, from the stub's request log:
  lists once, per-container inspect polling (19× per
  container), stats and log-follow streams per selection,
  events, version, pings — and zero write requests (t10).
- The published keybinding tables
  (`docs/keybindings/Keybindings_en.md` at the v0.25.2 tag)
  cross-checked against the menu the program drew: the
  Containers entries agree line for line.

Documented only — described from the project's documentation,
its menus, or its published tables, not run, and the text does
not claim otherwise:

- **Every state-changing operation**: stop, restart, pause,
  remove, attach, exec shell, open-in-browser, image removal
  and pruning, volume and network removal, and every bulk
  command's execution. The stub could not have performed
  them; the lab opened the menus, read the keys, and closed
  them again. Confirmation behaviour is described from the
  menus and documentation.
- The Services panel in operation and the Project view
  succeeding: no compose project was detected through the
  stub, so panels 1–2 never rendered their lists; the
  `dockerCompose` template remedy for the Project view's
  `docker-compose` error is stated as the config's evident
  fix, not a verified one.
- Any behaviour against a real daemon: real stats staleness,
  real event timing, attach/exec terminal behaviour, health
  status rendering (the fixture carries no healthchecks), and
  compose projects whose containers the stub cannot imitate.
- The neighbour tools of chapter 11, except the Docker CLI
  (which was run, against both the missing daemon and the
  stub): Portainer, Dockge, ctop, dive and lazygit are
  characterised, not installed.
- Package-manager installs (Homebrew, Arch, Nix, Scoop):
  named as routes; only the release archive was exercised.

One fixture note, for the record: the stub's first version
held log-follow connections open before sending the buffered
lines, so the Logs tab rendered empty until the stub was
fixed to send first and hold after (chapter 13 tells this as
the troubleshooting lesson it was). The transcripts in the
repository are from the corrected stub.
