#!/usr/bin/env node
/* E2E: login -> enqueue actions -> poll status */

const RIONA_URL = process.env.RIONA_URL || 'http://localhost:3001/api';
const SESSION_ID = process.env.IG_SESSION_ID || process.env.RIONA_IG_SESSION_ID;

if (!SESSION_ID) {
  console.log('[E2E] Skipping run: please set IG_SESSION_ID (Instagram sessionid cookie value)');
  process.exit(0);
}

async function main() {
  let cookie = '';

  // Login with session cookie
  const loginRes = await fetch(`${RIONA_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId: SESSION_ID }),
    redirect: 'manual',
  });
  const setCookie = loginRes.headers.get('set-cookie');
  if (!loginRes.ok || !setCookie) {
    const text = await loginRes.text().catch(() => '');
    throw new Error(`[E2E] Login failed: ${loginRes.status} ${text}`);
  }
  cookie = setCookie.split(';')[0];
  console.log('[E2E] Login OK');

  // Enqueue actions
  const actions = [{ type: 'interact' }];
  const enqueueRes = await fetch(`${RIONA_URL}/actions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Cookie: cookie },
    body: JSON.stringify({ actions }),
  });
  if (!enqueueRes.ok) {
    const text = await enqueueRes.text().catch(() => '');
    throw new Error(`[E2E] Enqueue failed: ${enqueueRes.status} ${text}`);
  }
  const { id, statusUrl } = await enqueueRes.json();
  console.log('[E2E] Enqueued. id=', id, 'statusUrl=', statusUrl);

  // Poll status
  const maxMs = Number(process.env.E2E_MAX_MS) || 60_000;
  const intervalMs = Number(process.env.E2E_INTERVAL_MS) || 2_000;
  const start = Date.now();
  while (Date.now() - start < maxMs) {
    const statusRes = await fetch(`${RIONA_URL}/actions/${id}`, {
      headers: { Cookie: cookie },
    });
    const json = await statusRes.json().catch(() => null);
    console.log('[E2E] Status:', json);
    if (json && (json.status === 'completed' || json.status === 'failed')) {
      if (json.status === 'completed') {
        console.log('[E2E] Completed successfully.');
        process.exit(0);
      } else {
        console.error('[E2E] Failed:', json);
        process.exit(1);
      }
    }
    await new Promise((r) => setTimeout(r, intervalMs));
  }
  console.error('[E2E] Timeout waiting for completion');
  process.exit(1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
