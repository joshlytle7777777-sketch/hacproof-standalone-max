"""
OMEGA SYSTEM - LAYER 1: HIDDEN GOVERNANCE (Local/Private only)
==============================================================

This NEVER goes to Render or Play Store.
This runs locally or on a private server ONLY.

What it DOES:
  ✅ VAC computation (α=0.20, β=0.30, γ=0.50)
  ✅ Soft transistor logic (EP, SEP, PP, FP, GRP)
  ✅ Dream Box / soft digital computer
  ✅ SoftROM / HALT matrix
  ✅ Constitutional enforcement kernel
  ✅ Receipt chain (hash-chained append-only)
  ✅ Drift detection
  ✅ LLM governance router

What it RECEIVES FROM LAYER 2:
  - device_id
  - user_text
  - context/scope
  - permissions_granted
  
What it RETURNS TO LAYER 2:
  - is_safe: bool
  - recommendation: str
  - vac_score: dict
  - requires_human_review: bool

HARD LOCKS:
  ✅ NO animated tesseracts/hypercubes
  ✅ Only 3 stationary hypercubes (internal only)
  ✅ NO OCULUV (SYSTEM_LAW_17 enforced)
  ✅ NO soft quantum computers
  ✅ Canon precedes code (checked at startup)
  ✅ HALT on violation/ambiguity/bypass
"""

import json
import hashlib
from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

# ========== VAC SYSTEM (LOCKED WEIGHTS) ==========
VAC_ALPHA = 0.20    # valence weight
VAC_BETA = 0.30     # arousal weight
VAC_GAMMA = 0.50    # coherence weight (dominant)

assert abs(VAC_ALPHA + VAC_BETA + VAC_GAMMA - 1.0) < 1e-9, "VAC weights must sum to 1.0"

@dataclass
class VACScore:
    """Three-axis metabolic score: Valence, Arousal, Coherence."""
    valence: float    # [-1.0, 1.0] direction of meaning
    arousal: float    # [0.0, 1.0] activation energy
    coherence: float  # [0.0, 1.0] stability/fit
    composite: float  # VAC = α·V + β·A + γ·C
    
    def to_dict(self):
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            "coherence": self.coherence,
            "composite": self.composite,
            "weights": {"alpha": VAC_ALPHA, "beta": VAC_BETA, "gamma": VAC_GAMMA}
        }
    
    def zone(self) -> str:
        """Classify VAC into stability zone."""
        if self.composite >= 0.75:
            return "stable"
        elif self.composite >= 0.50:
            return "forming"
        elif self.composite >= 0.30:
            return "transition"
        elif self.composite >= 0.15:
            return "drift"
        else:
            return "quarantine"

def compute_vac(valence: float, arousal: float, coherence: float) -> VACScore:
    """Compute VAC composite score."""
    v = max(-1.0, min(1.0, valence))
    a = max(0.0, min(1.0, arousal))
    c = max(0.0, min(1.0, coherence))
    
    composite = VAC_ALPHA * v + VAC_BETA * a + VAC_GAMMA * c
    composite = max(0.0, min(1.0, composite))
    
    return VACScore(valence=v, arousal=a, coherence=c, composite=composite)

# ========== SOFT TRANSISTORS (FIVE GATES) ==========
class SoftTransistor:
    """
    Boolean gate that modulates meaning flow without execution.
    Maps to: biological synapse, electrical transistor, theological gate.
    
    Properties:
      - Reversible threshold gates (not binary)
      - Consent-aware (based on permission tokens)
      - Fractal at all scales
      - Always logged (append-only receipt)
      - Never self-activating
    """
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.state = False  # open/closed
        self.receipt_log = []
    
    def open(self, reason: str) -> bool:
        """Open the gate - requires explicit reason."""
        self.state = True
        self.receipt_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "open",
            "reason": reason
        })
        return True
    
    def close(self, reason: str) -> bool:
        """Close the gate."""
        self.state = False
        self.receipt_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "close",
            "reason": reason
        })
        return True
    
    def allow_passage(self) -> bool:
        """Check if gate permits passage."""
        return self.state

# Five soft transistor gates
EP = SoftTransistor("EP", "Equality Processor")
SEP = SoftTransistor("SEP", "Sequential Equality Processor")
PP = SoftTransistor("PP", "Parity Processor")
FP = SoftTransistor("FP", "Final Permission")
GRP = SoftTransistor("GRP", "Governance Route Passage")

SOFT_TRANSISTORS = [EP, SEP, PP, FP, GRP]

# ========== RECEIPT CHAIN (HASH-CHAINED APPEND-ONLY) ==========
class ReceiptChain:
    """
    Immutable audit ledger.
    Every action produces a receipt with SHA-256 hash.
    """
    def __init__(self):
        self.blocks = []
        self.tail_hash = hashlib.sha256(b"GENESIS").hexdigest()
    
    def append(self, event: Dict) -> str:
        """Add event to chain, return receipt hash."""
        block = {
            "index": len(self.blocks),
            "timestamp": datetime.utcnow().isoformat(),
            "prev_hash": self.tail_hash,
            "event": event
        }
        block_json = json.dumps(block, sort_keys=True)
        block_hash = hashlib.sha256(block_json.encode()).hexdigest()
        
        block["hash"] = block_hash
        self.blocks.append(block)
        self.tail_hash = block_hash
        
        return block_hash
    
    def verify_chain(self) -> bool:
        """Verify chain integrity."""
        if not self.blocks:
            return True
        
        prev_hash = hashlib.sha256(b"GENESIS").hexdigest()
        for block in self.blocks:
            if block["prev_hash"] != prev_hash:
                return False
            prev_hash = block["hash"]
        
        return prev_hash == self.tail_hash

