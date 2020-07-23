#!/bin/bash

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

urlwatch \
  --config $HERE/urlwatch/config.yaml \
  --urls $HERE/urlwatch/urls.yaml \
  --hooks $HERE/urlwatch/hooks.py \
  --cache $HERE/urlwatch/cache.db \
  "$@"
