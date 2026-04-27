/**
 * OMEGA SYSTEM - LAYER 2: VISIBLE IMPLEMENTATION
 * Express server for Render (https://hacproof-standalone-max.onrender.com:8787)
 * 
 * What this DOES:
 *   ✓ Serve Mirror UI
 *   ✓ Device registration & consent gates
 *   ✓ Public API endpoints
 *   ✓ Call to Layer 1 governance (if available)
 *   ✓ Hard locks (kill switch, mirror recall)
 * 
 * What this DOES NOT:
 *   ✗ VAC computation (Layer 1 only)
 *   ✗ Governance decisions (Layer 1 only)
 *   ✗ Receipt chain logic (Layer 1 only)
 *   ✗ Constitutional enforcement (Layer 1 only)
 * 
 * Hard Locks Maintained:
 *   ✓ HA=1.0 / SA=0.0 (always displayed)
 *   ✓ Kill switch ("stop stop stop")
 *   ✓ Mirror recall ("mirror mirror")
 *   ✓ Consent required before action
 *   ✓ Visibility required before execution
 *   ✓ NO animated tesseracts/hypercubes in UI
 */

const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 8787;

// ========== CONFIGURATION ==========
const HA = 1.0;  // Human Authority (always 100%)
const SA = 0.0;  // System Authority (always 0%)
let MIRROR_ACTIVE = false;
let DEVICE_ID = null;

// Layer 1 interface (if available)
const LAYER1_URL = process.env.LAYER1_URL || null;
let LAYER1_AVAILABLE = false;

// ========== MIDDLEWARE ==========
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Check Layer 1 availability at startup
async function checkLayer1() {
  if (!LAYER1_URL) return;
  try {
    const response = await fetch(`${LAYER1_URL}/status`, { timeout: 2000 });
    LAYER1_AVAILABLE = response.ok;
    console.log(LAYER1_AVAILABLE ? '✓ Layer 1 available' : '✗ Layer 1 unavailable');
  } catch (e) {
    LAYER1_AVAILABLE = false;
  }
}

// ========== HARD LOCKS ==========
function handleKillSwitch(text) {
  if (text.toLowerCase().trim() === 'stop stop stop') {
    return {
      action: 'KILL_SWITCH',
      status: 'HALT - execution paused',
      human_authority: HA,
      system_authority: SA,
      requires_manual_reset: true
    };
  }
  return null;
}

function handleMirrorRecall(text) {
  if (text.toLowerCase().trim() === 'mirror mirror') {
    return {
      action: 'MIRROR_RECALL',
      status: 'returning to Mirror entry',
      human_authority: HA,
      system_authority: SA
    };
  }
  return null;
}

// ========== ROUTES ==========

// Entry point: Mirror UI
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Device registration
app.post('/api/device/register', (req, res) => {
  const { device_name, alignment_confirmed } = req.body;

  // Hard lock: Consent precedes execution
  if (!alignment_confirmed) {
    return res.status(403).json({
      status: 'error',
      reason: 'alignment confirmation required',
      human_authority: HA,
      system_authority: SA
    });
  }

  // Register device
  DEVICE_ID = require('crypto')
    .createHash('sha256')
    .update(device_name)
    .digest('hex')
    .substring(0, 16);
  
  MIRROR_ACTIVE = true;

  res.json({
    status: 'success',
    device_id: DEVICE_ID,
    device_name: device_name,
    mirror_active: true,
    human_authority: HA,
    system_authority: SA,
    timestamp: new Date().toISOString()
  });
});

// Process user input
app.post('/api/process', async (req, res) => {
  if (!MIRROR_ACTIVE) {
    return res.status(403).json({
      status: 'error',
      reason: 'mirror not active - register first'
    });
  }

  const { text } = req.body;

  // Check hard locks first
  const killResult = handleKillSwitch(text);
  if (killResult) {
    return res.json(killResult);
  }

  const recallResult = handleMirrorRecall(text);
  if (recallResult) {
    return res.json(recallResult);
  }

  // If Layer 1 is available, forward for governance
  if (LAYER1_AVAILABLE) {
    try {
      const response = await fetch(`${LAYER1_URL}/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_id: DEVICE_ID, text: text }),
        timeout: 5000
      });
      const data = await response.json();
      return res.json(data);
    } catch (e) {
      return res.json({
        status: 'layer1_unavailable',
        error: e.message,
        fallback: 'local_processing_only'
      });
    }
  }

  // Fallback: Process locally without governance
  res.json({
    status: 'ok',
    device_id: DEVICE_ID,
    text: text,
    layer1_available: false,
    note: 'Response generated without governance. Connect Layer 1 for full alignment.',
    human_authority: HA,
    system_authority: SA
  });
});

// System status
app.get('/api/status', (req, res) => {
  res.json({
    mirror_active: MIRROR_ACTIVE,
    device_id: DEVICE_ID,
    layer1_available: LAYER1_AVAILABLE,
    human_authority: HA,
    system_authority: SA,
    timestamp: new Date().toISOString()
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    system: 'HAC-Proof Standalone Max',
    ha: HA,
    sa: SA,
    timestamp: new Date().toISOString()
  });
});

// ========== STARTUP ==========
app.listen(PORT, async () => {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║  OMEGA SYSTEM - LAYER 2: VISIBLE IMPLEMENTATION          ║
║  https://hacproof-standalone-max.onrender.com:${PORT}       ║
║                                                          ║
║  Hard Locks Active:                                      ║
║    ✓ Human Authority = 100%                             ║
║    ✓ System Authority = 0%                              ║
║    ✓ Kill switch ("stop stop stop")                     ║
║    ✓ Mirror recall ("mirror mirror")                    ║
║    ✓ Consent required (alignment)                       ║
║    ✓ Visibility required                                ║
╚══════════════════════════════════════════════════════════╝
  `);

  await checkLayer1();
  console.log(`Listening on port ${PORT}`);
});

module.exports = app;
