#!/bin/mksh
#-
# Copyright © 2007, 2008, 2012, 2013, 2014, 2019
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
# Provide our own GPX, or filter or regenerate those we get from the
# waypoint listing site. Does not support all sites yet…
#
# TODO:
# – CacheBox unknown types “waypoint|virtual stage”, “waypoint|physical stage”

unset LANGUAGE; export LC_ALL=C
unset HTTP_PROXY

mydir=$(realpath "$0/..")
. "$mydir/geo.sh"

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

# escape XHTML characters (three mandatory XML ones plus double quotes,
# the latter in an XML safe fashion numerically though)
function xhtml_fesc {
	REPLY=${1//'&'/'&amp;'}
	REPLY=${REPLY//'<'/'&lt;'}
	REPLY=${REPLY//'>'/'&gt;'}
	REPLY=${REPLY//'"'/'&#34;'}
}

function arbusage {
	print -ru2 "E: arbitrary waypoint $1"
	print -ru2 "I: gpx.sh -WP1234 lat lon owner url title description"
	exit 1
}

typeset -i10 -Z4 dY
typeset -i10 -Z2 dM dD

xff="${HTTP_X_FORWARDED_FOR:+$HTTP_X_FORWARDED_FOR, }$REMOTE_ADDR"
set -A fetch -- ftp -H "X-Forwarded-For: $xff" -H "User-Agent: MirKarte/0.2 (Beta; +https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git using MirBSD ftp)" -o -
whence -p wget >/dev/null 2>&1 && \
    set -A fetch -- wget -e robots=off --header "X-Forwarded-For: $xff" -U "MirKarte/0.2 (Beta; +https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git using GNU wget)" -qO- -T3
function gnumd5 {
	md5sum | sed 's/ .*$//'
}
md=gnumd5
whence -p md5 >/dev/null 2>&1 && md=md5

wp=$1
wptype=
case $wp {
(-*)
	wptype=arbitrary ;;
(OC*)
	wptype=oc ;;
(GD*)
	wptype=gd ;;
(VX*)
	wptype=vx ;;
(2[0-9][0-9][0-9]-@(0[1-9]|1[0-2])-[0-3][0-9]_?(-)+([0-9])_?(-)+([0-9]))
	wptype=geohash ;;
(2[0-9][0-9][0-9]-@(0[1-9]|1[0-2])-[0-3][0-9]_[Gg][Ll][Oo][Bb][Aa][Ll])
	wptype=globalhash ;;
}

[[ -n $wptype ]] || exit 1

# redirections
if [[ $wptype = oc ]]; then
	i=$("${fetch[@]}" "https://www.opencaching.de/search.php?searchbywp=1&showresult=1&output=GPX&f_inactive=0&f_ignored=0&wp=$wp" \
	    2>/dev/null)
	[[ $i = *'<wpt'* ]] || exit 1
	print -r -- "$i"
	exit 0
fi

now=$(date -u +'%Y-%m-%dT%H:%M:%SZ')				# current time

case $wptype {
(arbitrary)
	[[ -n $4 && -n $5 && -n $6 && -n $7 ]] || arbusage 'syntax error'
	wp_src='for an arbitrary waypoint'			# data source
	lat=$(chklatlon lat "$2") || arbusage "$lat"		# position N/S
	lon=$(chklatlon lon "$3") || arbusage "$lon"		# position E/W
	wptime=$now						# date placed
	wpname=${wp#-}						# WP code full
	if (( ${#wpname} > 8 )); then
		typeset -Uui16 -Z11 hex="0x${wpname@#} & 0x7FFFFFFF"
		wpcode=${hex#16#}				# WP code 8byte
	else
		wpcode=$wpname					# WP code 8byte
	fi
	wpdesc=$6						# title text
	wpurlt=$5						# link target
	wpurln=$6						# link text
	wpownr=$4						# owner text
	wp_dif=2						# D rating
	wp_ter=2						# T rating
	wpsdsc="Arbitrary waypoint <tt>${|xhtml_fesc "$wpname";}</tt>"	# short html
	wpldsc=$7						# long html
	wphint=''						# hint text
	;;
(gd)
	wp_src='from geodashing.gpsgames.org data'		# data source
	set -eo pipefail
	"${fetch[@]}" "http://geodashing.gpsgames.org/cgi-bin/dp.pl?dp=$wp" | \
	    sed -n '/^.*maps\.pl.*[&;?]lat=\([0-9.-]*\)&a*m*p*;*lon=\([0-9.-]*\)".*$/s//\1 \2/p' |&
	read -p lat lon						# position
	[[ -n $lat && -n $lon ]]
	set +e
	lattxt=${|decmin2txt ${lat%.*} .${lat#*.} N S 2;}
	lontxt=${|decmin2txt ${lon%.*} .${lon#*.} E W 3;}
	wptime=${now%%+([0-9])T*}01T00:00:00Z			# date placed
	wpname=$wp						# WP code full
	wpcode=${wp//-}						# WP code 8byte
	wpdesc="$wp Dashpoint"					# title text
	wpurlt="http://geodashing.gpsgames.org/cgi-bin/dp.pl?dp=$wp"	# link target
	wpurln="$wp"						# link text
	wpownr="gpsgames.org"					# owner text
	wp_dif=2						# D rating
	wp_ter=2						# T rating
	wpsdsc="Dashpoint ${wpname//_/ }"			# short html
	wpldsc="GeoDashing at $lattxt $lontxt"			# long html
	wphint=''						# hint text
	;;
(vx)
	wp_src='from geovexilla.gpsgames.org data'		# data source
	T=$(mktemp /tmp/gpx.XXXXXXXXXX) || exit 1
	"${fetch[@]}" >"$T" "http://geovexilla.gpsgames.org/cgi-bin/vx.pl?listwaypointlogs=yes&wp=$wp" || { rm -f "$T"; exit 1; }
	sed -n '/^.*maps\.pl.*[&;?]lat=\([0-9.-]*\)&a*m*p*;*lon=\([0-9.-]*\)".*$/s//\1 \2/p' <"$T" |&
	read -p lat lon || lat=					# position
	[[ -n $lat && -n $lon ]] || { rm -f "$T"; exit 1; }
	flag=$(sed -n '/^.*src=".images.flags.*title="\([^"]*\)".*$/s//\1/p' <"$T")
	lattxt=${|decmin2txt ${lat%.*} .${lat#*.} N S 2;}
	lontxt=${|decmin2txt ${lon%.*} .${lon#*.} E W 3;}
	wptime=$(sed -n '/Expires:/s/^.* \(2[0-9][0-9][0-9]-[01][0-9]-[0-3][0-9]\) \([0-2][0-9]:[0-5][0-9]:[0-6][0-9]\) UTC\( .*\)\{0,1\}$/\1T\2Z/p' "$T")
	[[ -n $wptime ]] || wptime=$now				# date placed
	wpname=$wp						# WP code full
	wpcode=${wp//-}						# WP code 8byte
	wpdesc="$wp${flag:+ $flag} flag"			# title text
	wpurlt="http://geovexilla.gpsgames.org/cgi-bin/vx.pl?listwaypointlogs=yes&wp=$wp"	# link target
	wpurln="$wp"						# link text
	wpownr="gpsgames.org"					# owner text
	wp_dif=2						# D rating
	wp_ter=2						# T rating
	wpsdsc="Flag ${wpname//_/ }"				# short html
	wpldsc="GeoVexilla at $lattxt $lontxt$(fgrep \
	    -e Near: -e Expires: -e Flag: "$T" | sed \
	    -e 's!src="/images!src="http://geovexilla.gpsgames.org/images!g' \
	    -e 's!</TD>!!g')"					# long html
	wphint=''						# hint text
	rm -f "$T"
	;;
(geohash)
	# split into day and graticule
	IFS=$' \t\n_'
	set -A w -- $wp
	IFS=$' \t\n-'
	set -A d -- ${w[0]}
	IFS=$' \t\n'
	dY=${d[0]}
	dM=${d[1]}
	dD=${d[2]}
	lat=${w[1]}
	lon=${w[2]}

	# get MJD for that day
	set -A t -- $(mjd_implode 0 0 0 $((dD)) $((dM - 1)) $((dY - 1900)))
	mjd=${t[0]}
	# 30W rule
	(( t[0] -= ((lon > -30 && mjd >= 54613) ? 1 : 0) ))
	# get DJIA day
	set -A t -- $(mjd_explode ${t[0]} 0)
	(( dY = t[tm_year] + 1900 ))
	(( dM = t[tm_mon] + 1 ))
	(( dD = t[tm_mday] ))
	# get DJIA
	i=$("${fetch[@]}" http://carabiner.peeron.com/xkcd/map/data/$dY/$dM/$dD \
	    2>/dev/null)
	[[ -n $i ]] || exit 1
	# get hash day
	set -A t -- $(mjd_explode $mjd 0)
	(( dY = t[tm_year] + 1900 ))
	(( dM = t[tm_mon] + 1 ))
	(( dD = t[tm_mday] ))
	# get that day’s hash
	set -A latlon -- $(print -nr -- "$dY-$dM-$dD-$i" | $md | \
	    sed -e 'y/abcdef/ABCDEF/' -e 's/.\{16\}/.&p/g' | \
	    dc -e 16i -)
	# format the common notation
	lattxt=${|decmin2txt $lat ${latlon[0]} N S 2;}
	lontxt=${|decmin2txt $lon ${latlon[1]} E W 3;}
	# get that graticule’s coordinates
	lat+=${latlon[0]}					# position N/S
	lon+=${latlon[1]}					# position E/W
	# fill out data and metadata
	wp_src='using DJIA from carabiner.peeron.com'		# data source
	wptime=$dY-$dM-${dD}T00:00:00Z				# date placed
	wpname=$dY-$dM-${dD}_${lat%.*}_${lon%.*}		# WP code full
	typeset -Uui16 -Z11 hex="0x${wpname@#} & 0x7FFFFFFF"
	wpcode=${hex#16#}					# WP code 8byte
	wpdesc="${wpname//_/ } GeoHash"				# title text
	wpurlt="https://geohashing.site/geohashing/$wpname"	# link target
	wpurln="Meetup ${wpname//_/ }"				# link text
	wpownr="The Internet"					# owner text
	wp_dif=2						# D rating
	wp_ter=2						# T rating
	wpsdsc="GeoHash ${wpname//_/ }"				# short html
	wpldsc="Regular Geo Hash on $lattxt $lontxt"		# long html
	wphint=''						# hint text
	;;
(globalhash)
	# split into day and graticule
	IFS=$' \t\n_'
	set -A w -- $wp
	IFS=$' \t\n-'
	set -A d -- ${w[0]}
	IFS=$' \t\n'
	dY=${d[0]}
	dM=${d[1]}
	dD=${d[2]}

	# get MJD for that day
	set -A t -- $(mjd_implode 0 0 0 $((dD)) $((dM - 1)) $((dY - 1900)))
	mjd=${t[0]}
	# 30W rule
	(( --t[0] ))
	# get DJIA day
	set -A t -- $(mjd_explode ${t[0]} 0)
	(( dY = t[tm_year] + 1900 ))
	(( dM = t[tm_mon] + 1 ))
	(( dD = t[tm_mday] ))
	# get DJIA
	i=$("${fetch[@]}" http://carabiner.peeron.com/xkcd/map/data/$dY/$dM/$dD \
	    2>/dev/null)
	[[ -n $i ]] || exit 1
	# get hash day
	set -A t -- $(mjd_explode $mjd 0)
	(( dY = t[tm_year] + 1900 ))
	(( dM = t[tm_mon] + 1 ))
	(( dD = t[tm_mday] ))
	# get that day’s hash
	set -A latlon -- $(print -nr -- "$dY-$dM-$dD-$i" | $md | \
	    sed -e 'y/abcdef/ABCDEF/' -e 's/.\{16\}/.&p/g' | \
	    dc -e 16i -)
	x=$(dc -e "${latlon[0]} 180* 90-ps."); lat=${x%.*}; latlon[0]=.${x#*.}
	x=$(dc -e "${latlon[1]} 360* 180-ps."); lon=${x%.*}; latlon[1]=.${x#*.}
	# format the common notation
	lattxt=${|decmin2txt $lat ${latlon[0]} N S 2;}
	lontxt=${|decmin2txt $lon ${latlon[1]} E W 3;}
	# get that graticule’s coordinates
	lat+=${latlon[0]}					# position N/S
	lon+=${latlon[1]}					# position E/W
	# fill out data and metadata
	wp_src='using DJIA from carabiner.peeron.com'		# data source
	wptime=$dY-$dM-${dD}T00:00:00Z				# date placed
	wpname=$dY-$dM-${dD}_global				# WP code full
	typeset -Uui16 -Z11 hex="0x${wpname@#} & 0x7FFFFFFF"
	wpcode=${hex#16#}					# WP code 8byte
	wpdesc="${wpname//_/ } GeoHash"				# title text
	wpurlt="https://geohashing.site/geohashing/$wpname"	# link target
	wpurln="Meetup ${wpname//_/ }"				# link text
	wpownr="The Internet"					# owner text
	wp_dif=2						# D rating
	wp_ter=2						# T rating
	wpsdsc="GeoHash ${wpname//_/ }"				# short html
	wpldsc="Global Geo Hash on $lattxt $lontxt"		# long html
	wphint=''						# hint text
	;;
(*)
	exit 1
	;;
}

typeset -u wpcode

sed $'s/$/\r/' <<EOF
<?xml version="1.0" encoding="utf-8"?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" version="1.0" creator="MirKarte by mirabilos - https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd http://www.groundspeak.com/cache/1/0/1 http://www.groundspeak.com/cache/1/0/1/cache.xsd" xmlns="http://www.topografix.com/GPX/1/0">
  <name>Waypoint Listing Generated by MirKarte</name>
  <desc>This is an individual waypoint generated ${|xhtml_fesc "$wp_src";} by MirKarte</desc>
  <author>mirabilos</author>
  <email>miros-discuss@mirbsd.org</email>
  <url>https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git</url>
  <urlname>MirKarte (beta)</urlname>
  <time>${|xhtml_fesc "$now";}</time>
  <keywords>cache, geocache, dashpoint, geovexilla, xkcd, geohashing, waypoint, shutterspot, terracaching, opencaching</keywords>
  <bounds minlat="${|xhtml_fesc "$lat";}" minlon="${|xhtml_fesc "$lon";}" maxlat="${|xhtml_fesc "$lat";}" maxlon="${|xhtml_fesc "$lon";}" />
  <wpt lat="${|xhtml_fesc "$lat";}" lon="${|xhtml_fesc "$lon";}">
    <time>${|xhtml_fesc "$wptime";}</time>
    <name>${|xhtml_fesc "$wpcode";}</name>
    <desc>${|xhtml_fesc "$wpdesc";}</desc>
    <url>${|xhtml_fesc "$wpurlt";}</url>
    <urlname>${|xhtml_fesc "$wpurln";}</urlname>
    <sym>Geocache</sym>
    <type>Geocache|Virtual Cache</type>
    <groundspeak:cache id="notfromgs_${wpname@#}" available="False" archived="False" xmlns:groundspeak="http://www.groundspeak.com/cache/1/0/1">
      <groundspeak:name>${|xhtml_fesc "$wpname";}</groundspeak:name>
      <groundspeak:placed_by>${|xhtml_fesc "$wpownr";}</groundspeak:placed_by>
      <groundspeak:owner id="notfromgspr">${|xhtml_fesc "$wpownr";}</groundspeak:owner>
      <groundspeak:type>Virtual Cache</groundspeak:type>
      <groundspeak:container>Virtual</groundspeak:container>
      <groundspeak:attributes>
        <groundspeak:attribute id="67" inc="1">GeoTour</groundspeak:attribute>
      </groundspeak:attributes>
      <groundspeak:difficulty>${|xhtml_fesc "$wp_dif";}</groundspeak:difficulty>
      <groundspeak:terrain>${|xhtml_fesc "$wp_ter";}</groundspeak:terrain>
      <groundspeak:country>Terra</groundspeak:country>
      <groundspeak:state>unknown</groundspeak:state>
      <groundspeak:short_description html="True">${|xhtml_fesc "$wpsdsc";}</groundspeak:short_description>
      <groundspeak:long_description html="True">${|xhtml_fesc "$wpldsc";}</groundspeak:long_description>
      <groundspeak:encoded_hints>${|xhtml_fesc "$wphint";}</groundspeak:encoded_hints>
      <groundspeak:logs>
      </groundspeak:logs>
      <groundspeak:travelbugs />
    </groundspeak:cache>
  </wpt>
</gpx>
EOF
exit 0
