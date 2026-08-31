#!/usr/bin/env bash
# migrate.sh - move one existing app site into its subfolder on the new domain.
#
# Usage:
#   ./scripts/migrate.sh <app> <path-to-existing-site-folder> <new-domain>
#   ./scripts/migrate.sh pacingguard ~/sites/pacingguard-export kstech.app
#
# apps: pacingguard | respirix | lull | spacesift | promptuary
#
# What it does:
#   1. Replaces the holding page: copies your existing site files into <app>/
#   2. Rewrites absolute URLs (https://old-domain/...) -> https://<new-domain>/<app>/...
#      This covers <link rel="canonical">, og:url, og:image and internal absolute links.
#   3. Prefixes root-relative paths (href="/x", src="/x") with /<app>/ so nothing
#      breaks under the subdirectory.
#   4. Prints a grep QA report: leftover old-domain references, support@ emails
#      to review, and the canonical/og lines to eyeball.
#
# Written for macOS (BSD sed/grep, bash 3.2) and Linux. Runs offline.

set -euo pipefail

APP="${1:-}"; SRC="${2:-}"; DOMAIN="${3:-}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() { grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
[ -n "$APP" ] && [ -n "$SRC" ] && [ -n "$DOMAIN" ] || usage
[ -d "$SRC" ] || { echo "ERROR: source folder not found: $SRC"; exit 1; }

# Old domain(s) per app. Lull has two: the pages.dev URL it is served from
# and lull.app, which its canonical tags point to.
case "$APP" in
  pacingguard) OLD="pacingguard.app" ;;
  respirix)    OLD="respirix.app" ;;
  spacesift)   OLD="spacesift.app" ;;
  promptuary)  OLD="promptuaryapp.com" ;;
  lull)        OLD="lull.app lull-website.pages.dev" ;;
  *) echo "ERROR: unknown app '$APP'"; usage ;;
esac

DEST="$ROOT/$APP"
echo "==> $APP: $SRC -> $DEST  (new base: https://$DOMAIN/$APP/)"

rm -rf "$DEST"
mkdir -p "$DEST"
cp -R "$SRC"/. "$DEST"/

# Collect text files to rewrite (html/css/js/xml/txt/json/webmanifest)
FILES=$(find "$DEST" -type f \( -name '*.html' -o -name '*.htm' -o -name '*.css' \
        -o -name '*.js' -o -name '*.xml' -o -name '*.txt' -o -name '*.json' \
        -o -name '*.webmanifest' \))

if [ -n "$FILES" ]; then
  # 1) absolute old-domain URLs -> new domain + subpath
  for D in $OLD; do
    E=$(printf '%s' "$D" | sed 's/\./\\./g')
    echo "$FILES" | while IFS= read -r F; do
      sed -i.bak -E "s#https?://(www\.)?$E#https://$DOMAIN/$APP#g" "$F"
    done
  done
  # 2) root-relative paths -> /<app>/-prefixed (skip protocol-relative //)
  #    covers href/src/srcset/poster attributes and CSS url(/...) incl. url("/ and url('/
  echo "$FILES" | while IFS= read -r F; do
    sed -i.bak -E "s#(href|src|srcset|poster)=\"/([^/])#\1=\"/$APP/\2#g" "$F"
    sed -i.bak -E "s#(href|src|srcset|poster)=\"/\"#\1=\"/$APP/\"#g" "$F"
    sed -i.bak -E "s#url\((\"|')?/([^/])#url(\1/$APP/\2#g" "$F"
  done
  find "$DEST" -name '*.bak' -delete
fi

echo
echo "---- QA report ----------------------------------------------"
echo "[1] Leftover old-domain references (should be empty or intentional):"
grep -rn "pacingguard\.app\|respirix\.app\|spacesift\.app\|promptuaryapp\.com\|lull\.app\|pages\.dev" "$DEST" \
  | grep -v "apps\.apple\.com" || echo "    none"
echo
echo "[2] support@ addresses found (update to the new domain before old domains lapse):"
grep -rno "support@[A-Za-z0-9.-]*" "$DEST" | sort -u || echo "    none"
echo
echo "[3] Canonical / OG lines to eyeball:"
grep -rn 'rel="canonical"\|og:url\|og:image' "$DEST" | head -20 || echo "    none"
echo
echo "[4] Multi-URL srcset values with root-relative entries (fix by hand if any):"
grep -rn 'srcset="[^"]*[, ] */[^/]' "$DEST" || echo "    none"
echo "--------------------------------------------------------------"
echo "Done. Open https://$DOMAIN/$APP/ after deploy and click through nav,"
echo "assets and the support/privacy/terms links."
