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
set -A t -- $(mjd_explode $((t[0] - 1)) 0)
(( dY = t[tm_year] + 1900 ))
(( dM = t[tm_mon] + 1 ))
(( dD = t[tm_mday] ))

xff="${HTTP_X_FORWARDED_FOR:+$HTTP_X_FORWARDED_FOR, }$REMOTE_ADDR"
set -A fetch -- ftp -H "X-Forwarded-For: $xff" -H "User-Agent: MirKarte/0.2 (Beta; +https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git using MirBSD ftp)" -o -
whence -p wget >/dev/null 2>&1 && \
    set -A fetch -- wget --header "X-Forwarded-For: $xff" -U "MirKarte/0.2 (Beta; +https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git using GNU wget)" -qO- -T3
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
<p>No data yet for today!</p>
</body></html>
EOF
	exit 0
fi
set -A t -- $(mjd_implode 0 0 0 ${d[2]} $((d[1] - 1)) $((d[0] - 1900)))
set -A t -- $(mjd_explode $((t[0])) 0)
(( dY = t[tm_year] + 1900 ))
(( dM = t[tm_mon] + 1 ))
(( dD = t[tm_mday] ))
set -A latlon -- $(print -nr -- "$dY-$dM-$dD-$i" | $md | \
    sed -e 'y/abcdef/ABCDEF/' -e 's/.\{16\}/.&p/g' | \
    dc -e 16i -)

