#!/usr/bin/env python3
"""A tiny fake Docker Engine API endpoint, for the lazydocker lab.

lazydocker talks to Docker over its HTTP API. This sandbox has no
Docker daemon and cannot run one, so this stub answers the subset of
the API lazydocker asks for, with invented fixture data. It is NOT a
container runtime: nothing here can start, stop or create anything.
POST/DELETE calls are logged and answered 204 so the requests
lazydocker makes stay visible in the log.

Every request line (method + path) is appended to the file named by
STUB_LOG (default ./stub-requests.log in the working directory).

Usage: python3 docker-stub.py [port]     (default 18086, loopback only)
"""
import json
import os
import struct
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

LOG = os.environ.get("STUB_LOG", "stub-requests.log")
NOW = 1762214400  # a fixed "now" for fixture timestamps (2025-11-03)

C1 = "a1b2c3d4e5f6" * 5 + "a1b2"  # 64 hex chars
C2 = "b2c3d4e5f6a1" * 5 + "b2c3"
C3 = "c3d4e5f6a1b2" * 5 + "c3d4"
C4 = "d4e5f6a1b2c3" * 5 + "d4e5"
IMG1 = "sha256:" + "1a" * 32
IMG2 = "sha256:" + "2b" * 32
IMG3 = "sha256:" + "3c" * 32
IMG4 = "sha256:" + "4d" * 32
IMG5 = "sha256:" + "5e" * 32

HARBOUR = {"com.docker.compose.project": "harbour",
           "com.docker.compose.config-hash": "f00df00d"}


def container(cid, name, image, img, state, status, created, ports=None,
              labels=None, cmd="/start.sh"):
    return {
        "Id": cid,
        "Names": ["/" + name],
        "Image": image,
        "ImageID": img,
        "Command": cmd,
        "Created": created,
        "Ports": ports or [],
        "Labels": labels or {},
        "State": state,
        "Status": status,
        "NetworkSettings": {"Networks": {"bridge": {
            "NetworkID": "netbridge", "EndpointID": "ep" + cid[:6],
            "Gateway": "172.17.0.1", "IPAddress": "172.17.0.2",
            "MacAddress": "02:42:ac:11:00:02", "Aliases": None}}},
        "Mounts": [],
    }


CONTAINERS = [
    container(C1, "hello-web", "example/hello-web:1.4", IMG1, "running",
              "Up 3 hours", NOW - 10800,
              ports=[{"IP": "0.0.0.0", "PrivatePort": 80, "PublicPort": 8080,
                      "Type": "tcp"}],
              labels={**HARBOUR, "com.docker.compose.service": "hello-web"}),
    container(C2, "scratch-db", "example/scratch-db:16", IMG2, "running",
              "Up 3 hours", NOW - 10700,
              labels={**HARBOUR, "com.docker.compose.service": "scratch-db"},
              cmd="postgres"),
    container(C3, "cache-box", "example/cache:7", IMG3, "running",
              "Up 5 days", NOW - 432000, cmd="cache-server --port 6379"),
    container(C4, "nightly-backup", "example/backup-tool:2.0", IMG4, "exited",
              "Exited (0) 2 hours ago", NOW - 90000, cmd="/backup.sh nightly"),
]

IMAGES = [
    {"Id": IMG1, "RepoTags": ["example/hello-web:1.4"], "RepoDigests": [],
     "Created": NOW - 86400 * 9, "Size": 142_000_000,
     "VirtualSize": 142_000_000, "Labels": {}, "ParentId": "", "Containers": 1},
    {"Id": IMG2, "RepoTags": ["example/scratch-db:16"], "RepoDigests": [],
     "Created": NOW - 86400 * 21, "Size": 388_000_000,
     "VirtualSize": 388_000_000, "Labels": {}, "ParentId": "", "Containers": 1},
    {"Id": IMG3, "RepoTags": ["example/cache:7"], "RepoDigests": [],
     "Created": NOW - 86400 * 30, "Size": 31_000_000,
     "VirtualSize": 31_000_000, "Labels": {}, "ParentId": "", "Containers": 1},
    {"Id": IMG4, "RepoTags": ["example/backup-tool:2.0"], "RepoDigests": [],
     "Created": NOW - 86400 * 12, "Size": 58_000_000,
     "VirtualSize": 58_000_000, "Labels": {}, "ParentId": "", "Containers": 1},
    {"Id": IMG5, "RepoTags": ["<none>:<none>"], "RepoDigests": [],
     "Created": NOW - 86400 * 40, "Size": 12_000_000,
     "VirtualSize": 12_000_000, "Labels": {}, "ParentId": "", "Containers": 0},
]

