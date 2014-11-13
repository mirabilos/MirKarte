#!/bin/mksh
#-
# Copyright © 2014
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

#XXX make these CGI parameters
deflat=50.7
deflon=7.11
defzoom=9
set -A defyear -- $(date +'%y %m')
defmon=${defyear[1]}

xff="${HTTP_X_FORWARDED_FOR:+$HTTP_X_FORWARDED_FOR, }$REMOTE_ADDR"
set -A fetch -- ftp -H "X-Forwarded-For: $xff" -o -
whence -p wget >/dev/null 2>&1 && \
    set -A fetch -- wget --header "X-Forwarded-For: $xff" -qO- -T3

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
 <title>MirKarte for GeoDashing (Beta)</title>
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
EOF
print "  mirkarte_default_loc = [$deflat, $deflon, $defzoom];"

"${fetch[@]}" "http://geodashing.gpsgames.org/cgi-bin/stats.pl?startmonth=$defmon&startyear=$defyear&endmonth=$defmon&endyear=$defyear&radius=200&lat_1=$deflat&lon_1=$deflon&statstype=circle&download=Download&downloadformat=LOC" | \
    xmlstarlet sel -t -m //waypoint -v name/@id -o ' ' -v coord/@lat -o ' ' -v coord/@lon -n |&
n=0; print "  var geodashing_arr = ["
while read -pr id lat lon; do
	[[ $id = [0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z][0-9A-Z] ]] || continue
	print -r -- "	[$((++n)), $lat, $lon, \"GD${id::2}-${id:2}\"],"
done
print '	[0, 0, 0, ""]'
print '  ];'

cat <<'EOF'

  function mirkarte_hookfn(map) {
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
echo "  <span>GeoDashing ${mirtime_months[defmon - 1]} 20$defyear</span><br />"
cat <<'EOF'
  <span id="map_coors_ns"></span><br />
  <span id="map_coors_we"></span>
 </div>
</div>
</body></html>
EOF
exit 0
