#!/bin/bash
set -evx

mkdir ~/.hatchcore

# safety check
if [ ! -f ~/.hatchcore/.hatch.conf ]; then
  cp share/hatch.conf.example ~/.hatchcore/hatch.conf
fi
