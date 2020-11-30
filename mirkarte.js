/*-
 * Copyright © 2014, 2015, 2017, 2018, 2020
 *	mirabilos <m@mirbsd.org>
 *
 * Provided that these terms and disclaimer and all copyright notices
 * are retained or reproduced in an accompanying document, permission
 * is granted to deal in this work without restriction, including un‐
 * limited rights to use, publicly perform, distribute, sell, modify,
 * merge, give away, or sublicence.
 *
 * This work is provided “AS IS” and WITHOUT WARRANTY of any kind, to
 * the utmost extent permitted by applicable law, neither express nor
 * implied; without malicious intent or gross negligence. In no event
 * may a licensor, author or contributor be held liable for indirect,
 * direct, other damage, loss, or other issues arising in any way out
 * of dealing in the work, even if advised of the possibility of such
 * damage or existence of a defect, except proven that it results out
 * of said person’s immediate fault when using the work as intended.
 */

var isNum = /^-?[0-9]*(\.[0-9]*)?$/;
var isTwoNum = /^-?[0-9]*(\.[0-9]*)?,-?[0-9]*(\.[0-9]*)?$/;
var isTwoNumSlashd = /^-?[0-9]*(\.[0-9]*)?\/-?[0-9]*(\.[0-9]*)?$/;
var isThreeNumSlashd = /^[1-9][0-9]*\/-?[0-9]*(\.[0-9]*)?\/-?[0-9]*(\.[0-9]*)?$/;
var map_initialised = false, myzoomcontrol_text;
var map, ctl_layers, ctl_coors, marker = false, params, params_saved = "";

var attributions = {
	"OSM": '© <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
	"OCM": '© <a href="http://www.opencyclemap.org">OpenCycleMap</a>, <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
	"MapboxAPI": '<a href="http://mapbox.com/about/maps" style="position:absolute;display:block;height:20px;width:65px;left:-70px;bottom:0px;text-indent:-9999px;z-index:99999;overflow:hidden;background-image:url(img/mapboxwm.svg);background-repeat:no-repeat;background-position:0 0;background-size:65px 20px;" target="_blank"></a>© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> — © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> — <a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a>',
	"StamenT": 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>',
	"StamenW": 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>',
	"Esri": "Tiles © Esri",
	"EsriDeLorme": "Tiles © Esri — Copyright: ©2012 DeLorme",
	"EsriWorldTopoMap": "Tiles © Esri — Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community",
	"EsriWorldImagery": "Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
	"EsriOceanBasemap": "Tiles © Esri — Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri",
	"EsriNatGeoWorldMap": "Tiles © Esri — National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC",
	"Google": 'Map data © <a href="http://googlemaps.com">Google</a>',
	"CartoDB": '© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, © <a href="https://carto.com/attribution">CARTO</a>',
	"Lyrk": '<a href="/copyright">Lizenzinformationen</a>, Tiles by <a href="http://lyrk.de/">Lyrk</a>',
	"OpenMapSurfer": 'Imagery from <a href="http://www.geog.uni-heidelberg.de/gis/index.html">GIScience Research Group @ University of Heidelberg</a> – Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
	"HikeBikeMap": 'Map Data © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Hillshading: SRTM3 v2 (<a href="http://www2.jpl.nasa.gov/srtm/">NASA</a>)',
	"ÖPNVkarte": ' (© by <a href="http://memomaps.de/">MeMoMaps</a>).',
	"OpenTopoMap": 'map data: © <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org/">SRTM</a> | map style: © <a href="https://opentopomap.org/">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
	"OpenRailwayMap": 'Data <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>, Style: <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA 2.0</a> <a href="http://www.openrailwaymap.org/">OpenRailwayMap</a>',
	"TC": '© <a href="http://www.terracaching.com/">Terra Interactive, LLC</a>'
    };

function zeropad(n, len) {
	n = "" + n;
	while (n.length < len)
		n = "0" + n;
	return (n);
}

function llformat(lat, lon, ashtml) {
	var ns, we, sns, swe, t;

	ns = lat;
	we = lon;
	if (ns < 0) {
		ns = -ns;
		sns = "S ";
	} else
		sns = "N ";
	if (we < 0) {
		we = -we;
		swe = "W ";
	} else
		swe = "E ";
	t = ns | 0;
	ns = (ns - t) * 60;
	sns = sns + zeropad(t, 2) + "° " + zeropad(ns.toFixed(3), 6);
	t = we | 0;
	we = (we - t) * 60;
	swe = swe + zeropad(t, 3) + "° " + zeropad(we.toFixed(3), 6);

	if (ashtml) {
		var snw = '<span class="nowrap">';

		if (ashtml == 2)
			return (snw + sns + " " + swe + "</span>");
		sns = snw + sns + "</span>";
		swe = snw + swe + "</span>";
	}

	return ([sns, swe]);
}

