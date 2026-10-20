"""Local teaching runner. Run only on the instructor's own computer."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
TOKEN = secrets.token_urlsafe(24)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path == '/session':
            # Same-origin page gets the token; no cross-origin access is enabled.
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(json.dumps({'token': TOKEN}).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != '/run' or self.headers.get('X-Demo-Token') != TOKEN:
            self.send_error(403)
            return
        size = int(self.headers.get('Content-Length', 0))
        if size > 20000:
            self.send_error(413)
            return
        try:
            code = json.loads(self.rfile.read(size))['code']
            with tempfile.TemporaryDirectory(prefix='aimat-demo-') as folder:
                env = os.environ.copy()
                env['MPLBACKEND'] = 'Agg'
                result = subprocess.run([sys.executable, '-I', '-c', code], cwd=folder,
                                        env=env, capture_output=True, text=True, timeout=8)
            payload = {'output': (result.stdout + result.stderr)[-12000:], 'ok': result.returncode == 0}
        except subprocess.TimeoutExpired:
            payload = {'output': '执行超过 8 秒，已停止。请检查循环。', 'ok': False}
        except Exception as exc:
            payload = {'output': str(exc), 'ok': False}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode())

if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 8765), Handler)
    print('Open http://127.0.0.1:8765/ — Ctrl+C to stop.', flush=True)
    print('代码使用本机 Python 执行，不是安全沙箱；仅运行自己的课堂代码。', flush=True)
    server.serve_forever()
