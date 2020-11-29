# $MirOS: src/share/misc/licence.template,v 1.28 2008/11/14 15:33:44 tg Rel $
#-
# Copyright © 2014
#	mirabilos <m@mirbsd.org>
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
#-
# Helper script to download and convert data

unset LANGUAGE; export LC_ALL=C

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

exec >xkcd2js.out

# we always apply the 30W rule, so the code would need to be
# changed, both here and in the CGI, to go further west… but
# that would not scale either, anyway, plus we calculate all
# points using CET/CEST, so we don’t do that

for lat in 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56; do
	for lon in -6 -5 -4 -3 -2 -1 -0 0 1 2 3 4 5 6 7 8 9 10 11 12; do
		x=$(ftp -o - http://carabiner.peeron.com/xkcd/map/data/loc/$lat,$lon)
		x=$(xhtml_escape "$x")
		[[ $x = *'!/'* ]] && x="<a href=\"http://wiki.xkcd.com/${x##*'!/'}\">${x%'!/'*}</a>"
		print "	[\"$lat\", \"$lon\", $(json_escape "$x")],"
	done
done
print "	[\"666\", \"666\", \"\"]"
ls -la xkcd2js.out >&2