function marker_popup(marker, text) {
	marker.bindPopup(text);
	marker.on("popupopen", function () {
		var xtext, f, pos = marker.getLatLng();

		f = llformat(pos.lat, pos.lng, 1);
		xtext = text.replace(/°N/g, f[0]).replace(/°E/g, f[1]);
		marker.setPopupContent(xtext);
	    });
}

function nuke_marker() {
	if (marker !== false) {
		marker.closePopup();
		map.removeLayer(marker);
		marker = false;
	}
	delete params["m"];
	update_hash();
}

var MarkerWithAttribution = L.Marker.extend({
	options: {
		"attribution": ""
	},

	getAttribution: function () {
		return (this.options.attribution);
	}
});

var nextpos = false;
function jumptonextpos() {
	map.closePopup();
	if (nextpos !== false)
		map.fitBounds(nextpos[0], nextpos[1]);
}

mirkarte_gpx_links = [
	[ /^GC/, /\bGeocache\b/, 'http://coord.info/$&' ],
	[ /^TC/, /\bTerraCache\b/, 'http://www.terracaching.com/Cache/$&' ],
	[ /^OC/, /\bGeocache\b/, 'http://www.opencaching.de/viewcache.php?wp=$&' ],
];

function add_gpx_to_map(gpx_string, layer_name) {
	if (!/<gpx/.test(gpx_string))
		return false;
	var dom = (new DOMParser()).parseFromString(gpx_string,
	    "text/xml");
	var gjsn = toGeoJSON.gpx(dom);
	var xn = -1000, xe = -1000, xs = 1000, xw = 1000;
	ctl_layers.addOverlay(L.geoJson(gjsn, {
		coordsToLatLng: function (coords) {
			if (coords[1] > xn)
				xn = coords[1];
			if (coords[1] < xs)
				xs = coords[1];
			if (coords[0] > xe)
				xe = coords[0];
			if (coords[0] < xw)
				xw = coords[0];
			return new L.LatLng(coords[1], coords[0], coords[2]);
		},
		pointToLayer: function (feature, latlng) {
			var o = {}, res;

			if (feature.properties["sym"] == "TerraCache") {
				o["icon"] = tc_icon;
				o["attribution"] = attributions["TC"];
			}
			feature["_isWP"] = latlng;
			return (new MarkerWithAttribution(latlng, o));
		},
		onEachFeature: function (feature, layer) {
			if (!feature["_isWP"])
				return;
			var s, f, x, pos = feature["_isWP"];

			f = llformat(pos.lat, pos.lng, 2);
			x = feature.properties["name"];
			s = (x ? (x + " ") : "") + f;

			x = feature.properties["desc"];
			var n = mirkarte_gpx_links.length;
			for (var i = 0; i < n; ++i) {
				if (!mirkarte_gpx_links[i][0].test(feature.properties["name"]) ||
				    !mirkarte_gpx_links[i][1].test(feature.properties["sym"]))
					continue;
				x = '<a href="' +
				    feature.properties.name.replace(mirkarte_gpx_links[i][0],
				    mirkarte_gpx_links[i][2]) + '">' +
				    (x ? x : "(no description)") +
				    '</a>';
				break;
			}
			if (x)
				s = s + "<br />" + x;
			layer.bindPopup(s);
		}
	    }).addTo(map), layer_name);
	if (xn != -1000 && xe != -1000 && xs != 1000 && xw != 1000)
		return ([[[xs, xw], [xn, xe]], {
			"padding": [48, 48],
			"maxZoom": 14
		    }]);
	return false;
}

