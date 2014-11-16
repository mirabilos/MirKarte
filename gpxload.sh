#!/bin/mksh
#-
# Copyright © 2014
#	Thorsten Glaser <tg@mirbsd.org>
#
# Provided that these terms and disclaimer and all copyright notices
# are retained or reproduced in an accompanying document, permission
# is granted to deal in this work without restriction, including un‐
# limited rights to use, publicly perform, distribute, sell, modify,
# merge, give away, or sublicence.
#
# This work is provided “AS IS” and WITHOUT WARRANTY of any kind, to
# the utmost extent permitted by applicable law, neither express nor
# implied; without malicious intent or gross negligence. In no event
# may a licensor, author or contributor be held liable for indirect,
# direct, other damage, loss, or other issues arising in any way out
# of dealing in the work, even if advised of the possibility of such
# damage or existence of a defect, except proven that it results out
# of said person’s immediate fault when using the work as intended.

set -o pipefail

if [[ ! -s $1 ]]; then
	print -ru2 "E: GPX '$1' not found"
	exit 1
fi
gpxf=$(realpath "$1")
cd "$(realpath "$0/..")"

# escape XHTML characters (three mandatory XML ones plus double quotes,
# the latter in an XML safe fashion numerically though)
function xhtml_escape {
	if (( $# )); then
		print -nr -- "$@"
	else
		cat
	fi | sed \
	    -e 's&\&amp;g' \
	    -e 's<\&lt;g' \
	    -e 's>\&gt;g' \
	    -e 's"\&#34;g'
}

# escape string into JSON string (with surrounding quotes)
function json_escape {
	[[ -o utf8-mode ]]; local u=$?
	set -U
	local o=\" s
	if (( $# )); then
		read -raN-1 s <<<"$*"
		unset s[${#s[*]}-1]
	else
		read -raN-1 s
	fi
	local -i i=0 n=${#s[*]} wc
	local -Uui16 -Z7 x
	local -i1 ch

	while (( i < n )); do
		(( ch = x = wc = s[i++] ))
		case $wc {
		(8) o+=\\b ;;
		(9) o+=\\t ;;
		(10) o+=\\n ;;
		(12) o+=\\f ;;
		(13) o+=\\r ;;
		(34) o+=\\\" ;;
		(92) o+=\\\\ ;;
		(*)
			if (( wc < 0x20 || wc > 0xFFFD || \
			    (wc >= 0xD800 && wc <= 0xDFFF) || \
			    (wc > 0x7E && wc < 0xA0) )); then
				o+=\\u${x#16#}
			else
				o+=${ch#1#}
			fi
			;;
		}
	done
	(( u )) && set +U
	print -nr -- "$o\""
}

# output is probably JSON (without the quotes!)… input MUST be UTF-8
function fast_json_export {
	set -e
	# GNU hexdump cannot output backslashes
	iconv -f utf-8 -t ucs-2be | hexdump -ve '"_u" 2/1 "%02X"' | tr _ \\
	set +e
}

rm -f gpxload.htm
while IFS= read -r line; do
	print -r -- "$line"
	[[ $line = *mirkarte_default_loc* ]] || continue
	print -r "  function mirkarte_hookfn(map) {"
	print -r "	nextpos = add_gpx_to_map(\"$(fast_json_export <"$gpxf")\", $(json_escape "$(xhtml_escape "$1")"));"
	print -r "	jumptonextpos();"
	print -r "  }"
done <index.htm >gpxload.htm

print -r -- "\$BROWSER file://$(realpath gpxload.htm)"
exit 0
