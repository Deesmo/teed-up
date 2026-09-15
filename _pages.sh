#!/bin/zsh
T=$(git -C "$HOME/teedup-site" config --get credential.helper >/dev/null 2>&1; echo)
if command -v gh >/dev/null 2>&1; then
  gh api -X POST repos/Deesmo/teed-up/pages/builds 2>&1 | head -5
  echo "--- latest ---"
  gh api repos/Deesmo/teed-up/pages/builds/latest 2>&1 | head -20
else
  echo "no gh"
fi
