#!/bin/mksh
#-
# Copyright © 2007, 2008, 2012, 2013, 2014, 2020
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

unset LANGUAGE; export LC_ALL=C
unset HTTP_PROXY

#XXX make these CGI parameters
deflat=50.7
deflon=7.11
defzoom=8

#XXX add attribution (either to #map_coors or by moving CGI content
#XXX into a layer; maybe even make an AJAX version of the CGIs that
#XXX merge all the CGIs into layers)

# magic from MirOS: src/kern/c/mirtime.c,v 1.3 2011/11/20 23:40:10 tg Exp $

# struct tm members and (POSIX) time functions
typeset -ir tm_sec=0		# seconds [0-59]
typeset -ir tm_min=1		# minutes [0-59]
typeset -ir tm_hour=2		# hours [0-23]
typeset -ir tm_mday=3		# day of month [1-31]
typeset -ir tm_mon=4		# month of year - 1 [0-11]
typeset -ir tm_year=5		# year - 1900
typeset -ir tm_wday=6		# day of week [0 = sunday]	input:ignored
typeset -ir tm_yday=7		# day of year [0-365]		input:ignored
typeset -ir tm_isdst=8		# summer time act.? [0/1] (0)	input:ignored
typeset -ir tm_gmtoff=9		# seconds offset from UTC (0)
typeset -ir tm_zone=10		# abbrev. of timezone ("UTC")	input:ignored

set -A mirtime_months -- Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
set -A mirtime_wdays -- Sun Mon Tue Wed Thu Fri Sat
readonly mirtime_months[*] mirtime_wdays[*]

# $ timet2mjd posix_timet
# ⇒ mjd sec
function timet2mjd {
	local -i10 mjd=$1 sec

	(( sec = mjd % 86400 ))
	(( mjd = (mjd / 86400) + 40587 ))
	while (( sec < 0 )); do
		(( --mjd ))
		(( sec += 86400 ))
	done

	print -- $mjd $sec
}

# $ mjd2timet mjd sec
# ⇒ posix_timet
function mjd2timet {
	local -i10 t=$1 sec=$2

	(( t = (t - 40587) * 86400 + sec ))
	print -- $t
}

# $ mjd_explode mjd sec
# ⇒ tm_sec tm_min tm_hour tm_mday tm_mon tm_year \
#   tm_wday tm_yday "0" "0" "UTC"
function mjd_explode {
	local tm
	set -A tm
	local -i10 sec=$2 day yday mon year=$1

	while (( sec < 0 )); do
		(( --year ))
		(( sec += 86400 ))
	done
	while (( sec >= 86400 )); do
		(( ++year ))
		(( sec -= 86400 ))
	done

	(( day = year % 146097 + 678881 ))
	(( year = 4 * ((year / 146097) + (day / 146097)) ))
	(( day %= 146097 ))
	(( tm[tm_wday] = (day + 3) % 7 ))
	if (( day == 146096 )); then
		(( year += 3 ))
		(( day = 36524 ))
	else
		(( year += day / 36524 ))
		(( day %= 36524 ))
	fi
	(( year = 4 * ((year * 25) + (day / 1461)) ))
	(( day %= 1461 ))
	(( yday = (day < 306) ? 1 : 0 ))
	if (( day == 1460 )); then
		(( year += 3 ))
		(( day = 365 ))
	else
		(( year += day / 365 ))
		(( day %= 365 ))
	fi
	(( yday += day ))
	(( day *= 10 ))
	(( mon = (day + 5) / 306 ))
	(( day = ((day + 5) % 306) / 10 ))
	if (( mon >= 10 )); then
		(( mon -= 10 ))
		(( yday -= 306 ))
		(( ++year ))
	else
		(( mon += 2 ))
		(( yday += 59 ))
	fi
	(( tm[tm_sec] = sec % 60 ))
	(( sec /= 60 ))
	(( tm[tm_min] = sec % 60 ))
	(( tm[tm_hour] = sec / 60 ))
	(( tm[tm_mday] = day + 1 ))
	(( tm[tm_mon] = mon ))
	(( tm[tm_year] = (year < 1 ? year - 1 : year) - 1900 ))
	(( tm[tm_yday] = yday ))
	(( tm[tm_isdst] = 0 ))
	(( tm[tm_gmtoff] = 0 ))
	tm[tm_zone]=UTC

	print -r -- "${tm[@]}"
}

# $ mjd_implode tm_sec tm_min tm_hour tm_mday tm_mon tm_year \
#   ignored ignored ignored tm_gmtoff [ignored]
# ⇒ mjd sec
function mjd_implode {
	local tm
	set -A tm -- "$@"
	local -i10 day x y sec

	(( sec = tm[tm_sec] + 60 * tm[tm_min] + 3600 * tm[tm_hour] - \
	    tm[tm_gmtoff] ))
	(( (day = tm[tm_year] + 1900) < 0 )) && (( ++day ))
	(( y = day % 400 ))
	(( day = (day / 400) * 146097 - 678882 + tm[tm_mday] ))
	while (( sec < 0 )); do
		(( --day ))
		(( sec += 86400 ))
	done
	while (( sec >= 86400 )); do
		(( ++day ))
		(( sec -= 86400 ))
	done
	(( x = tm[tm_mon] ))
	while (( x < 0 )); do
		(( --y ))
		(( x += 12 ))
	done
	(( y += x / 12 ))
	(( x %= 12 ))
	if (( x < 2 )); then
		(( x += 10 ))
		(( --y ))
	else
		(( x -= 2 ))
	fi
	(( day += (306 * x + 5) / 10 ))
	while (( y < 0 )); do
		(( day -= 146097 ))
		(( y += 400 ))
	done
	(( day += 146097 * (y / 400) ))
	(( y %= 400 ))
	(( day += 365 * (y % 4) ))
	(( y /= 4 ))
	(( day += 1461 * (y % 25) + 36524 * (y / 25) ))

	print -- $day $sec
}