var show_menu_marker = (function () {
	var hasfile = false;
	var filestr = "Your browser does not support the File API";
	var current_filename = "";

	if (window.File && window.FileList && window.FileReader && window.Blob) {
		hasfile = true;
		filestr = '<fieldset><legend>GPX upload</legend>' +
		    '<div id="gpxupload"><table>' +
		    '<tr><th>*.gpx:</th><td><input type="file" id="files" name="files[]" /></td></tr>' +
		    '<tr><th>*.zip:</th><td><input type="file" id="filez" name="filez[]" /></td></tr>' +
		    '</table></div></fieldset>';
	}

	var handleGpxFileLoaded = function (e) {
		var s = "GPX " + current_filename.escapeHTML() + " loaded.";
		$("gpxupload").update(s);
		if (!/<gpx/.test(e.target.result))
			$("gpxupload").update(current_filename.escapeHTML() +
			    " is not a valid GPX file.");
		var res = add_gpx_to_map(e.target.result,
		    current_filename.escapeHTML());
		if (res !== false) {
			nextpos = res;
			s += " <a href=\"javascript:jumptonextpos();\">Show</a>";
			$("gpxupload").update(s);
		}
	};

	var handleZipExtraction = function (entry) {
		current_filename += "/" + entry.filename;
		$("gpxupload").update("Extracting " +
		    current_filename.escapeHTML());
		entry.getData(new zip.BlobWriter(), function (asblob) {
			$("gpxupload").update("Extracted " +
			    current_filename.escapeHTML());
			var reader = new FileReader();
			reader.onload = handleGpxFileLoaded;
			reader.readAsText(asblob);
		    }, function (current, total) {
			$("gpxupload").update("Extracting " +
			    current_filename.escapeHTML() + "… " +
			    current + "/" + total);
		    }, true);
	};

	var handleZipFileLoaded = function (entries) {
		var ents = new Element("ul");
		entries.forEach(function(entry) {
			var fn = "" + entry.filename;
			var a = new Element("a",
			    {"href": "#"}).update(fn.escapeHTML());
			a.addEventListener("click", function(event) {
				handleZipExtraction(entry);
				event.preventDefault();
				return (false);
			    }, false);
			ents.appendChild(new Element("li").update(a));
		    });
		if (ents.empty())
			$("gpxupload").update("Empty ZIP file: " +
			    current_filename.escapeHTML());
		else
			$("gpxupload").update("Directory of " +
			    current_filename.escapeHTML() +
			    ":").appendChild(ents);
	};

	var handleFileSelect = function (e, filetype, cb) {
		var reader, f = e.target.files[0];

		if (!f) {
			current_filename = "";
			$("gpxupload").update("No file found.");
			return;
		}
		current_filename = "" + f.name;
		$("gpxupload").update("Loading " +
		    current_filename.escapeHTML() + "…");
		if (filetype == "zip") {
			zip.createReader(new zip.BlobReader(f),
			    function (zipReader) {
				zipReader.getEntries(cb);
			    }, function (message) {
				$("gpxupload").update("ZIP error: " +
				    ("" + message).escapeHTML());
			    });
		} else {
			reader = new FileReader();
			reader.onload = cb;
			if (filetype == "text")
				reader.readAsText(f);
			else
				reader.readAsBinaryString(f);
		}
	};

	var handleGpxFileSelect = function (e) {
		handleFileSelect(e, "text", handleGpxFileLoaded);
	};

	var handleZipFileSelect = function (e) {
		handleFileSelect(e, "zip", handleZipFileLoaded);
	};

	var res = function () {
		var s, pos = map.getCenter();
		var f = llformat(pos.lat, pos.lng, 0);

		s = '<span class="nowrap">Current centre: ' + f[0] + " " +
		    f[1] + "</span><hr />" + filestr;
		L.popup().setLatLng(pos).setContent(s).openOn(map);
		if (hasfile) {
			document.getElementById("files").addEventListener("change",
			    handleGpxFileSelect, false);
			document.getElementById("filez").addEventListener("change",
			    handleZipFileSelect, false);
		}
	};

	return (res);
    })();

/* $(document).observe("hashchange", fn_hashchange); does not work */
(function () {
	var prevhash = "" + location.href.split("#")[1];
	this.checkHash = function () {
		var newhash = "" + location.href.split("#")[1];
		if (prevhash !== newhash) {
			prevhash = newhash;
			/*
			 * Event.fire(document, "hashchange");
			 * doesn’t work here
			 */
			fn_hashchange("callout");
		}
	    }.bind(this);
	if (typeof(window.onhashchange) !== "undefined" &&
	    (document.documentMode === undefined || document.documentMode > 7))
		window.onhashchange = this.checkHash;
	else
		window.setInterval(this.checkHash, 100);
    })();

