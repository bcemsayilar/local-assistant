#!/bin/bash
# usage: sj.sh 'js'  -> runs JS in the Safari tab whose URL contains $TABMATCH (default appstoreconnect.apple.com/apps/)
JS="${1:-$(cat)}"
osascript - "$JS" "${TABMATCH:-appstoreconnect.apple.com/apps/}" <<'OSA'
on run argv
  tell application "Safari"
    repeat with w in windows
      repeat with t in tabs of w
        if (URL of t) contains (item 2 of argv) then return do JavaScript (item 1 of argv) in t
      end repeat
    end repeat
  end tell
  return "NOTAB"
end run
OSA