VOLUMES = [
    {"Name": "web-content", "Driver": "local",
     "Mountpoint": "/var/lib/docker/volumes/web-content/_data",
     "CreatedAt": "2025-10-20T09:14:00Z", "Labels": {}, "Scope": "local",
     "Options": {}, "UsageData": {"RefCount": 1, "Size": 4_800_000}},
    {"Name": "db-data", "Driver": "local",
     "Mountpoint": "/var/lib/docker/volumes/db-data/_data",
     "CreatedAt": "2025-09-28T17:40:00Z", "Labels": {}, "Scope": "local",
     "Options": {}, "UsageData": {"RefCount": 1, "Size": 912_000_000}},
    {"Name": "backup-store", "Driver": "local",
     "Mountpoint": "/var/lib/docker/volumes/backup-store/_data",
     "CreatedAt": "2025-08-15T08:02:00Z", "Labels": {}, "Scope": "local",
     "Options": {}, "UsageData": {"RefCount": 0, "Size": 2_300_000_000}},
]

NETWORKS = [
    {"Id": "netbridge", "Name": "bridge", "Driver": "bridge", "Scope": "local",
     "Created": "2025-08-01T00:00:00Z", "EnableIPv6": False, "Internal": False,
     "Attachable": False, "Ingress": False,
     "IPAM": {"Driver": "default", "Config": [{"Subnet": "172.17.0.0/16",
     "Gateway": "172.17.0.1"}]}, "Containers": {}, "Options": {}, "Labels": {}},
    {"Id": "netharbour", "Name": "harbour_default", "Driver": "bridge",
     "Scope": "local", "Created": "2025-10-20T09:13:00Z", "EnableIPv6": False,
     "Internal": False, "Attachable": False, "Ingress": False,
     "IPAM": {"Driver": "default", "Config": [{"Subnet": "172.18.0.0/16",
     "Gateway": "172.18.0.1"}]}, "Containers": {}, "Options": {},
     "Labels": {"com.docker.compose.project": "harbour"}},
]

def log_lines(name):
    return [
        f"2025-11-03T09:00:01Z {name}: fixture process started",
        f"2025-11-03T09:00:02Z {name}: ready to serve",
        f"2025-11-03T09:12:44Z {name}: handled request 200",
        f"2025-11-03T09:31:07Z {name}: handled request 200",
        f"2025-11-03T10:02:19Z {name}: checkpoint written",
    ]


def stats(cid):
    base = {
        "read": "2025-11-03T10:15:00.000000000Z",
        "preread": "2025-11-03T10:14:59.000000000Z",
        "num_procs": 0,
        "pids_stats": {"current": 12, "limit": 0},
        "blkio_stats": {"io_service_bytes_recursive": [
            {"major": 8, "minor": 0, "op": "Read", "value": 40960},
            {"major": 8, "minor": 0, "op": "Write", "value": 8192}]},
        "cpu_stats": {
            "cpu_usage": {"total_usage": 4_500_000_000,
                          "percpu_usage": [2_300_000_000, 2_200_000_000],
                          "usage_in_kernelmode": 300_000_000,
                          "usage_in_usermode": 4_200_000_000},
            "system_cpu_usage": 96_000_000_000,
            "online_cpus": 2,
            "throttling_data": {"periods": 0, "throttled_periods": 0,
                                "throttled_time": 0}},
        "precpu_stats": {
            "cpu_usage": {"total_usage": 4_000_000_000,
                          "percpu_usage": [2_050_000_000, 1_950_000_000],
                          "usage_in_kernelmode": 280_000_000,
                          "usage_in_usermode": 3_720_000_000},
            "system_cpu_usage": 94_000_000_000,
            "online_cpus": 2,
            "throttling_data": {"periods": 0, "throttled_periods": 0,
                                "throttled_time": 0}},
        "memory_stats": {"usage": 42_000_000, "limit": 8_300_000_000,
                         "max_usage": 48_000_000, "failcnt": 0,
                         "stats": {"cache": 6_000_000, "rss": 36_000_000}},
        "name": "/fixture",
        "id": cid,
        "networks": {"eth0": {"rx_bytes": 154_000, "rx_packets": 900,
                              "tx_bytes": 402_000, "tx_packets": 850}},
        "storage_stats": {},
    }
    return base


