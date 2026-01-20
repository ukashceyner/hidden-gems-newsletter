#!/usr/bin/env bash
# gems.sh  — fetch fresh ≥50★ repos from the last 7 days
set -eo pipefail

# ── Config ────────────────────────────────────────────────
DAYS_BACK=7          # how many days of history
STAR_MIN=50          # minimum stars
LIMIT=50             # how many repos to fetch
# ───────────────────────────────────────────────────────────

# Compute dates on both macOS (BSD date) and Linux (GNU date)
if date -v-1d >/dev/null 2>&1; then              # BSD (macOS)
  START=$(date -v-"$DAYS_BACK"d +%Y-%m-%d)
  TODAY=$(date +%d-%m-%Y)
else                                             # GNU (Linux / GitHub runner)
  START=$(date -d "$DAYS_BACK days ago" +%Y-%m-%d)
  TODAY=$(date +%d-%m-%Y)
fi

OUTPUT_FILE="${TODAY}.json"


gh search repos \
  --created=">=$START" \
  --stars=">=${STAR_MIN}" \
  --sort=stars --order=desc --limit="$LIMIT" \
  --json=name,fullName,url,description,language,stargazersCount,createdAt \
| jq 'map({
      createdAt,
      stars:        .stargazersCount,
      name:         .fullName,
      url,
      lang:         .language,
      desc:         (.description // "")
    })' > "$OUTPUT_FILE"

echo "✅  Saved $(jq length "$OUTPUT_FILE") fresh repos (≥${STAR_MIN}★, since $START) to $OUTPUT_FILE"
