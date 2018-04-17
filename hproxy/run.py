#!/usr/bin/env python
"""
 Created by howie.hu at 17-10-18.
"""
import subprocess

if __name__ == '__main__':
    servers = [
        ["pipenv", "run", "gunicorn", "-c", "hproxy/config/gunicorn.py", "--worker-class",
         "sanic.worker.GunicornWorker", 'hproxy.server:app'],
        ["pipenv", "run", "python", "hproxy/scheduled_task.py"]
    ]
    procs = []
    for server in servers:
        proc = subprocess.Popen(server)
        procs.append(proc)
    for proc in procs:
        proc.wait()
        if proc.poll():
            exit(0)
