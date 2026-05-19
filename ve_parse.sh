#!/bin/sh
# ve_parse.sh — root shim (calls core/ve_parse.sh)
# CI compatibility shim. The real parser lives in core/ve_parse.sh
exec "$(dirname "$0")/core/ve_parse.sh" "$@"
