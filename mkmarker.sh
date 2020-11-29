#!/bin/sh
#-
# Tool to recreate marker.htm from index.htm

set -ex
cd "$(dirname "$0")"
sed \
    -e '/<title>/s^.*$ <title>MirKarte with multiple markers (Alpha)</title>' \
    -e 's/mirkarte\.js/marker.js/g' \
    <index.htm >marker.htm~
mv marker.htm~ marker.htm
