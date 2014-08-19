#!/bin/mksh
#-
# Copyright © 2007, 2008, 2012, 2013, 2014
#	Thorsten “mirabilos” Glaser <tg@mirbsd.org>
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

set -A d -- $(TZ=Europe/Berlin date +'%Y %m %d %F')
set -A t -- $(mjd_implode 0 0 0 ${d[2]} $((d[1] - 1)) $((d[0] - 1900)))
set -A t -- $(mjd_explode $((t[0] - 1)) 0)

typeset -i10 -Z4 dY
typeset -i10 -Z2 dM dD

(( dY = t[tm_year] + 1900 ))
(( dM = t[tm_mon] + 1 ))
(( dD = t[tm_mday] ))

i=$(ftp -o - http://carabiner.peeron.com/xkcd/map/data/$dY/$dM/$dD 2>/dev/null)
set -A latlon -- $(print -nr -- "${d[3]}-$i" | md5 | \
    sed -e 'y/abcdef/ABCDEF/' -e 's/.\{16\}/.&p/g' | \
    dc -e 16i -)

cat <<'EOF'
Content-type: text/html; charset=utf-8

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
 "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head>
 <meta http-equiv="content-type" content="text/html; charset=utf-8" />
 <meta name="copyright" content="see mirkarte.js" />
 <title>MirKarte (Beta)</title>
 <link rel="stylesheet" type="text/css" href="leaflet/leaflet.css" />
 <style type="text/css"><!--/*--><![CDATA[/*><!--*/
  #nomap {
	padding:12px;
	margin:12px;
	border:1px solid black;
	width:24em;
  }
  #map {
	height:100%;
	width:100%;
	position:relative;
  }
  #map_coors {
	position:fixed;
	right:0; bottom:16px;
	padding:6px;
	font:12px monospace, sans-serif;
	text-align:right;
	z-index:3;
  }
  #map_coors span {
	background:rgba(255, 255, 255, 0.33);
  }
  #map_wrapper {
	position:absolute;
	top:0; left:0;
	bottom:0; right:0;
  }
  .myzoomcontrol-text {
	font:bold 14px 'Lucida Console', Monaco, monospace;
	text-align:center;
	vertical-align:middle;
  }
  .nowrap {
	white-space:nowrap;
  }
 /*]]>*/--></style>
 <script type="text/javascript" src="leaflet/leaflet-src.js"></script>
 <script type="text/javascript" src="prototype/prototype.js"></script>
 <script type="text/javascript" src="togeojson/togeojson.js"></script>
 <script type="text/javascript" src="zip.js/WebContent/zip.js"></script>
 <script type="text/javascript"><!--//--><![CDATA[//><!--
  zip.workerScriptsPath = "zip.js/WebContent/";
  var geohashing_points = [
EOF

for lat in 49 50 51 52; do
	for lon in -2 -1 -0 1 2 3 4 5 6 7 8 9 10 11 12; do
		print "	[${lat}${latlon[0]}, ${lon}${latlon[1]}],"
	done
done

cat <<'EOF'
	[0, 0] // to please strict syntax, and sentinel
  ];

  function mirkarte_hookfn(map) {
	var i = 0;

	while (geohashing_points[i][0] && geohashing_points[i][1]) {
		var ghmarker = L.marker(geohashing_points[i], {
			"draggable": false
		    }).addTo(map);
		marker_popup(ghmarker,
		    'Geo Hashing Point<br />°N<br />°E');
		i++;
	}
  }

 //--><!]]></script>
 <script type="text/javascript" src="mirkarte.js"></script>
</head><body>
<div id="map_wrapper">
 <div id="map">
  <p id="nomap">
   This is an interactive map application called “MirKarte”.
   Unfortunately, it is implemented completely client-side
   in JavaScript – so, you have to enable that, and use a
   GUI webbrowser supported by Leaflet and Prototype.
  </p>
 </div>
 <div id="map_coors">
  <span id="map_coors_ns"></span><br />
  <span id="map_coors_we"></span>
 </div>
</div>
</body></html>
EOF
exit 0
