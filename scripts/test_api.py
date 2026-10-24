"""Test HTTP isolé du TP : ne touche pas au serveur de classe."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]

def main():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    proc = subprocess.Popen(
        [sys.executable, '-B', '-m', 'uvicorn', 'api.main:app',
         '--host', '127.0.0.1', '--port', str(port), '--log-level', 'error'],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL,
    )
    def call(method, path, body=None, extra=None):
        headers = {'Content-Type': 'application/json'}
        headers.update(extra or {})
        data = None if body is None else json.dumps(body).encode('utf-8')
        req = Request(base + path, data=data, headers=headers, method=method)
        try:
            with urlopen(req, timeout=5) as res:
                raw = res.read()
                payload = (json.loads(raw) if 'application/json' in res.headers.get('content-type', '')
                           else raw.decode('utf-8')) if raw else None
                return res.status, payload, res.headers
        except HTTPError as err:
            raw = err.read()
            return err.code, json.loads(raw) if raw else None, err.headers
    try:
        deadline = time.monotonic() + 15
        while True:
            try:
                status, tasks, _ = call('GET', '/tasks')
                break
            except (URLError, TimeoutError):
                if proc.poll() is not None or time.monotonic() > deadline:
                    raise RuntimeError('Le serveur de test ne démarre pas')
                time.sleep(.1)
        assert status == 200 and len(tasks) == 2, (status, tasks)
        assert tasks[1]['title'] == 'Vérifier les alertes'
        print('OK GET 200 et caractères accentués')
        status, created, _ = call('POST', '/tasks', {'title': 'Test isolé'})
        assert status == 201 and created['done'] is False
        task_id = created['id']
        print('OK POST 201')
        status, updated, _ = call('PATCH', f'/tasks/{task_id}', {'done': True})
        assert status == 200 and updated['done'] is True
        assert updated['title'] == 'Test isolé'
        print('OK PATCH 200 et titre conservé')
        status, deleted, _ = call('DELETE', f'/tasks/{task_id}')
        assert status == 200 and deleted == {'deleted': task_id}
        assert all(t['id'] != task_id for t in call('GET', '/tasks')[1])
        print('OK DELETE 200 et absence confirmée par GET')
        assert call('PATCH', f'/tasks/{task_id}', {'done': False})[0] == 404
        assert call('POST', '/tasks', {})[0] == 422
        print('OK erreurs 404 et 422')
        status, _, headers = call('OPTIONS', '/tasks', extra={
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type',
        })
        assert status == 200
        assert headers['access-control-allow-origin'] == 'http://localhost:5173'
        print('OK CORS pour React localhost:5173')
        print('Tous les contrôles HTTP ont réussi sur une instance isolée.')
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)

if __name__ == '__main__':
    main()
