#!/bin/zsh
cd "$HOME/teedup-site" || exit 1
echo "HEAD: $(git log --oneline -1)"
git push origin main 2>&1 | tail -6
echo "EXIT:$?"
echo "REMOTE HEAD: $(git ls-remote origin main 2>&1 | head -1)"
