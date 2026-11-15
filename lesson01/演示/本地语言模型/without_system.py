#!/usr/bin/env python3
"""Launch llama-server behind a local gateway that drops system-role messages."""
import json
import signal
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BACKEND = 'http://127.0.0.1:8088'


def strip_system(body):
    if isinstance(body, dict) and isinstance(body.get('messages'), list):
        body['messages'] = [m for m in body['messages'] if m.get('role') != 'system']
    return body


class Gateway(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def forward(self):
        try:
            data = None
            if self.command == 'POST':
                data = self.rfile.read(int(self.headers.get('Content-Length', '0')))
                if 'application/json' in self.headers.get('Content-Type', ''):
                    data = json.dumps(strip_system(json.loads(data)), ensure_ascii=False).encode()
            request = urllib.request.Request(BACKEND + self.path, data=data, method=self.command)
            for key in ['Content-Type', 'Accept', 'Authorization']:
                if key in self.headers:
                    request.add_header(key, self.headers[key])
            try:
                response = urllib.request.urlopen(request, timeout=180)
            except urllib.error.HTTPError as exc:
                response = exc
            with response:
                self.send_response(response.status)
                for key, value in response.headers.items():
                    if key.lower() not in {'transfer-encoding', 'connection', 'content-length'}:
                        self.send_header(key, value)
                self.send_header('Connection', 'close')
                self.end_headers()
                while chunk := response.read1(4096):
                    self.wfile.write(chunk)
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except (urllib.error.URLError, ValueError, TimeoutError) as exc:
            self.send_error(502, str(exc))

    do_GET = forward
    do_POST = forward
    do_OPTIONS = forward
    do_HEAD = forward


def main():
    # Bind first so an occupied public port does not leave an orphan backend.
    server = ThreadingHTTPServer(('127.0.0.1', 8087), Gateway)
    backend = subprocess.Popen(sys.argv[1:])
    def shutdown(*_):
        threading.Thread(target=server.shutdown, daemon=True).start()
    signal.signal(signal.SIGTERM, shutdown)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        backend.terminate()
        try:
            backend.wait(timeout=10)
        except subprocess.TimeoutExpired:
            backend.kill()
            backend.wait()


if __name__ == '__main__':
    main()
