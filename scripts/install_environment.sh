#!/usr/bin/env bash
set -euo pipefail

# Bootstraps a Python environment for the wing trade study.
# Supports online installs, optional wheelhouse installs, and optional
# no-build-isolation fallback for managed environments.

usage() {
  cat <<'USAGE'
Usage:
  scripts/install_environment.sh [options]

Options:
  --python PATH           Python executable to use (default: python)
  --wheelhouse DIR        Install from local wheelhouse only
  --no-build-isolation    Pass --no-build-isolation for editable install
  --skip-pip-upgrade      Skip pip self-upgrade step
  -h, --help              Show help

Examples:
  scripts/install_environment.sh
  scripts/install_environment.sh --python python3.11
  scripts/install_environment.sh --wheelhouse /opt/wheels
  scripts/install_environment.sh --no-build-isolation
USAGE
}

PYTHON_BIN="python"
WHEELHOUSE=""
NO_BUILD_ISOLATION=0
SKIP_PIP_UPGRADE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --python)
      PYTHON_BIN="${2:?missing value for --python}"
      shift 2
      ;;
    --wheelhouse)
      WHEELHOUSE="${2:?missing value for --wheelhouse}"
      shift 2
      ;;
    --no-build-isolation)
      NO_BUILD_ISOLATION=1
      shift
      ;;
    --skip-pip-upgrade)
      SKIP_PIP_UPGRADE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python executable not found: $PYTHON_BIN" >&2
  exit 1
fi

echo "[1/4] Using interpreter: $PYTHON_BIN"
"$PYTHON_BIN" --version

echo "[2/4] Upgrading pip"
if [[ "$SKIP_PIP_UPGRADE" -eq 0 ]]; then
  "$PYTHON_BIN" -m pip install -U pip
else
  echo "Skipping pip upgrade by request"
fi

echo "[3/4] Installing project and dev dependencies"
PIP_ARGS=(install -e '.[dev]')

if [[ -n "$WHEELHOUSE" ]]; then
  if [[ ! -d "$WHEELHOUSE" ]]; then
    echo "Wheelhouse directory does not exist: $WHEELHOUSE" >&2
    exit 1
  fi
  PIP_ARGS=(install --no-index --find-links "$WHEELHOUSE" -e '.[dev]')
fi

if [[ "$NO_BUILD_ISOLATION" -eq 1 ]]; then
  PIP_ARGS=(install --no-build-isolation "${PIP_ARGS[@]:1}")
fi

"$PYTHON_BIN" -m pip "${PIP_ARGS[@]}"

echo "[4/4] Running environment verification"
"$PYTHON_BIN" -m wing_trade_study.cli.main doctor

cat <<'DONE'
Environment bootstrap complete.

If solver imports fail, see:
  docs/environment_setup.md
DONE
