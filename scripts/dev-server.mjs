import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import readline from 'node:readline';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const webRoot = path.join(root, 'web');
const args = process.argv.slice(2);
const option = (name, fallback) => {
  const index = args.indexOf(name);
  if (index >= 0 && args[index + 1]) return args[index + 1];
  const inline = args.find(arg => arg.startsWith(`${name}=`));
  return inline?.slice(name.length + 1) || fallback;
};
const port = Number(option('--port', process.env.PORT || 7100));
const host = option('--host', '0.0.0.0');
const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json; charset=utf-8' };

let engine;
let engineUrl;
const engineReady = new Promise(resolve => {
  const executable = ['build/JudgeBox.exe', 'JudgeBox.exe'].map(file => path.join(root, file)).find(existsSync);
  if (!executable) { resolve(null); return; }
  engine = spawn(executable, ['--no-browser', '--data-dir', path.join(root, '.runtime', 'dev-preview')], { cwd: root, stdio: ['ignore', 'pipe', 'ignore'] });
  const lines = readline.createInterface({ input: engine.stdout });
  lines.once('line', line => { engineUrl = line.trim(); lines.close(); resolve(engineUrl); });
  engine.once('error', () => resolve(null));
  engine.once('exit', () => resolve(null));
});

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    if (url.pathname.startsWith('/api/')) {
      const target = await engineReady;
      if (!target) {
        res.writeHead(503, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ error: '未找到 JudgeBox 引擎，请先运行 build.ps1。' }));
        return;
      }
      const [base, token = ''] = target.split('/#');
      const body = ['POST', 'PUT', 'PATCH'].includes(req.method) ? Buffer.concat(await Array.fromAsync(req)) : undefined;
      const response = await fetch(base + url.pathname + url.search, {
        method: req.method,
        headers: { 'Content-Type': 'application/json', 'X-JudgeBox-Token': token },
        body
      });
      res.writeHead(response.status, { 'Content-Type': response.headers.get('content-type') || 'application/json; charset=utf-8' });
      res.end(Buffer.from(await response.arrayBuffer()));
      return;
    }
    const requested = url.pathname === '/' ? 'index.html' : decodeURIComponent(url.pathname.slice(1));
    const file = path.resolve(webRoot, requested);
    if (!file.startsWith(webRoot + path.sep)) throw new Error('Invalid path');
    const content = await readFile(file);
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    res.end(content);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Not found');
  }
});

server.listen(port, host, () => console.log(`JudgeBox preview: http://localhost:${port}`));
function shutdown() {
  server.close();
  if (engine && !engine.killed) engine.kill();
}
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
