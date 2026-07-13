#!/bin/bash
# ============================================================
# OmniVoice - Install Script for Google Colab
# Usage: bash install.sh [--share] [--demo|--infer]
# ============================================================

set -e

# ── Colors ──────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log()  { echo -e "${GREEN}[OmniVoice]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ── Parse args ──────────────────────────────────────────────
SHARE_FLAG=""
RUN_CMD="omnivoice-demo"

for arg in "$@"; do
  case $arg in
    --share) SHARE_FLAG="--share" ;;
    --demo)  RUN_CMD="omnivoice-demo" ;;
    --infer) RUN_CMD="omnivoice-infer" ;;
  esac
done

# ── Step 1: Install uv ──────────────────────────────────────
if ! command -v uv &>/dev/null; then
  log "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.cargo/bin:$PATH"
else
  log "uv already installed: $(uv --version)"
fi

# ── Step 2: Add uv tool bin to PATH ─────────────────────────
export PATH="/root/.local/bin:$HOME/.local/bin:$PATH"

# Persist PATH for the current shell session
if ! grep -q '/root/.local/bin' ~/.bashrc 2>/dev/null; then
  echo 'export PATH="/root/.local/bin:$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

# ── Step 3: Install OmniVoice ───────────────────────────────
log "Installing OmniVoice (this may take a few minutes)..."
uv tool install https://github.com/mrtruongleo/OmniVoice.git

# ── Step 4: Verify installation ─────────────────────────────
if command -v omnivoice-demo &>/dev/null; then
  log "✅ OmniVoice installed successfully!"
  log "Available commands:"
  echo "   omnivoice-demo        → Gradio web UI"
  echo "   omnivoice-infer       → Single inference"
  echo "   omnivoice-infer-batch → Batch inference"
else
  err "Installation failed. Commands not found in PATH."
fi

# ── Step 5: Run (optional) ──────────────────────────────────
if [[ "${RUN:-1}" == "1" ]]; then
  log "Starting $RUN_CMD $SHARE_FLAG ..."
  $RUN_CMD $SHARE_FLAG
fi
