#!/bin/sh
# ve_kernel.sh — root shim (calls core/ve_kernel.sh)
# CI compatibility shim. The real kernel shell lives in core/ve_kernel.sh
exec "$(dirname "$0")/core/ve_kernel.sh" "$@"
