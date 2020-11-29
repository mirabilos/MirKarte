#!/bin/mksh
#-
# Copyright © 2014, 2017, 2020
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

#XXX add attribution (either to #map_coors or by moving CGI content
#XXX into a layer; maybe even make an AJAX version of the CGIs that
#XXX merge all the CGIs into layers)

#XXX make these CGI parameters
deflat=50.7
deflon=7.11
defzoom=9
set -A defyear -- $(date +'%y %m')
defmon=${defyear[1]}

xff="${HTTP_X_FORWARDED_FOR:+$HTTP_X_FORWARDED_FOR, }$REMOTE_ADDR"
set -A fetch -- ftp -H "X-Forwarded-For: $xff" -H "User-Agent: MirKarte/0.2 (Beta; +https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git using MirBSD ftp)" -o -
whence -p wget >/dev/null 2>&1 && \
    set -A fetch -- wget -e robots=off --header "X-Forwarded-For: $xff" -U "MirKarte/0.2 (Beta; +https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git using GNU wget)" -qO- -T3

# for xmlstarlet on MirPorts
PATH=$PATH:/usr/mpkg/bin

set -A mirtime_months -- Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
set -A mirtime_wdays -- Sun Mon Tue Wed Thu Fri Sat
readonly mirtime_months[*] mirtime_wdays[*]

cat <<'EOF'
Content-type: text/html; charset=utf-8

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
 "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head>
 <meta http-equiv="content-type" content="text/html; charset=utf-8" />
 <meta name="copyright" content="see mirkarte.js" />
 <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
 <title>MirKarte for GeoDashing (Beta)</title>
 <link rel="stylesheet" type="text/css" href="leaflet/leaflet.css" />
 <link rel="stylesheet" type="text/css" href="leaflet-compass/leaflet-compass.css" />
 <link rel="stylesheet" type="text/css" href="leaflet-gps/leaflet-gps.css" />
 <style type="text/css"><!--/*--><![CDATA[/*><!--*/
  html, body {
	position:fixed;
	overflow:hidden;
	width:100%;
	height:100%;
	margin:0px;
  }
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
	-webkit-overflow-scrolling:touch;
  }
  .leaflet-top.leaflet-right {
	max-width:90%;
	bottom:54px;
  }
  .leaflet-control-layers-expanded {
	max-height:100%;
	overflow-y:scroll;
  }
  .leaflet-control-layers-list, .leaflet-control-layers-base {
	max-height:100%;
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
 <script type="text/javascript" src="leaflet-compass/leaflet-compass.js"></script>
 <script type="text/javascript" src="leaflet-gps/leaflet-gps.js"></script>
 <script type="text/javascript" src="prototype/prototype.js"></script>
 <script type="text/javascript" src="togeojson/togeojson.js"></script>
 <script type="text/javascript" src="zip.js/WebContent/zip.js"></script>
 <script type="text/javascript"><!--//--><![CDATA[//><!--
  zip.workerScriptsPath = "zip.js/WebContent/";
EOF
print "  mirkarte_default_loc = [$deflat, $deflon, $defzoom];"

"${fetch[@]}" "http://geodashing.gpsgames.org/cgi-bin/stats.pl?startmonth=$defmon&startyear=$defyear&endmonth=$defmon&endyear=$defyear&radius=200&lat_1=$deflat&lon_1=$deflon&statstype=circle&download=Download&downloadformat=GPX" | \
    sed '1s/ xmlns="[^"]*"//' | \
    xmlstarlet sel -t -m //*/wpt -v name -o ' ' -v @lat -o ' ' -v @lon -n |&
n=0; print "  var geodashing_arr = ["
while read -pr id lat lon; do
	[[ $id = [0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z] ]] || continue
	print -r -- "	[$((++n)), $lat, $lon, \"GD${id::2}-${id:2}\"],"
done
print '	[0, 0, 0, ""]'
print '  ];'
print
print '  function mirkarte_hookfn(map) {'
print -r "	var el_t = document.createTextNode(\" ${mirtime_months[defmon - 1]} 20$defyear\");"

cat <<'EOF'
	var el_span = L.DomUtil.create("span", "");
	var el_a = L.DomUtil.create("a", "", el_span);
	el_a.href = "http://geodashing.gpsgames.org/";
	el_a.update("GeoDashing");
	el_span.appendChild(el_t);
	var el_br = L.DomUtil.create("br", "");
	map._coorscontrol._unshift(el_br)._unshift(el_span);

	var i = 0;
	while (geodashing_arr[i][0] != 0) {
		var ghlat = geodashing_arr[i][1];
		var ghlon = geodashing_arr[i][2];
		var ghmarker = L.marker([ghlat, ghlon], {
			"draggable": false
		    }).addTo(map);
		var f = llformat(ghlat, ghlon, 1);
		ghmarker.bindPopup(f[0] + ' ' + f[1] +
		    '<br /><a href="http://geodashing.gpsgames.org/cgi-bin/dp.pl?dp=' +
		    geodashing_arr[i][3] + '">' + geodashing_arr[i][3] +
		    '</a> | <a href="gpx.cgi?' + geodashing_arr[i][3] + '">GPX</a>');
		i++;
	}

	var compass = new L.Control.Compass();
	map.addControl(compass);
	compass.activate();

	var gpsctl = new L.Control.Gps({
		"setView": true,
		"title": "Centre map on your location"
	});
	map.addControl(gpsctl);
  }

 //--><!]]></script>
 <!-- see mapbox.js.example about this -->
 <script type="text/javascript" src=".mapbox.js"></script>
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
</div>
</body></html>
EOF
exit 0