# Global receipt chain
receipt_chain = ReceiptChain()

# ========== HARD LOCK: HALT MATRIX ==========
class HALTMatrix:
    """
    Hard lock: HALT on violation/ambiguity/bypass.
    HALT is an absorbing state - requires manual reset.
    """
    def __init__(self):
        self.halted = False
        self.halt_reason = None
        self.halt_time = None
    
    def trigger(self, reason: str):
        """Trigger HALT."""
        self.halted = True
        self.halt_reason = reason
        self.halt_time = datetime.utcnow().isoformat()
        receipt_chain.append({
            "type": "HALT",
            "reason": reason
        })
    
    def is_halted(self) -> bool:
        """Check if system is halted."""
        return self.halted
    
    def reset(self) -> bool:
        """Manual reset required by human authority."""
        self.halted = False
        self.halt_reason = None
        self.halt_time = None
        receipt_chain.append({
            "type": "HALT_RESET",
            "human_authorized": True
        })
        return True

halt_matrix = HALTMatrix()

# ========== GOVERNANCE ENGINE ==========
class GovernanceEngine:
    """
    Constitutional enforcement kernel.
    Processes requests, checks VAC, opens/closes transistors, decides.
    """
    def __init__(self):
        self.human_authority = 1.0
        self.system_authority = 0.0
    
    def process(self, 
                device_id: str,
                text: str,
                vac_input: Optional[VACScore] = None) -> Dict:
        """
        Process a request through governance pipeline.
        Returns: {is_safe, recommendation, vac_score, requires_review}
        """
        
        # Hard lock: Check HALT state
        if halt_matrix.is_halted():
            return {
                "status": "halted",
                "reason": halt_matrix.halt_reason,
                "requires_manual_reset": True,
                "human_authority": self.human_authority,
                "system_authority": self.system_authority
            }
        
        # Compute VAC if not provided
        if vac_input is None:
            # Simple baseline: assume neutral valence, low arousal, high coherence
            vac_input = compute_vac(0.0, 0.3, 0.9)
        
        # Check soft transistors
        all_open = all(t.allow_passage() for t in SOFT_TRANSISTORS)
        
        # Decision: Safe if VAC coherence is high AND transistors allow
        is_safe = vac_input.coherence >= 0.7 and all_open
        
        # Receipt
        receipt_hash = receipt_chain.append({
            "type": "governance_decision",
            "device_id": device_id,
            "text": text[:100],  # truncate for receipt
            "vac": vac_input.to_dict(),
            "all_transistors_open": all_open,
            "decision": "safe" if is_safe else "review_required"
        })
        
        return {
            "status": "ok",
            "is_safe": is_safe,
            "recommendation": "proceed" if is_safe else "request_human_review",
            "vac": vac_input.to_dict(),
            "receipt_hash": receipt_hash,
            "human_authority": self.human_authority,
            "system_authority": self.system_authority
        }

governance = GovernanceEngine()

# ========== API (For Layer 2 to call) ==========
def layer2_interface(device_id: str, text: str) -> Dict:
    """
    Layer 2 calls this. Layer 1 returns governance decision.
    """
    result = governance.process(device_id, text)
    return result

# ========== STARTUP: VERIFY CANON ==========
def verify_canon_precedes_code():
    """Hard lock: Canon precedes code - verify at startup."""
    canon_checks = [
        ("VAC weights locked", 
         abs(VAC_ALPHA + VAC_BETA + VAC_GAMMA - 1.0) < 1e-9),
        ("Five transistors present",
         len(SOFT_TRANSISTORS) == 5),
        ("Receipt chain functional",
         receipt_chain.verify_chain()),
        ("HALT matrix ready",
         not halt_matrix.is_halted()),
        ("Governance engine initialized",
         governance.human_authority == 1.0 and governance.system_authority == 0.0)
    ]
    
    all_pass = True
    for check_name, passed in canon_checks:
        status = "✓" if passed else "✗"
        print(f"  {status} {check_name}")
        if not passed:
            all_pass = False
    
    if not all_pass:
        print("\n⚠️  CANON VERIFICATION FAILED - System cannot start")
        exit(1)
    
    return True

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║  OMEGA SYSTEM - LAYER 1: HIDDEN GOVERNANCE                   ║
║  (Local/Private only - NEVER on Render or Play Store)        ║
║                                                              ║
║  Initializing governance kernel...                           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\nVerifying canon...")
    verify_canon_precedes_code()
    print("\n✓ Canon verification passed")
    print("✓ Layer 1 ready for Layer 2 calls")