cat <<'EOF'
Content-type: text/html; charset=utf-8

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
 "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head>
 <meta http-equiv="content-type" content="text/html; charset=utf-8" />
 <meta name="copyright" content="see mirkarte.js" />
 <title>MirKarte for xkcd Geo Hashing in Central Europe (Beta)</title>
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
  mirkarte_default_loc = [50.7, 7.11, 8];
  var graticules = [
	/* BEGIN generated file from xkcd2js.sh */
	["42", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Ponferrada,_Spain\">Ponferrada, Spain</a>"],
	["42", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Le%C3%B3n,_Spain\">León, Spain</a>"],
	["42", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Palencia,_Spain\">Palencia, Spain</a>"],
	["42", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Burgos,_Spain\">Burgos, Spain</a>"],
	["42", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Vitoria-Gasteiz,_Spain\">Vitoria-Gasteiz, Spain</a>"],
	["42", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Pamplona,_Spain\">Pamplona, Spain</a>"],
	["42", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Huesca,_Spain\">Huesca, Spain</a>"],
	["42", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Barbastro,_Spain\">Barbastro, Spain</a>"],
	["42", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Andorra\">Andorra</a>"],
	["42", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Perpignan,_France\">Perpignan, France</a>"],
	["42", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Roses,_Spain\">Roses, Spain</a>"],
	["42", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Mediterranean_Sea_42,_4\">Mediterranean Sea 42, 4</a>"],
	["42", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Mediterranean_Sea_42,_5\">Mediterranean Sea 42, 5</a>"],
	["42", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Porquerolles,_France\">Porquerolles, France</a>"],
	["42", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Mediterranean_Sea_42,_7\">Mediterranean Sea 42, 7</a>"],
	["42", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Calvi,_France\">Calvi, France</a>"],
	["42", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Bastia,_France\">Bastia, France</a>"],
	["42", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Piombino,_Italy\">Piombino, Italy</a>"],
	["42", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Grosseto,_Italy\">Grosseto, Italy</a>"],
	["42", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Terni,_Italy\">Terni, Italy</a>"],
	["43", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Vald%C3%A9s,_Spain\">Valdés, Spain</a>"],
	["43", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Gij%C3%B3n,_Spain\">Gijón, Spain</a>"],
	["43", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Torrelavega,_Spain\">Torrelavega, Spain</a>"],
	["43", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Santander,_Spain\">Santander, Spain</a>"],
	["43", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Bilbao,_Spain\">Bilbao, Spain</a>"],
	["43", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Bayonne,_France\">Bayonne, France</a>"],
	["43", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Pau,_France\">Pau, France</a>"],
	["43", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Tarbes,_France\">Tarbes, France</a>"],
	["43", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Toulouse,_France\">Toulouse, France</a>"],
	["43", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Carcassonne,_France\">Carcassonne, France</a>"],
	["43", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Montpellier,_France\">Montpellier, France</a>"],
	["43", "4", "<a href=\"http://wiki.xkcd.com/geohashing/N%C3%AEmes,_France\">Nîmes, France</a>"],
	["43", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Marseille,_France\">Marseille, France</a>"],
	["43", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Draguignan,_France\">Draguignan, France</a>"],
	["43", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Nice,_France\">Nice, France</a>"],
	["43", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Imperia,_Italy\">Imperia, Italy</a>"],
	["43", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Capraia,_Italy\">Capraia, Italy</a>"],
	["43", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Livorno,_Italy\">Livorno, Italy</a>"],
	["43", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Firenze,_Italy\">Firenze, Italy</a>"],
	["43", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Perugia,_Italy\">Perugia, Italy</a>"],
	["44", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_44,_-6\">Bay of Biscay 44, -6</a>"],
	["44", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_44,_-5\">Bay of Biscay 44, -5</a>"],
	["44", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_44,_-4\">Bay of Biscay 44, -4</a>"],
	["44", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_44,_-3\">Bay of Biscay 44, -3</a>"],
	["44", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_44,_-2\">Bay of Biscay 44, -2</a>"],
	["44", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Arcachon,_France\">Arcachon, France</a>"],
	["44", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Bordeaux,_France\">Bordeaux, France</a>"],
	["44", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Bergerac,_France\">Bergerac, France</a>"],
	["44", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Montauban,_France\">Montauban, France</a>"],
	["44", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Aurillac,_France\">Aurillac, France</a>"],
	["44", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Millau,_France\">Millau, France</a>"],
	["44", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Valence,_France\">Valence, France</a>"],
	["44", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Carpentras,_France\">Carpentras, France</a>"],
	["44", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Gap,_France\">Gap, France</a>"],
	["44", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Cuneo,_Italy\">Cuneo, Italy</a>"],
	["44", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Genova,_Italy\">Genova, Italy</a>"],
	["44", "9", "<a href=\"http://wiki.xkcd.com/geohashing/La_Spezia,_Italy\">La Spezia, Italy</a>"],
	["44", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Parma,_Italy\">Parma, Italy</a>"],
	["44", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Bologna,_Italy\">Bologna, Italy</a>"],
	["44", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Ravenna,_Italy\">Ravenna, Italy</a>"],
	["45", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Atlantic_Ocean_45,_-6\">Atlantic Ocean 45, -6</a>"],
	["45", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_45,_-5\">Bay of Biscay 45, -5</a>"],
	["45", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_45,_-4\">Bay of Biscay 45, -4</a>"],
	["45", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_45,_-3\">Bay of Biscay 45, -3</a>"],
	["45", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_45,_-2\">Bay of Biscay 45, -2</a>"],
	["45", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Royan,_France\">Royan, France</a>"],
	["45", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Saintes,_France\">Saintes, France</a>"],
	["45", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Angoul%C3%AAme,_France\">Angoulême, France</a>"],
	["45", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Limoges,_France\">Limoges, France</a>"],
	["45", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Ussel,_France\">Ussel, France</a>"],
	["45", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Clermont-Ferrand,_France\">Clermont-Ferrand, France</a>"],
	["45", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Lyon,_France\">Lyon, France</a>"],
	["45", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Grenoble,_France\">Grenoble, France</a>"],
	["45", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Annecy,_France\">Annecy, France</a>"],
	["45", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Torino,_Italy\">Torino, Italy</a>"],
	["45", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Novara,_Italy\">Novara, Italy</a>"],
	["45", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Milano,_Italy\">Milano, Italy</a>"],
	["45", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Verona,_Italy\">Verona, Italy</a>"],
	["45", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Padova,_Italy\">Padova, Italy</a>"],
	["45", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Venezia,_Italy\">Venezia, Italy</a>"],
	["46", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Atlantic_Ocean_46,_-6\">Atlantic Ocean 46, -6</a>"],
	["46", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_46,_-5\">Bay of Biscay 46, -5</a>"],
	["46", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_46,_-4\">Bay of Biscay 46, -4</a>"],
	["46", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Bay_of_Biscay_46,_-3\">Bay of Biscay 46, -3</a>"],
	["46", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/L%27%C3%8Ele-d%27Yeu,_France\">L'Île-d'Yeu, France</a>"],
	["46", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/La_Roche-sur-Yon,_France\">La Roche-sur-Yon, France</a>"],
	["46", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Niort,_France\">Niort, France</a>"],
	["46", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Poitiers,_France\">Poitiers, France</a>"],
	["46", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Ch%C3%A2teauroux,_France\">Châteauroux, France</a>"],
	["46", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Montlu%C3%A7on,_France\">Montluçon, France</a>"],
	["46", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Nevers,_France\">Nevers, France</a>"],
	["46", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Chalon-sur-Sa%C3%B4ne,_France\">Chalon-sur-Saône, France</a>"],
	["46", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Bourg-en-Bresse,_France\">Bourg-en-Bresse, France</a>"],
	["46", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Gen%C3%A8ve,_Switzerland\">Genève, Switzerland</a>"],
	["46", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Bern,_Switzerland\">Bern, Switzerland</a>"],
	["46", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Lugano,_Switzerland\">Lugano, Switzerland</a>"],
	["46", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Chur,_Switzerland\">Chur, Switzerland</a>"],
	["46", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Livigno,_Italy\">Livigno, Italy</a>"],
	["46", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Trento,_Italy\">Trento, Italy</a>"],
	["46", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Belluno,_Italy\">Belluno, Italy</a>"],
	["47", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Atlantic_Ocean_47,_-6\">Atlantic Ocean 47, -6</a>"],
	["47", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Atlantic_Ocean_47,_-5\">Atlantic Ocean 47, -5</a>"],
	["47", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Quimper,_France\">Quimper, France</a>"],
	["47", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Lorient,_France\">Lorient, France</a>"],
	["47", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Vannes,_France\">Vannes, France</a>"],
	["47", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Nantes,_France\">Nantes, France</a>"],
	["47", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Angers,_France\">Angers, France</a>"],
	["47", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Tours,_France\">Tours, France</a>"],
	["47", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Orl%C3%A9ans,_France\">Orléans, France</a>"],
	["47", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Bourges,_France\">Bourges, France</a>"],
	["47", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Auxerre,_France\">Auxerre, France</a>"],
	["47", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Beaune,_France\">Beaune, France</a>"],
	["47", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Dijon,_France\">Dijon, France</a>"],
	["47", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Besan%C3%A7on,_France\">Besançon, France</a>"],
	["47", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Basel,_Switzerland\">Basel, Switzerland</a>"],
	["47", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Z%C3%BCrich,_Switzerland\">Zürich, Switzerland</a>"],
	["47", "9", "<a href=\"http://wiki.xkcd.com/geohashing/St._Gallen,_Switzerland\">St. Gallen, Switzerland</a>"],
	["47", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Kempten,_Germany\">Kempten, Germany</a>"],
	["47", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Innsbruck,_Austria\">Innsbruck, Austria</a>"],
	["47", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Rosenheim,_Germany\">Rosenheim, Germany</a>"],
	["48", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Atlantic_Ocean_48,_-6\">Atlantic Ocean 48, -6</a>"],
	["48", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Ouessant,_France\">Ouessant, France</a>"],
	["48", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Brest,_France\">Brest, France</a>"],
	["48", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Lannion,_France\">Lannion, France</a>"],
	["48", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Saint-Brieuc,_France\">Saint-Brieuc, France</a>"],
	["48", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Rennes,_France\">Rennes, France</a>"],
	["48", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Laval,_France\">Laval, France</a>"],
	["48", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Le_Mans,_France\">Le Mans, France</a>"],
	["48", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Chartres,_France\">Chartres, France</a>"],
	["48", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Paris,_France\">Paris, France</a>"],
	["48", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Sens,_France\">Sens, France</a>"],
	["48", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Troyes,_France\">Troyes, France</a>"],
	["48", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Chaumont,_France\">Chaumont, France</a>"],
	["48", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Nancy,_France\">Nancy, France</a>"],
	["48", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Strasbourg,_France\">Strasbourg, France</a>"],
	["48", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Pforzheim,_Germany\">Pforzheim, Germany</a>"],
	["48", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Stuttgart,_Germany\">Stuttgart, Germany</a>"],
	["48", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Augsburg,_Germany\">Augsburg, Germany</a>"],
	["48", "11", "<a href=\"http://wiki.xkcd.com/geohashing/M%C3%BCnchen,_Germany\">München, Germany</a>"],
	["48", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Landshut,_Germany\">Landshut, Germany</a>"],
	["49", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Isles_of_Scilly,_United_Kingdom\">Isles of Scilly, United Kingdom</a>"],
	["49", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Lizard_Point,_United_Kingdom\">Lizard Point, United Kingdom</a>"],
	["49", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/English_Channel_49,_-4\">English Channel 49, -4</a>"],
	["49", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/English_Channel_49,_-3\">English Channel 49, -3</a>"],
	["49", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Channel_Islands\">Channel Islands</a>"],
	["49", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Cherbourg,_France\">Cherbourg, France</a>"],
	["49", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Caen,_France\">Caen, France</a>"],
	["49", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Le_Havre,_France\">Le Havre, France</a>"],
	["49", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Rouen,_France\">Rouen, France</a>"],
	["49", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Amiens,_France\">Amiens, France</a>"],
	["49", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Saint-Quentin,_France\">Saint-Quentin, France</a>"],
	["49", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Reims,_France\">Reims, France</a>"],
	["49", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Verdun,_France\">Verdun, France</a>"],
	["49", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Luxembourg,_Luxembourg\">Luxembourg, Luxembourg</a>"],
	["49", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Kaiserslautern,_Germany\">Kaiserslautern, Germany</a>"],
	["49", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Mannheim,_Germany\">Mannheim, Germany</a>"],
	["49", "9", "<a href=\"http://wiki.xkcd.com/geohashing/W%C3%BCrzburg,_Germany\">Würzburg, Germany</a>"],
	["49", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Bamberg,_Germany\">Bamberg, Germany</a>"],
	["49", "11", "<a href=\"http://wiki.xkcd.com/geohashing/N%C3%BCrnberg,_Germany\">Nürnberg, Germany</a>"],
	["49", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Regensburg,_Germany\">Regensburg, Germany</a>"],
	["50", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Atlantic_Ocean_50,_-6\">Atlantic Ocean 50, -6</a>"],
	["50", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Camborne,_United_Kingdom\">Camborne, United Kingdom</a>"],
	["50", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Plymouth,_United_Kingdom\">Plymouth, United Kingdom</a>"],
	["50", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Exeter,_United_Kingdom\">Exeter, United Kingdom</a>"],
	["50", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Weymouth,_United_Kingdom\">Weymouth, United Kingdom</a>"],
	["50", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Southampton,_United_Kingdom\">Southampton, United Kingdom</a>"],
	["50", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Brighton,_United_Kingdom\">Brighton, United Kingdom</a>"],
	["50", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Eastbourne,_United_Kingdom\">Eastbourne, United Kingdom</a>"],
	["50", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Calais,_France\">Calais, France</a>"],
	["50", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Arras,_France\">Arras, France</a>"],
	["50", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Lille,_France\">Lille, France</a>"],
	["50", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Bruxelles,_Belgium\">Bruxelles, Belgium</a>"],
	["50", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Li%C3%A8ge,_Belgium\">Liège, Belgium</a>"],
	["50", "6", "<a href=\"http://wiki.xkcd.com/geohashing/K%C3%B6ln,_Germany\">Köln, Germany</a>"],
	["50", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Bonn,_Germany\">Bonn, Germany</a>"],
	["50", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Frankfurt_am_Main,_Germany\">Frankfurt am Main, Germany</a>"],
	["50", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Fulda,_Germany\">Fulda, Germany</a>"],
	["50", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Schweinfurt,_Germany\">Schweinfurt, Germany</a>"],
	["50", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Erfurt,_Germany\">Erfurt, Germany</a>"],
	["50", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Chemnitz,_Germany\">Chemnitz, Germany</a>"],
	["51", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Atlantic_Ocean_51,_-6\">Atlantic Ocean 51, -6</a>"],
	["51", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Milford_Haven,_United_Kingdom\">Milford Haven, United Kingdom</a>"],
	["51", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Barnstaple,_United_Kingdom\">Barnstaple, United Kingdom</a>"],
	["51", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Cardiff,_United_Kingdom\">Cardiff, United Kingdom</a>"],
	["51", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Bristol,_United_Kingdom\">Bristol, United Kingdom</a>"],
	["51", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Swindon,_United_Kingdom\">Swindon, United Kingdom</a>"],
	["51", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/London_West,_United_Kingdom\">London West, United Kingdom</a>"],
	["51", "0", "<a href=\"http://wiki.xkcd.com/geohashing/London_East,_United_Kingdom\">London East, United Kingdom</a>"],
	["51", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Canterbury,_United_Kingdom\">Canterbury, United Kingdom</a>"],
	["51", "2", "<a href=\"http://wiki.xkcd.com/geohashing/Dunkerque,_France\">Dunkerque, France</a>"],
	["51", "3", "<a href=\"http://wiki.xkcd.com/geohashing/Gent,_Belgium\">Gent, Belgium</a>"],
	["51", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Rotterdam,_Netherlands\">Rotterdam, Netherlands</a>"],
	["51", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Eindhoven,_Netherlands\">Eindhoven, Netherlands</a>"],
	["51", "6", "<a href=\"http://wiki.xkcd.com/geohashing/D%C3%BCsseldorf,_Germany\">Düsseldorf, Germany</a>"],
	["51", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Dortmund,_Germany\">Dortmund, Germany</a>"],
	["51", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Paderborn,_Germany\">Paderborn, Germany</a>"],
	["51", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Kassel,_Germany\">Kassel, Germany</a>"],
	["51", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Nordhausen,_Germany\">Nordhausen, Germany</a>"],
	["51", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Halle_(Saale),_Germany\">Halle (Saale), Germany</a>"],
	["51", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Leipzig,_Germany\">Leipzig, Germany</a>"],
	["52", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Carlow,_Ireland\">Carlow, Ireland</a>"],
	["52", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Fishguard,_United_Kingdom\">Fishguard, United Kingdom</a>"],
	["52", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Aberystwyth,_United_Kingdom\">Aberystwyth, United Kingdom</a>"],
	["52", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Mid_Wales,_United_Kingdom\">Mid Wales, United Kingdom</a>"],
	["52", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Shrewsbury,_United_Kingdom\">Shrewsbury, United Kingdom</a>"],
	["52", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Birmingham,_United_Kingdom\">Birmingham, United Kingdom</a>"],
	["52", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Northampton,_United_Kingdom\">Northampton, United Kingdom</a>"],
	["52", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Cambridge,_United_Kingdom\">Cambridge, United Kingdom</a>"],
	["52", "1", "<a href=\"http://wiki.xkcd.com/geohashing/Norwich,_United_Kingdom\">Norwich, United Kingdom</a>"],
	["52", "2", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_52,_2\">North Sea 52, 2</a>"],
	["52", "3", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_52,_3\">North Sea 52, 3</a>"],
	["52", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Amsterdam,_Netherlands\">Amsterdam, Netherlands</a>"],
	["52", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Utrecht,_Netherlands\">Utrecht, Netherlands</a>"],
	["52", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Enschede,_Netherlands\">Enschede, Netherlands</a>"],
	["52", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Rheine,_Germany\">Rheine, Germany</a>"],
	["52", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Bielefeld,_Germany\">Bielefeld, Germany</a>"],
	["52", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Hannover,_Germany\">Hannover, Germany</a>"],
	["52", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Braunschweig,_Germany\">Braunschweig, Germany</a>"],
	["52", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Magdeburg,_Germany\">Magdeburg, Germany</a>"],
	["52", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Brandenburg,_Germany\">Brandenburg, Germany</a>"],
	["53", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Dublin,_Ireland\">Dublin, Ireland</a>"],
	["53", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Irish_Sea_53,_-5\">Irish Sea 53, -5</a>"],
	["53", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Anglesey,_United_Kingdom\">Anglesey, United Kingdom</a>"],
	["53", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Blackpool,_United_Kingdom\">Blackpool, United Kingdom</a>"],
	["53", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Manchester,_United_Kingdom\">Manchester, United Kingdom</a>"],
	["53", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Sheffield,_United_Kingdom\">Sheffield, United Kingdom</a>"],
	["53", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Hull,_United_Kingdom\">Hull, United Kingdom</a>"],
	["53", "0", "<a href=\"http://wiki.xkcd.com/geohashing/Skegness,_United_Kingdom\">Skegness, United Kingdom</a>"],
	["53", "1", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_53,_1\">North Sea 53, 1</a>"],
	["53", "2", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_53,_2\">North Sea 53, 2</a>"],
	["53", "3", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_53,_3\">North Sea 53, 3</a>"],
	["53", "4", "<a href=\"http://wiki.xkcd.com/geohashing/Texel,_Netherlands\">Texel, Netherlands</a>"],
	["53", "5", "<a href=\"http://wiki.xkcd.com/geohashing/Leeuwarden,_Netherlands\">Leeuwarden, Netherlands</a>"],
	["53", "6", "<a href=\"http://wiki.xkcd.com/geohashing/Groningen,_Netherlands\">Groningen, Netherlands</a>"],
	["53", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Emden,_Germany\">Emden, Germany</a>"],
	["53", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Bremen,_Germany\">Bremen, Germany</a>"],
	["53", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Hamburg_(West),_Germany\">Hamburg (West), Germany</a>"],
	["53", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Hamburg_(East),_Germany\">Hamburg (East), Germany</a>"],
	["53", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Schwerin,_Germany\">Schwerin, Germany</a>"],
	["53", "12", "<a href=\"http://wiki.xkcd.com/geohashing/G%C3%BCstrow,_Germany\">Güstrow, Germany</a>"],
	["54", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Lisburn,_United_Kingdom\">Lisburn, United Kingdom</a>"],
	["54", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Belfast,_United_Kingdom\">Belfast, United Kingdom</a>"],
	["54", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Isle_of_Man\">Isle of Man</a>"],
	["54", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Barrow-in-Furness,_United_Kingdom\">Barrow-in-Furness, United Kingdom</a>"],
	["54", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Carlisle,_United_Kingdom\">Carlisle, United Kingdom</a>"],
	["54", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Middlesbrough,_United_Kingdom\">Middlesbrough, United Kingdom</a>"],
	["54", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/Scarborough,_United_Kingdom\">Scarborough, United Kingdom</a>"],
	["54", "0", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_54,_0\">North Sea 54, 0</a>"],
	["54", "1", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_54,_1\">North Sea 54, 1</a>"],
	["54", "2", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_54,_2\">North Sea 54, 2</a>"],
	["54", "3", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_54,_3\">North Sea 54, 3</a>"],
	["54", "4", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_54,_4\">North Sea 54, 4</a>"],
	["54", "5", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_54,_5\">North Sea 54, 5</a>"],
	["54", "6", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_54,_6\">North Sea 54, 6</a>"],
	["54", "7", "<a href=\"http://wiki.xkcd.com/geohashing/Helgoland,_Germany\">Helgoland, Germany</a>"],
	["54", "8", "<a href=\"http://wiki.xkcd.com/geohashing/T%C3%B8nder,_Denmark\">Tønder, Denmark</a>"],
	["54", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Flensburg,_Germany\">Flensburg, Germany</a>"],
	["54", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Kiel,_Germany\">Kiel, Germany</a>"],
	["54", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Nyk%C3%B8bing_Falster,_Denmark\">Nykøbing Falster, Denmark</a>"],
	["54", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Rostock,_Germany\">Rostock, Germany</a>"],
	["55", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Coleraine,_United_Kingdom\">Coleraine, United Kingdom</a>"],
	["55", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Campbeltown,_United_Kingdom\">Campbeltown, United Kingdom</a>"],
	["55", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Glasgow,_United_Kingdom\">Glasgow, United Kingdom</a>"],
	["55", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Edinburgh,_United_Kingdom\">Edinburgh, United Kingdom</a>"],
	["55", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Jedburgh,_United_Kingdom\">Jedburgh, United Kingdom</a>"],
	["55", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/Blyth,_United_Kingdom\">Blyth, United Kingdom</a>"],
	["55", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_-0\">North Sea 55, -0</a>"],
	["55", "0", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_0\">North Sea 55, 0</a>"],
	["55", "1", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_1\">North Sea 55, 1</a>"],
	["55", "2", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_2\">North Sea 55, 2</a>"],
	["55", "3", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_3\">North Sea 55, 3</a>"],
	["55", "4", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_4\">North Sea 55, 4</a>"],
	["55", "5", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_5\">North Sea 55, 5</a>"],
	["55", "6", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_6\">North Sea 55, 6</a>"],
	["55", "7", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_55,_7\">North Sea 55, 7</a>"],
	["55", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Esbjerg,_Denmark\">Esbjerg, Denmark</a>"],
	["55", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Kolding,_Denmark\">Kolding, Denmark</a>"],
	["55", "10", "<a href=\"http://wiki.xkcd.com/geohashing/Odense,_Denmark\">Odense, Denmark</a>"],
	["55", "11", "<a href=\"http://wiki.xkcd.com/geohashing/N%C3%A6stved,_Denmark\">Næstved, Denmark</a>"],
	["55", "12", "<a href=\"http://wiki.xkcd.com/geohashing/K%C3%B8benhavn,_Denmark\">København, Denmark</a>"],
	["56", "-6", "<a href=\"http://wiki.xkcd.com/geohashing/Tobermory,_United_Kingdom\">Tobermory, United Kingdom</a>"],
	["56", "-5", "<a href=\"http://wiki.xkcd.com/geohashing/Oban,_United_Kingdom\">Oban, United Kingdom</a>"],
	["56", "-4", "<a href=\"http://wiki.xkcd.com/geohashing/Helensburgh,_United_Kingdom\">Helensburgh, United Kingdom</a>"],
	["56", "-3", "<a href=\"http://wiki.xkcd.com/geohashing/Perth,_United_Kingdom\">Perth, United Kingdom</a>"],
	["56", "-2", "<a href=\"http://wiki.xkcd.com/geohashing/Dundee,_United_Kingdom\">Dundee, United Kingdom</a>"],
	["56", "-1", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_-1\">North Sea 56, -1</a>"],
	["56", "-0", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_-0\">North Sea 56, -0</a>"],
	["56", "0", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_0\">North Sea 56, 0</a>"],
	["56", "1", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_1\">North Sea 56, 1</a>"],
	["56", "2", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_2\">North Sea 56, 2</a>"],
	["56", "3", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_3\">North Sea 56, 3</a>"],
	["56", "4", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_4\">North Sea 56, 4</a>"],
	["56", "5", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_5\">North Sea 56, 5</a>"],
	["56", "6", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_6\">North Sea 56, 6</a>"],
	["56", "7", "<a href=\"http://wiki.xkcd.com/geohashing/North_Sea_56,_7\">North Sea 56, 7</a>"],
	["56", "8", "<a href=\"http://wiki.xkcd.com/geohashing/Herning,_Denmark\">Herning, Denmark</a>"],
	["56", "9", "<a href=\"http://wiki.xkcd.com/geohashing/Silkeborg,_Denmark\">Silkeborg, Denmark</a>"],
	["56", "10", "<a href=\"http://wiki.xkcd.com/geohashing/%C3%85rhus,_Denmark\">Århus, Denmark</a>"],
	["56", "11", "<a href=\"http://wiki.xkcd.com/geohashing/Anholt,_Denmark\">Anholt, Denmark</a>"],
	["56", "12", "<a href=\"http://wiki.xkcd.com/geohashing/Helsingborg,_Sweden\">Helsingborg, Sweden</a>"],
	["666", "666", ""]
	/* END generated file from xkcd2js.sh */
  ];
EOF
print "  var geohashing_offset = [\"${latlon[0]}\", \"${latlon[1]}\"];"
print "  var geohashing_day = \"$dY-$dM-$dD\";"
cat <<'EOF'

  function mirkarte_hookfn(map) {
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
EOF
echo "  <span><a href=\"http://wiki.xkcd.com/geohashing/Main_Page\">Geo Hashing</a> on $dY-$dM-$dD</span><br />"
cat <<'EOF'
  <span id="map_coors_ns"></span><br />
  <span id="map_coors_we"></span>
 </div>
</div>
</body></html>
EOF
exit 0