def inspect_container(c):
    return {
        "Id": c["Id"], "Created": "2025-11-03T07:00:00.000000000Z",
        "Path": "/start.sh", "Args": [], "Name": c["Names"][0],
        "Image": c["ImageID"],
        "State": {"Status": c["State"],
                  "Running": c["State"] == "running", "Paused": False,
                  "Restarting": False, "OOMKilled": False, "Dead": False,
                  "Pid": 1234 if c["State"] == "running" else 0,
                  "ExitCode": 0, "Error": "",
                  "StartedAt": "2025-11-03T07:00:01.000000000Z",
                  "FinishedAt": "0001-01-01T00:00:00Z"},
        "ResolvConfPath": "", "HostnamePath": "", "HostsPath": "",
        "LogPath": "", "RestartCount": 0, "Driver": "overlay2",
        "Platform": "linux",
        "HostConfig": {"NetworkMode": "default", "RestartPolicy":
                       {"Name": "no", "MaximumRetryCount": 0}, "Binds": []},
        "GraphDriver": {"Name": "overlay2", "Data": {}},
        "Mounts": [],
        "Config": {"Hostname": c["Names"][0].strip("/"), "User": "",
                   "Env": ["PATH=/usr/local/bin:/usr/bin:/bin"],
                   "Cmd": ["/start.sh"], "Image": c["Image"],
                   "Labels": c["Labels"], "Tty": False,
                   "ExposedPorts": {"80/tcp": {}} if c["Id"] == C1 else {}},
        "NetworkSettings": c["NetworkSettings"],
    }