# end magic from mirtime.c

typeset -i10 -Z4 dY
typeset -i10 -Z2 dM dD

# force hash to use Central European Time (possibly with DST)
# for calculation, and always apply the 30W rule
set -A d -- $(TZ=Europe/Berlin date +'%Y %m %d')
set -A t -- $(mjd_implode 0 0 0 ${d[2]} $((d[1] - 1)) $((d[0] - 1900)))
set -A t -- $(mjd_explode $((t[0] + 1 - 1)) 0)
(( dY = t[tm_year] + 1900 ))
(( dM = t[tm_mon] + 1 ))
(( dD = t[tm_mday] ))

xff="${HTTP_X_FORWARDED_FOR:+$HTTP_X_FORWARDED_FOR, }$REMOTE_ADDR"
set -A fetch -- ftp -H "X-Forwarded-For: $xff" -H "User-Agent: MirKarte/0.2 (Beta; +https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git using MirBSD ftp)" -o -
whence -p wget >/dev/null 2>&1 && \
    set -A fetch -- wget -e robots=off --header "X-Forwarded-For: $xff" -U "MirKarte/0.2 (Beta; +https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git using GNU wget)" -qO- -T3
function gnumd5 {
	md5sum | sed 's/ .*$//'
}
md=gnumd5
whence -p md5 >/dev/null 2>&1 && md=md5

i=$("${fetch[@]}" http://carabiner.peeron.com/xkcd/map/data/$dY/$dM/$dD 2>/dev/null)
if [[ -z $i ]]; then
	cat <<'EOF'
Content-type: text/html; charset=utf-8

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
 "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head>
 <meta http-equiv="content-type" content="text/html; charset=utf-8" />
 <meta name="copyright" content="see mirkarte.js" />
 <title>MirKarte for xkcd Geo Hashing in Central Europe (Beta)</title>
</head><body>
<h1>Error!</h1>
<p>No data yet for tomorrow!</p>
</body></html>
EOF
	exit 0
fi
set -A t -- $(mjd_implode 0 0 0 ${d[2]} $((d[1] - 1)) $((d[0] - 1900)))
set -A t -- $(mjd_explode $((t[0] + 1)) 0)
(( dY = t[tm_year] + 1900 ))
(( dM = t[tm_mon] + 1 ))
(( dD = t[tm_mday] ))
set -A latlon -- $(print -nr -- "$dY-$dM-$dD-$i" | $md | \
    sed -e 'y/abcdef/ABCDEF/' -e 's/.\{16\}/.&p/g' | \
    dc -e 16i -)

cd "$(realpath "$0/..")" || exit 255
print 'Content-type: text/html; charset=utf-8'
print
sed \
    -e '/<title>/s^.*$ <title>MirKarte for xkcd Geo Hashing in Central Europe (Beta)</title>' \
    <tpl/0-prefix.htm
print "  mirkarte_default_loc = [$deflat, $deflon, $defzoom];"
print

cat tpl/2-gh-graticules.js
print
print "  var geohashing_offset = [\"${latlon[0]}\", \"${latlon[1]}\"];"
print "  var geohashing_day = \"$dY-$dM-$dD\";"

cat tpl/5-hookfn.js
cat <<'EOF'
	var el_span = L.DomUtil.create("span", "");
	var el_a = L.DomUtil.create("a", "", el_span);
	el_a.href = "http://wiki.xkcd.com/geohashing/Main_Page";
	el_a.update("Geo Hashing");
	var el_t = document.createTextNode(" on " + geohashing_day);
	el_span.appendChild(el_t);
	var el_br = L.DomUtil.create("br", "");
	map._coorscontrol._unshift(el_br)._unshift(el_span);

	var i = 0;

	while (graticules[i][0] != "666") {
		var ghlat = parseFloat(graticules[i][0] + geohashing_offset[0]);
		var ghlon = parseFloat(graticules[i][1] + geohashing_offset[1]);
		var ghmarker = L.marker([ghlat, ghlon], {
			"draggable": false
		    }).addTo(map);
		var ghwp = geohashing_day + '_' + graticules[i][0] +
		    '_' + graticules[i][1];
		marker_popup(ghmarker,
		    'Geo Hashing Point<br />' + graticules[i][2] +
		    '<br /><a href="http://wiki.xkcd.com/geohashing/' +
		    ghwp + '">Meetup</a> | <a href="gpx.cgi?' + ghwp +
		    '">GPX</a><br />°N<br />°E');
		i++;
	}
	var ghlat = parseFloat(geohashing_offset[0]) * 180 - 90;
	var ghlon = parseFloat(geohashing_offset[1]) * 360 - 180;
	var ghmarker = L.marker([ghlat, ghlon], {
		"icon": marker_icon,
		"draggable": false
	    }).addTo(map);
	var ghwp = geohashing_day + '_global';
	marker_popup(ghmarker,
	    '<a href="http://wiki.xkcd.com/geohashing/Globalhash">Global Geohash</a>' +
	    '<br /><a href="http://wiki.xkcd.com/geohashing/' + ghwp +
	    '">Meetup</a> | <a href="gpx.cgi?' + ghwp +
	    '">GPX</a><br />°N<br />°E');
EOF
cat tpl/9-suffix.htm
exit 0
