#!/bin/sh
#-
# Tool to recreate index.htm and marker.htm from tpl/

set -ex
cd "$(realpath "$0/..")"
cat \
    tpl/0-prefix.htm \
    tpl/1-defloc.js \
    tpl/5-hookfn.js \
    tpl/9-suffix.htm \
    >index.htm~
mv index.htm~ index.htm
sed \
    -e '/<title>/s^.*$ <title>MirKarte with multiple markers (Alpha)</title>' \
    -e 's/mirkarte\.js/marker.js/g' \
    <index.htm >marker.htm~
mv marker.htm~ marker.htm