def framed_logs(name):
    out = b""
    for line in log_lines(name):
        payload = (line + "\n").encode()
        out += struct.pack(">BxxxI", 1, len(payload)) + payload
    return out


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # silence default logging
        pass

    def note(self):
        with open(LOG, "a") as f:
            f.write(f"{self.command} {self.path}\n")

    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Api-Version", "1.47")
        self.send_header("Docker-Experimental", "false")
        self.send_header("Ostype", "linux")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def handle_all(self):
        self.note()
        parsed = urlparse(self.path)
        path = parsed.path
        # strip /vX.Y prefix
        parts = path.split("/")
        if len(parts) > 1 and parts[1].startswith("v") and "." in parts[1]:
            path = "/" + "/".join(parts[2:])
        q = parse_qs(parsed.query)

        if path == "/_ping":
            body = b"OK"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Api-Version", "1.47")
            self.send_header("Docker-Experimental", "false")
            self.send_header("Ostype", "linux")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return

        if path == "/version":
            return self.send_json({
                "Version": "27.3.1", "ApiVersion": "1.47",
                "MinAPIVersion": "1.24", "GitCommit": "stub",
                "GoVersion": "go1.22", "Os": "linux", "Arch": "amd64",
                "KernelVersion": "6.8.0", "BuildTime": "2025-01-01T00:00:00Z",
                "PkgVersion": "stub", "Components": [], "Platform":
                {"Name": "Docker Engine - Community (stub)"}})

        if path == "/info":
            return self.send_json({
                "ID": "STUB", "Containers": 4, "ContainersRunning": 3,
                "ContainersPaused": 0, "ContainersStopped": 1, "Images": 5,
                "Driver": "overlay2", "Plugins": {}, "MemTotal": 8_300_000_000,
                "NCPU": 2, "Name": "stub-docker", "ServerVersion": "27.3.1",
                "OSType": "linux", "Architecture": "x86_64",
                "DockerRootDir": "/var/lib/docker",
                "SystemTime": "2025-11-03T10:15:00Z", "IndexConfig": {},
                "SecurityOptions": [], "Warnings": None})

        if path == "/system/df":
            return self.send_json({
                "LayersSize": 631_000_000, "Images": IMAGES,
                "Containers": [], "Volumes": VOLUMES, "BuildCache": [],
                "BuilderSize": 0})

        if path == "/containers/json":
            show_all = q.get("all", ["0"])[0] in ("1", "true")
            out = [c for c in CONTAINERS if show_all or c["State"] == "running"]
            return self.send_json(out)

        if path == "/images/json":
            return self.send_json(IMAGES)

        if path == "/volumes":
            return self.send_json({"Volumes": VOLUMES, "Warnings": None})

        if path == "/networks":
            return self.send_json(NETWORKS)

        if path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            try:
                while True:
                    time.sleep(30)  # hold the stream open, send nothing
            except (BrokenPipeError, ConnectionResetError):
                pass
            return

        if path.startswith("/containers/"):
            rest = path[len("/containers/"):]
            cid, _, action = rest.partition("/")
            match = next((c for c in CONTAINERS
                          if c["Id"].startswith(cid) or cid.startswith(c["Id"][:12])), None)
            if action == "json" and match:
                return self.send_json(inspect_container(match))
            if action == "stats":
                stream = q.get("stream", ["true"])[0] != "false"
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                try:
                    n = 30 if stream else 1
                    for _ in range(n):
                        self.wfile.write(json.dumps(stats(cid)).encode() + b"\n")
                        self.wfile.flush()
                        if not stream:
                            break
                        time.sleep(1)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return
            if action == "logs":
                name = match["Names"][0].strip("/") if match else "fixture"
                body = framed_logs(name)
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.docker.raw-stream")
                self.end_headers()
                self.wfile.write(body)
                self.wfile.flush()
                if q.get("follow", ["false"])[0] in ("1", "true"):
                    try:
                        while True:
                            time.sleep(30)  # hold the follow stream open
                    except (BrokenPipeError, ConnectionResetError):
                        pass
                else:
                    self.close_connection = True
                return
            if action == "top":
                return self.send_json({"Titles": ["UID", "PID", "TIME", "CMD"],
                                       "Processes": [["root", "1234", "2h",
                                                      "/start.sh"]]})
            if action == "changes":
                return self.send_json([])
            if action in ("start", "stop", "restart", "kill", "pause",
                          "unpause", "rename", "exec", "") or self.command in ("POST", "DELETE", "PUT"):
                self.send_response(204)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return

        if path.startswith("/images/") and path.endswith("/history"):
            return self.send_json([
                {"Id": IMG1, "Created": NOW - 86400 * 9,
                 "CreatedBy": "/bin/sh -c #(nop) ENTRYPOINT [\"/start.sh\"]",
                 "Tags": ["example/hello-web:1.4"], "Size": 0, "Comment": ""},
                {"Id": "<missing>", "Created": NOW - 86400 * 10,
                 "CreatedBy": "/bin/sh -c COPY app /srv/app",
                 "Tags": None, "Size": 96_000_000, "Comment": ""},
                {"Id": "<missing>", "Created": NOW - 86400 * 11,
                 "CreatedBy": "/bin/sh -c #(nop) FROM example/base:1",
                 "Tags": None, "Size": 46_000_000, "Comment": ""}])

        if path.startswith("/images/") and path.endswith("/json"):
            return self.send_json({"Id": IMG1, "RepoTags": ["example/hello-web:1.4"],
                                   "Created": "2025-10-25T00:00:00Z",
                                   "Config": {}, "Architecture": "amd64",
                                   "Os": "linux", "Size": 142_000_000,
                                   "GraphDriver": {"Name": "overlay2", "Data": {}},
                                   "RootFS": {"Type": "layers", "Layers": []},
                                   "Metadata": {}, "Descriptor": {}})

        if path.startswith("/volumes/"):
            name = path[len("/volumes/"):]
            v = next((v for v in VOLUMES if v["Name"] == name), None)
            if v:
                return self.send_json(v)

        if path.startswith("/networks/"):
            n = next((n for n in NETWORKS if n["Id"] == path[len("/networks/"):]), None)
            if n:
                return self.send_json(n)

        if self.command in ("POST", "DELETE", "PUT"):
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        return self.send_json({"message": f"stub: no such resource: {path}"}, code=404)

    do_GET = handle_all
    do_HEAD = handle_all
    do_POST = handle_all
    do_DELETE = handle_all
    do_PUT = handle_all


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18086
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"docker stub listening on 127.0.0.1:{port}", flush=True)
    server.serve_forever()
