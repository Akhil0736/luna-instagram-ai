#!/usr/bin/env node
/* Simple connectivity test for services */

const OPENMANUS_URL = process.env.OPENMANUS_URL || 'http://localhost:8091';
const RIONA_URL = process.env.RIONA_URL || 'http://localhost:3001/api';

async function main() {
  const results = { openmanus: null, riona: null };

  try {
    const res = await fetch(`${OPENMANUS_URL}/health`);
    const json = await res.json();
    results.openmanus = { ok: res.ok, data: json };
    console.log('[OpenManus] /health:', res.status, json);
  } catch (e) {
    results.openmanus = { ok: false, error: String(e) };
    console.error('[OpenManus] /health error:', e);
  }

  try {
    const res = await fetch(`${RIONA_URL}/status`);
    const json = await res.json();
    results.riona = { ok: res.ok, data: json };
    console.log('[Riona] /status:', res.status, json);
  } catch (e) {
    results.riona = { ok: false, error: String(e) };
    console.error('[Riona] /status error:', e);
  }

  const allOk = results.openmanus?.ok && results.riona?.ok;
  if (!allOk) {
    console.error('One or more services failed the health check:', results);
    process.exit(1);
  }
  console.log('All base service checks passed.');
}

main();
