# Dockerfile — Vulpine Echo (VE)
# Deterministic environment for running VE on any Linux/Mac host.
# PowerShell steps require Windows or a separate PS runner.
#
# Build:  docker build -t vulpine-echo .
# Run:    docker run --rm vulpine-echo python ledger/ve_quickcheck.py --ledger ve_ledger.jsonl
# Test:   docker run --rm vulpine-echo python -m pytest Tests/ -v

FROM python:3.11-slim

LABEL maintainer="@BioAnkh84"
LABEL description="Vulpine Echo — trust-gated execution harness"
LABEL version="0.1b"

WORKDIR /ve

# System deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy repo
COPY . .

# Python — no external dependencies (stdlib only)
# requirements.txt exists for documentation; nothing to install
RUN python --version && python -c "import hashlib, json, argparse; print('stdlib OK')"

# Verify gate logic is importable
RUN python -c "from core.ve_gatecheck import gate; assert gate(0.9,0.9,0.1)=='PROCEED'"

# Smoke test
RUN python core/ve_kernel.py quickcheck

ENTRYPOINT ["python"]
CMD ["core/ve_kernel.py", "quickcheck"]
