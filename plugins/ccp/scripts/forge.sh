#!/usr/bin/env bash
# Open or show a project-management view on whichever forge this repo uses.
#
# Detects GitHub vs GitLab by asking gh and glab themselves whether they
# recognize the current repo, rather than guessing from the remote URL, so
# self-hosted GitHub Enterprise and GitLab instances work the same as
# github.com and gitlab.com.
set -euo pipefail

ACTION="${1:?usage: forge.sh <issues|actions|prs|pr|repo|project>}"

open_url() {
  local url="$1"
  if command -v open >/dev/null 2>&1; then
    open "$url"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url"
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c "import webbrowser,sys; webbrowser.open(sys.argv[1])" "$url"
  else
    echo "$url"
  fi
}

glab_web_url() {
  glab repo view -F json | python3 -c "import json,sys; print(json.load(sys.stdin)['web_url'])"
}

forge=""
if command -v gh >/dev/null 2>&1 && gh repo view >/dev/null 2>&1; then
  forge="gh"
elif command -v glab >/dev/null 2>&1 && glab repo view >/dev/null 2>&1; then
  forge="glab"
else
  echo "Could not detect a GitHub or GitLab remote for this repo (checked gh and glab)." >&2
  exit 1
fi

case "$forge:$ACTION" in
  gh:issues) gh issue list --web ;;
  gh:actions) gh browse --actions ;;
  gh:prs) gh pr list --web ;;
  gh:pr) gh pr view ;;
  gh:repo) gh repo view --web ;;
  gh:project) gh browse --projects ;;
  glab:issues) open_url "$(glab_web_url)/-/issues" ;;
  glab:actions) open_url "$(glab_web_url)/-/pipelines" ;;
  glab:prs) open_url "$(glab_web_url)/-/merge_requests" ;;
  glab:pr) glab mr view ;;
  glab:repo) glab repo view --web ;;
  glab:project) open_url "$(glab_web_url)/-/boards" ;;
  *)
    echo "Unknown action: $ACTION" >&2
    exit 1
    ;;
esac
