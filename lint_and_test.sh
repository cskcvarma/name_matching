#!/usr/bin/env bash
set -euo pipefail

ruff check src tests
pytest --cov=src --cov-report=term-missing "$@"
