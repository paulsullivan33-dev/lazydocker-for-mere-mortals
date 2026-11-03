#!/usr/bin/env python3
"""Drive a TUI program in a pty and snapshot the rendered screen.

Usage: ptydrive.py <session-name> <steps-file> -- <command...>

The steps file has one step per line:
  wait <seconds>          sleep, reading output
  key <name>              send a key: enter tab esc up down left right
                          space backspace, or a literal string like "q"
  snap <label>            save the current screen rendering
Env for the child comes from the caller's environment.
Snapshots land in ./shots/<session>-<label>.txt ; the raw stream in
./shots/<session>.raw .
"""
import os
import pty
import select
import signal
import sys
import time

import pyte

COLS, ROWS = 140, 44


def main():
    session = sys.argv[1]
    steps_file = sys.argv[2]
    assert sys.argv[3] == "--"
    cmd = sys.argv[4:]

    os.makedirs("shots", exist_ok=True)
    raw_path = f"shots/{session}.raw"
    raw = open(raw_path, "wb")

    screen = pyte.Screen(COLS, ROWS)
    stream = pyte.ByteStream(screen)

    import fcntl
    import struct
    import termios

    pid, fd = pty.fork()
    if pid == 0:
        # set the window size before exec so the app reads it at startup
        fcntl.ioctl(1, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))
        os.environ["TERM"] = "xterm-256color"
        os.execvp(cmd[0], cmd)

    keys = {
        "enter": b"\r",
        "tab": b"\t",
        "esc": b"\x1b",
        "up": b"\x1b[A",
        "down": b"\x1b[B",
        "right": b"\x1b[C",
        "left": b"\x1b[D",
        "space": b" ",
        "backspace": b"\x7f",
        "ctrl-c": b"\x03",
    }

    def drain(timeout):
        end = time.time() + timeout
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], max(0, end - time.time()))
            if not r:
                break
            try:
                data = os.read(fd, 65536)
            except OSError:
                return False
            if not data:
                return False
            raw.write(data)
            raw.flush()
            stream.feed(data)
        return True

    def snap(label):
        drain(0.4)
        lines = [line.rstrip() for line in screen.display]
        while lines and not lines[-1]:
            lines.pop()
        with open(f"shots/{session}-{label}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"snapshot {label}: {len(lines)} rows")

    alive = True
    for line in open(steps_file):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        op, _, arg = line.partition(" ")
        if op == "wait":
            alive = drain(float(arg))
        elif op == "key":
            data = keys.get(arg, arg.encode().decode("unicode_escape").encode("latin1"))
            os.write(fd, data)
            alive = drain(0.3)
        elif op == "snap":
            snap(arg)
        if not alive:
            print("child exited early")
            break

    # make sure the child is gone
    try:
        os.kill(pid, signal.SIGHUP)
    except ProcessLookupError:
        pass
    try:
        _, status = os.waitpid(pid, 0)
        print(f"child exit status: {status}")
    except ChildProcessError:
        pass
    raw.close()


if __name__ == "__main__":
    main()
