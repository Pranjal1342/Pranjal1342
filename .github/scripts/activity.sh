#!/usr/bin/env bash
# Rewrites the README block between the ACTIVITY markers with the latest commit from each recently pushed public repo.
# Uses /repos + /commits, not the Events API: since 2025 PushEvent payloads no longer include commit messages.
set -euo pipefail
user="${GITHUB_REPOSITORY_OWNER:?}"
readme="${1:-README.md}"
api() { curl -fsSL -H "Authorization: Bearer ${GH_TOKEN:?}" -H "Accept: application/vnd.github+json" "https://api.github.com/$1"; }

repos=$(api "users/$user/repos?type=owner&sort=pushed&per_page=15" |
  jq -r --arg self "$user/$user" '.[] | select(.fork | not) | select(.full_name != $self) | .full_name' | head -n 6)

lines=""
for repo in $repos; do
  # Empty repos return 409; skip them instead of failing the run.
  line=$(api "repos/$repo/commits?per_page=1" | jq -r --arg r "${repo#*/}" \
    '.[0] | "- [\($r)](\(.html_url)): \(.commit.message | split("\n")[0] | gsub("[<>\\[\\]`]"; "")) · \(.commit.committer.date[:10])"') || continue
  lines+="$line"$'\n'
done

[ -n "$lines" ] || { echo "no activity found; README left unchanged"; exit 0; }

# ENVIRON (not awk -v) so backslashes in commit messages are kept literally.
BLOCK="$lines" awk '
  /<!-- ACTIVITY:START -->/ { print; printf "%s", ENVIRON["BLOCK"]; skip = 1; next }
  /<!-- ACTIVITY:END -->/   { skip = 0 }
  !skip
' "$readme" > "$readme.tmp" && mv "$readme.tmp" "$readme"