var marker_icon = L.icon({
	"iconUrl": "img/marker-icon.png",
	"iconRetinaUrl": "img/marker-icon-2x.png",
	"shadowUrl": "img/marker-shadow.png",

	/* copied from L.Icon.Default */
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],

	shadowSize: [41, 41]
});
var tc_icon = L.icon({
	"iconUrl": "tc/markerTC.png",
	"shadowUrl": "tc/markerShadow.png",
	"iconSize": [20, 34],
	"iconAnchor": [10, 34],
	"popupAnchor": [0, -30],
	"shadowSize": [37, 34]
});
var fn_mousemove = function (e) {
	var f = llformat(e.latlng.lat, e.latlng.lng, 1);

	ctl_coors._lat.update(f[0]);
	ctl_coors._lon.update(f[1]);
};
var ign_hashchange = false;
var update_hash = function () {
	ign_hashchange = true;
	window.location.hash =
	    $H(params).toQueryString().replace(/%2C/gi, ",");
};
var fn_hashchange = function (event) {
	var newhash = "" + location.href.split("#")[1];
	if (newhash !== params_saved) {
		params_saved = newhash;
		params = {};
		$H(newhash.parseQuery()).each(function (pair) {
			switch (pair.key) {
			case "center_lat":
			case "center_lon":
			case "ll":
			case "zoom":
			case "mlat":
			case "mlon":
			case "m":
				params[pair.key] = pair.value;
				break;
			case "map":
				if (isThreeNumSlashd.test(pair.value)) {
					var t = pair.value.split("/");
					params["m"] = t[1] + "," + t[2];
				}
				break;
			}
		    });
	}
	if (ign_hashchange) {
		ign_hashchange = false;
		return;
	}
	if (map_initialised) {
		fn_hashchanged();
	}
};
var fn_hashchanged = function () {
	var clat = NaN, clon = NaN;
	if (isTwoNum.test(params["ll"])) {
		clat = parseFloat(params["ll"].split(",")[0]);
		clon = parseFloat(params["ll"].split(",")[1]);
		if (isNaN(clat) || isNaN(clon) ||
		    clat < -85 || clat > 85 ||
		    clon < -180 || clon > 180) {
			clat = NaN;
			clon = NaN;
		}
	}
	if ((isNaN(clat) || isNaN(clon)) &&
	    isNum.test(params["center_lat"]) &&
	    isNum.test(params["center_lon"])) {
		clat = parseFloat(params["center_lat"]);
		clon = parseFloat(params["center_lon"]);
	}
	/* defer until we know marker pos */

	var czoom;
	if (/^\d+$/.test(params["zoom"]) &&
	    !isNaN((czoom = parseFloat(params["zoom"]))) &&
	    czoom >= 0 && czoom < 32) {
		/* convert to int */
		czoom = czoom | 0;
	} else {
		czoom = mirkarte_default_loc[2];
	}
	params["zoom"] = czoom;

	var wantMarker = false, mlat, mlon;
	if (isTwoNumSlashd.test(params["m"]))
		params["m"] = params["m"].replace("/", ",");
	if (isTwoNum.test(params["m"])) {
		wantMarker = true;
		mlat = parseFloat(params["m"].split(",")[0]);
		mlon = parseFloat(params["m"].split(",")[1]);
		if (isNaN(mlat) || isNaN(mlon) ||
		    mlat < -85 || mlat > 85 ||
		    mlon < -180 || mlon > 180)
			wantMarker = false;
	}
	if (!wantMarker &&
	    isNum.test(params["mlat"]) &&
	    isNum.test(params["mlon"])) {
		wantMarker = true;
		mlat = parseFloat(params["mlat"]);
		mlon = parseFloat(params["mlon"]);
		if (isNaN(mlat) || isNaN(mlon) ||
		    mlat < -85 || mlat > 85 ||
		    mlon < -180 || mlon > 180)
			wantMarker = false;
	}
	if (!wantMarker && /1/.test(params["m"])) {
		wantMarker = true;
		mlat = clat;
		mlon = clon;
		if (isNaN(mlat) || isNaN(mlon) ||
		    mlat < -85 || mlat > 85 ||
		    mlon < -180 || mlon > 180)
			wantMarker = false;
	}
	delete params["mlat"];
	delete params["mlon"];
	if (!wantMarker) {
		delete params["m"];
		if (marker !== false) {
			map.removeLayer(marker);
			marker = false;
		}
	} else {
		params["m"] = mlat + "," + mlon;
		if (marker === false) {
			marker = L.marker([mlat, mlon], {
				"icon": marker_icon,
				"draggable": true
			    }).addTo(map).on("dragend", function(e) {
				var newloc = marker.getLatLng();

				params["m"] = newloc.lat + "," + newloc.lng;
				update_hash();
			    });
			marker_popup(marker,
			    'Marker | <a href="javascript:nuke_marker();">Hide</a><br />°N<br />°E');
		} else
			marker.setLatLng([mlat, mlon]);
	}

	if (isNaN(clat) || isNaN(clon) ||
	    clat < -85 || clat > 85 ||
	    clon < -180 || clon > 180) {
		clat = mirkarte_default_loc[0];
		clon = mirkarte_default_loc[1];
		/* jump to marker position */
		if (wantMarker) {
			clat = mlat;
			clon = mlon;
		}
	}
	delete params["center_lat"];
	delete params["center_lon"]
	params["ll"] = clat + "," + clon;

	map.setView([clat, clon], czoom);
	update_hash();
};
$(document).observe("dom:loaded", function () {
	map_initialised = false;
	fn_hashchange(false);
	map = L.map("map", {
/*		"worldCopyJump": true,*/
		"maxBounds": [[-85, -180], [85, 180]],
		"attributionControl": false,
		"zoomControl": false
	    });
	$("nomap").hide();

	var ctl_attr = L.control.attribution({
		"prefix": '<a href="https://evolvis.org/plugins/scmgit/cgi-bin/gitweb.cgi?p=useful-scripts/mirkarte.git">MirKarte</a> (Beta) | ' +
		    L.Control.Attribution.prototype.options.prefix
	    });

	var maplayerlist = [
		{
			"_name": "OpenStreetMap (0‥19)",
			"_url": "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
			"maxZoom": 19,
			"attribution": attributions["OSM"]
		},
		{
			"_name": "OSM Black&amp;White (0‥18)",
			"_url": "http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png",
			"attribution": attributions["OSM"]
		},
		{
			"_name": "wmflabs Hike &amp; Bike (0‥19)",
			"_url": "http://{s}.tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png",
			"minZoom": 0,
			"maxZoom": 19,
			"attribution": attributions["HikeBikeMap"]
		},
		{
			"_isOverlay": true,
			"_name": "wmflabs Hillshading (0‥15)",
			"_url": "http://{s}.tiles.wmflabs.org/hillshading/{z}/{x}/{y}.png",
			"minZoom": 0,
			"maxZoom": 15,
			"attribution": attributions["OSM"]
		},
		{
			"_name": "wmflabs Mapnik unlabelled (0‥18)",
			"_url": "http://{s}.tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png",
			"attribution": attributions["OSM"]
		},
		{
			"_name": "OSM Germany (0‥18)",
			"_url": "http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png",
			"attribution": attributions["OSM"]
		},
		{
			"_name": "OSM Humanitarian (0‥19)",
			"_url": "http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
			"maxZoom": 19,
			"subdomains": "ab",
			"attribution": attributions["OSM"]
		},
		{
			"_isOverlay": true,
			"_name": "openptmap Transport",
			"_url": "http://www.openptmap.org/tiles/{z}/{x}/{y}.png",
			"_nohttps": true,
			"attribution": attributions["OSM"]
		},
		{
			"_isOverlay": true,
			"_name": "OpenRailwayMap infrastructure",
			"_url": "http://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png",
			"subdomains": "abc",
			"attribution": attributions["OpenRailwayMap"]
		},
		{
			"_isOverlay": true,
			"_name": "OpenRailwayMap maxspeed",
			"_url": "http://{s}.tiles.openrailwaymap.org/maxspeed/{z}/{x}/{y}.png",
			"subdomains": "abc",
			"attribution": attributions["OpenRailwayMap"]
		},
		{
			"_isOverlay": true,
			"_name": "OpenRailwayMap signals",
			"_url": "http://{s}.tiles.openrailwaymap.org/signals/{z}/{x}/{y}.png",
			"subdomains": "abc",
			"attribution": attributions["OpenRailwayMap"]
		},
		{
			"_isOverlay": true,
			"_name": "OpenSeaMap sea marks (9‥18)",
			"_url": "http://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
			"minZoom": 9,
			"maxZoom": 18,
			"attribution": attributions["OSM"]
		},
		{
			"_name": "Thunderforest OpenCycleMap (0‥18)",
			"_url": "http://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png",
			"attribution": attributions["OCM"]
		},
		{
			"_name": "Thunderforest Transport (0‥18)",
			"_url": "http://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png",
			"attribution": attributions["OCM"]
		},
		{
			"_name": "Thunderforest Landscape (0‥18)",
			"_url": "http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png",
			"attribution": attributions["OCM"]
		},
		{
			"_name": "ÖPNVkarte (0‥18)",
			"_url": "http://tile.memomaps.de/tilegen/{z}/{x}/{y}.png",
			"attribution": attributions["OSM"] + attributions["ÖPNVkarte"]
		},
		{
			"_name": "OpenTopoMap (0‥18)",
			"_url": "http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
			"subdomains": "abc",
			"attribution": attributions["OpenTopoMap"]
		},
		{
			"_name": "Lima Labs Open Carto (0‥18)",
			"_url": "http://cdn.lima-labs.com/{z}/{x}/{y}.png?free",
			"attribution": attributions["OSM"]
		},
		{
			"_name": "Stamen Toner (0‥20)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 0,
			"maxZoom": 20,
			"attribution": attributions["StamenT"]
		},
		{
			"_name": "Stamen TonerBackground (0‥20)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 0,
			"maxZoom": 20,
			"attribution": attributions["StamenT"]
		},
		{
			"_isOverlay": true,
			"_name": "Stamen TonerHybrid (0‥20)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/toner-hybrid/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 0,
			"maxZoom": 20,
			"attribution": attributions["StamenT"]
		},
		{
			"_isOverlay": true,
			"_name": "Stamen TonerLines (0‥20)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/toner-lines/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 0,
			"maxZoom": 20,
			"attribution": attributions["StamenT"]
		},
		{
			"_isOverlay": true,
			"_name": "Stamen TonerLabels (0‥20)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/toner-labels/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 0,
			"maxZoom": 20,
			"attribution": attributions["StamenT"]
		},
		{
			"_name": "Stamen TonerLite (0‥20)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 0,
			"maxZoom": 20,
			"attribution": attributions["StamenT"]
		},
		{
			"_name": "Stamen Terrain (4‥18)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 4,
			"maxZoom": 18,
			"attribution": attributions["StamenT"]
		},
		{
			"_isOverlay": true,
			"_name": "Stamen TerrainLabels (4‥18)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/terrain-labels/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 4,
			"maxZoom": 18,
			"attribution": attributions["StamenT"]
		},
		{
			"_isOverlay": true,
			"_name": "Stamen TerrainLines (4‥18)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/terrain-lines/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 4,
			"maxZoom": 18,
			"attribution": attributions["StamenT"]
		},
		{
			"_name": "Stamen TerrainBackground (4‥18)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}.png",
			"subdomains": "abcd",
			"minZoom": 4,
			"maxZoom": 18,
			"attribution": attributions["StamenT"]
		},
		{
			"_name": "Stamen Watercolor (3‥16)",
			"_url": "http://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg",
			"subdomains": "abcd",
			"minZoom": 3,
			"maxZoom": 16,
			"attribution": attributions["StamenW"]
		},
		{
			"_name": "de Topo (WMS)",
			"_url": "https://sg.geodatenzentrum.de/wms_webatlasde__8f827e84-bdc9-cda4-aad0-f9711caab5c3?",
			"_wms": true,
			"attribution": "Bundesamt für Kartographie und Geodäsie",
			"format": "image/jpeg",
			"layers": "webatlasde"
		},
		{
			"_name": "Google Maps (0‥20)",
			"_url": "http://mt{s}.googleapis.com/vt?x={x}&y={y}&z={z}",
			"subdomains": "0123",
			"maxZoom": 20,
			"attribution": attributions["Google"]
		},
		{
			"_name": "Google Satellite (0‥20)",
			"_url": "http://mt{s}.googleapis.com/vt?lyrs=s&x={x}&y={y}&z={z}",
			"subdomains": "0123",
			"maxZoom": 20,
			"attribution": attributions["Google"]
		},
		{
			"_name": "Google Terrain (0‥20)",
			"_url": "http://mt{s}.googleapis.com/vt?lyrs=p&x={x}&y={y}&z={z}",
			"subdomains": "0123",
			"maxZoom": 20,
			"attribution": attributions["Google"]
		},
		{
			"_name": "Esri WorldStreetMap (0‥18)",
			"_url": "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
			"attribution": attributions["Esri"]
		},
		{
			"_name": "Esri DeLorme (0‥11)",
			"_url": "http://server.arcgisonline.com/ArcGIS/rest/services/Specialty/DeLorme_World_Base_Map/MapServer/tile/{z}/{y}/{x}",
			"maxZoom": 11,
			"attribution": attributions["EsriDeLorme"]
		},
		{
			"_name": "Esri WorldTopoMap (0‥18)",
			"_url": "http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
			"attribution": attributions["EsriWorldTopoMap"]
		},
		{
			"_name": "Esri WorldImagery (0‥18)",
			"_url": "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
			"attribution": attributions["EsriWorldImagery"]
		},
		{
			"_name": "Esri OceanBasemap (0‥11)",
			"_url": "http://services.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}",
			"maxZoom": 11,
			"attribution": attributions["EsriOceanBasemap"]
		},
		{
			"_name": "Esri NatGeoWorldMap (0‥18)",
			"_url": "http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",
			"attribution": attributions["EsriNatGeoWorldMap"]
		},
/*
		{
			"_name": "MapSurfer.NET OSM Roads",
			"_url": "http://korona.geog.uni-heidelberg.de/tiles/roads/x={x}&y={y}&z={z}",
			"attribution": attributions["OpenMapSurfer"]
		},
		{
			"_name": "MapSurfer.NET OSM Semitransparent",
			"_url": "http://korona.geog.uni-heidelberg.de/tiles/hybrid/x={x}&y={y}&z={z}",
			"attribution": attributions["OpenMapSurfer"]
		},
 */
		{
			"_name": "MapSurfer.NET OSM Administrative Boundaries",
			"_url": "http://korona.geog.uni-heidelberg.de/tiles/adminb/x={x}&y={y}&z={z}",
			"_disabled": true,
			"attribution": attributions["OpenMapSurfer"]
		},
		{
			"_name": "Lyrk (0‥18)",
			"_url": "https://tiles.lyrk.org/ls/{z}/{x}/{y}",
			"attribution": attributions["Lyrk"]
		},
		{
			"_name": "CartoDB Positron (0‥18)",
			"_url": "http://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
			"attribution": attributions["CartoDB"]
		},
		{
			"_name": "CartoDB Dark Matter (0‥18)",
			"_url": "http://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
			"attribution": attributions["CartoDB"]
		}
	    ];
	if (typeof mirkarte_mapbox_token !== 'undefined') maplayerlist = maplayerlist.concat([
		{
			"_name": "Mapbox Satellite (0‥22)",
			"_url": "https://api.mapbox.com/v4/{id}/{z}/{x}/{y}.jpg90?access_token={accessToken}",
			"id": "mapbox.satellite",
			"accessToken": mirkarte_mapbox_token,
			"minZoom": 0,
			"maxZoom": 22,
			"attribution": attributions["MapboxAPI"]
		},
		{
			"_name": "Mapbox Hybrid (0‥22)",
			"_url": "https://api.mapbox.com/v4/{id}/{z}/{x}/{y}.jpg70?access_token={accessToken}",
			"id": "mapbox.satellite,mapbox.country-boundaries-v1,mapbox.mapbox-streets-v8,mapbox.mapbox-incidents-v1,mapbox.mapbox-traffic-v1",
			"accessToken": mirkarte_mapbox_token,
			"minZoom": 0,
			"maxZoom": 22,
			"attribution": attributions["MapboxAPI"]
		},
		{
			"_name": "Mapbox Satellite+Streets (0‥22)",
			"_url": "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
			"id": "mapbox/satellite-streets-v11",
			"tileSize": 512,
			"zoomOffset": -1,
			"accessToken": mirkarte_mapbox_token,
			"minZoom": 0,
			"maxZoom": 22,
			"attribution": attributions["MapboxAPI"]
		},
		{
			"_name": "Mapbox Streets (0‥22)",
			"_url": "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
			"id": "mapbox/streets-v11",
			"tileSize": 512,
			"zoomOffset": -1,
			"accessToken": mirkarte_mapbox_token,
			"minZoom": 0,
			"maxZoom": 22,
			"attribution": attributions["MapboxAPI"]
		},
		{
			"_name": "Mapbox Light (0‥22)",
			"_url": "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
			"id": "mapbox/light-v10",
			"tileSize": 512,
			"zoomOffset": -1,
			"accessToken": mirkarte_mapbox_token,
			"minZoom": 0,
			"maxZoom": 22,
			"attribution": attributions["MapboxAPI"]
		},
		{
			"_name": "Mapbox Dark (0‥22)",
			"_url": "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
			"id": "mapbox/dark-v10",
			"tileSize": 512,
			"zoomOffset": -1,
			"accessToken": mirkarte_mapbox_token,
			"minZoom": 0,
			"maxZoom": 22,
			"attribution": attributions["MapboxAPI"]
		},
		{
			"_name": "Mapbox Draußen (0‥22)",
			"_url": "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
			"id": "mirabilos/cki3kecpw2sm619mye2622h5l",
			"tileSize": 512,
			"zoomOffset": -1,
			"accessToken": mirkarte_mapbox_token,
			"minZoom": 0,
			"maxZoom": 22,
			"attribution": attributions["MapboxAPI"]
		}
	    ]);
	ctl_layers = function (map, layers) {
		var baseMaps = {};
		var overlays = {};
		var n = layers.length;
		var ishttps = (location.protocol === "https:");

		for (var i = 0; i < n; ++i) {
			var data = layers[i];
			var name = data["_name"];
			var url = data["_url"];
			var layer;

			if (ishttps) {
				if (data["_nohttps"])
					data["_disabled"] = true;
				url = url.replace(/^http:/, "https:");
			}

			delete data["_name"];
			delete data["_url"];
			if (data["_wms"]) {
				delete data["_wms"];
				layer = L.tileLayer.wms(url, data);
			} else
				layer = L.tileLayer(url, data);
			if (i == 0)
				layer.addTo(map);
			(data["_isOverlay"] ? overlays : baseMaps)[name] = layer;
		}
		return (L.control.layers(baseMaps, overlays));
	    } (map, maplayerlist);

	var myzoomclass = L.Control.Zoom.extend({
		onAdd: function (map) {
			var container = L.Control.Zoom.prototype.onAdd.apply(this, [map]);

			myzoomcontrol_text = this._createButton("-",
			    "Menu", "myzoomcontrol-text", false,
			    show_menu_marker, false);
			container.insertBefore(myzoomcontrol_text,
			    this._zoomOutButton);

			return (container);
		}
	    });
	var ctl_zoom = new myzoomclass();

	var ctl_scale = L.control.scale();

	var mycoorsclass = L.Control.extend({
		options: {
			"position": "bottomright",
			"autoZIndex": true
		},
		_unshift: function (el) {
			this._firstchild = this._container.insertBefore(el, this._firstchild);
			return this;
		},
		onAdd: function (map) {
			this._container = L.DomUtil.create("div", "leaflet-control");
			this._container.id = "map_coors";
			this._lat = L.DomUtil.create("span", "", this._container);
			this._firstchild = this._lat;
			this._container.appendChild(L.DomUtil.create("br", ""));
			this._lon = L.DomUtil.create("span", "", this._container);
			return this._container;
		}
	    });
	ctl_coors = new mycoorsclass();

	var ctl_compass = new L.Control.Compass();

	var ctl_gps = new L.Control.Gps({
		"setView": true,
		"title": "Centre map on your location"
	});

	map.addControl(ctl_attr);
	map.addControl(ctl_coors);
	map.addControl(ctl_scale);
	map.addControl(ctl_zoom);
	map.addControl(ctl_gps);
	map.addControl(ctl_layers);
	map.addControl(ctl_compass);

	map_initialised = true;
	ctl_compass.activate();
	map.on("moveend", function () {
		var newloc = map.getCenter();

		params["ll"] = newloc.lat + "," + newloc.lng;
		update_hash();
	    });
	map.on("zoomend", function () {
		myzoomcontrol_text.innerHTML = map.getZoom();
		params["zoom"] = map.getZoom();
		update_hash();
	    });
	map.on("contextmenu", function (e) {
		var l = e.latlng, llat = l.lat, llon = l.lng;
		var f = llformat(llat, llon, 0);
		var s = '<span class="nowrap">d: ' + llat + "," + llon +
		    '</span><br /><span class="nowrap">dm: ' + f[0] +
		    " " + f[1] + "</span>";

		L.popup().setLatLng(l).setContent(s).openOn(map);
		if (marker === false) {
			params["mlat"] = llat;
			params["mlon"] = llon;
			fn_hashchanged();
		}
	    });
	map.on("dragstart", function () { map.off("mousemove", fn_mousemove); });
	map.on("dragend", function () { map.on("mousemove", fn_mousemove); });
	fn_hashchange(false);
	if (!L.Browser.touch)
		fn_mousemove({"latlng": map.getCenter()});
	map.on("mousemove", fn_mousemove);
	$("map").focus();
	if (typeof mirkarte_hookfn == 'function')
		mirkarte_hookfn(map);
});
