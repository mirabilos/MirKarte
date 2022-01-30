# -*- mode: sh -*-
#-
# Copyright © 2014, 2021
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
# Geodesic helper functions

# lat_decimal=$(chklatlon lat "$userinput")  # same for lon
# userinput: decimal, geocaching (deg/min) or deg/min/sec
function chklatlon {
	local minus plus vmax mins
	local -i10 val
	local -u arg=${2//+([\'\"	 ]|’|′|°|�)/ }
	if [[ $arg = *.* ]]; then
		arg=${arg//,/ }
	else
		arg=${arg//,/.}
	fi
	arg=${arg##+( )}
	arg=${arg%%+( )}

	case $1 {
	(lat)
		minus=S
		plus=N
		vmax=90
		;;
	(lon)
		minus=W
		plus=E
		vmax=180
		;;
	(*)
		print internal error
		return 1
		;;
	}
	if [[ $arg = ${minus}*( )+([0-9])?(.*([0-9])) ]]; then
		arg=-${arg##$minus*( )}
	elif [[ $arg = ${plus}*( )+([0-9])?(.*([0-9])) ]]; then
		arg=${arg##$plus*( )}
	elif [[ $arg = +([0-9])?(.*([0-9]))*( )$minus ]]; then
		arg=-${arg%%*( )$minus}
	elif [[ $arg = +([0-9])?(.*([0-9]))*( )$plus ]]; then
		arg=${arg%%*( )$plus}
	elif [[ $arg = ${minus}*( ).+([0-9]) ]]; then
		arg=-0${arg##$minus*( )}
	elif [[ $arg = ${plus}*( ).+([0-9]) ]]; then
		arg=0${arg##$plus*( )}
	elif [[ $arg = .+([0-9])*( )$minus ]]; then
		arg=-0${arg%%*( )$minus}
	elif [[ $arg = .+([0-9])*( )$plus ]]; then
		arg=0${arg%%*( )$plus}
	elif [[ $arg = ${minus}*( )+([0-9])+( )@(+([0-9])?(.*([0-9]))|.+([0-9])) ]]; then
		arg=${arg##$minus*( )}
		val=10#${arg%% *}
		arg=${arg##*+( )}
		arg=-$(dc -e "20k $arg 60/ ${val}+ps.")
	elif [[ $arg = ${plus}*( )+([0-9])+( )@(+([0-9])?(.*([0-9]))|.+([0-9])) ]]; then
		arg=${arg##$plus*( )}
		val=10#${arg%% *}
		arg=${arg##*+( )}
		arg=$(dc -e "20k $arg 60/ ${val}+ps.")
	elif [[ $arg = +([0-9])+( )@(+([0-9])?(.*([0-9]))|.+([0-9]))*( )$minus ]]; then
		arg=${arg%%*( )$minus}
		val=10#${arg%% *}
		arg=${arg##*+( )}
		arg=-$(dc -e "20k $arg 60/ ${val}+ps.")
	elif [[ $arg = +([0-9])+( )@(+([0-9])?(.*([0-9]))|.+([0-9]))*( )$plus ]]; then
		arg=${arg%%*( )$plus}
		val=10#${arg%% *}
		arg=${arg##*+( )}
		arg=$(dc -e "20k $arg 60/ ${val}+ps.")
	elif [[ $arg = ${minus}*( )+([0-9])+( )+([0-9])+( )@(+([0-9])?(.*([0-9]))|.+([0-9])) ]]; then
		arg=${arg##$minus*( )}
		mins=${arg#* }
		val=10#${arg%% *}
		arg=$mins
		mins=10#${arg%% *}
		arg=${arg##*+( )}
		arg=-$(dc -e "20k $arg 60/ $((mins))+ 60/ ${val}+ps.")
	elif [[ $arg = ${plus}*( )+([0-9])+( )+([0-9])+( )@(+([0-9])?(.*([0-9]))|.+([0-9])) ]]; then
		arg=${arg##$plus*( )}
		mins=${arg#* }
		val=10#${arg%% *}
		arg=$mins
		mins=10#${arg%% *}
		arg=${arg##*+( )}
		arg=$(dc -e "20k $arg 60/ $((mins))+ 60/ ${val}+ps.")
	elif [[ $arg = +([0-9])+( )+([0-9])+( )@(+([0-9])?(.*([0-9]))|.+([0-9]))*( )$minus ]]; then
		arg=${arg%%*( )$minus}
		mins=${arg#* }
		val=10#${arg%% *}
		arg=$mins
		mins=10#${arg%% *}
		arg=${arg##*+( )}
		arg=-$(dc -e "20k $arg 60/ $((mins))+ 60/ ${val}+ps.")
	elif [[ $arg = +([0-9])+( )+([0-9])+( )@(+([0-9])?(.*([0-9]))|.+([0-9]))*( )$plus ]]; then
		arg=${arg%%*( )$plus}
		mins=${arg#* }
		val=10#${arg%% *}
		arg=$mins
		mins=10#${arg%% *}
		arg=${arg##*+( )}
		arg=$(dc -e "20k $arg 60/ $((mins))+ 60/ ${val}+ps.")
	fi
	arg=${arg#+}
	[[ $arg = ?(-)+([0-9]) ]] && arg+=.
	[[ $arg = ?(-).+([0-9]) ]] && arg=${arg/./0.}
	case $arg {
	(+([0-9]).*([0-9]))
		#arg=${arg#+}
		val=10#${arg%.*}
		mins=${arg#*.}
		mins=${mins%%*(0)}
		if (( val < vmax )); then
			:
		elif (( val == vmax )) && [[ -z $mins ]]; then
			:
		else
			print -r "value ${arg@Q} out of range"
			return 1
		fi
		arg=$val.${mins:-0}
		;;
	(-+([0-9]).*([0-9]))
		arg=${arg#-}
		val=10#${arg%.*}
		mins=${arg#*.}
		mins=${mins%%*(0)}
		if (( val < vmax )); then
			:
		elif (( val == vmax )) && [[ -z $mins ]]; then
			:
		else
			print -r "value ${arg@Q} out of range"
			return 1
		fi
		arg=-$val.${mins:-0}
		;;
	(*)
		print -r "value ${arg@Q} unrecognised"
		return 1
		;;
	}
	print -r -- $arg
}

function decmin2min {
	local x=${1#.}0000000
	typeset -i10 -Z9 y

	x=10#${x::7}
	(( y = x * 60 ))

	REPLY=${y::2}.${y:2}
}

function decmin2txt {
	local graticule=$1 decimal=$2 plus=$3 minus=$4 places=$5 x
	typeset -i10 -Z$places n

	if [[ $graticule = -* ]]; then
		REPLY=$minus
	else
		REPLY=$plus
	fi
	n=10#${graticule#-}
	REPLY+=" ${n}° "

	if ! x=${|decmin2min $decimal;}; then
		REPLY="unable to convert ${decimal@Q}"
		return 1
	fi
	typeset -i10 -Z2 n=${x%.*}
	x=${x#*.}
	typeset -i10 -Z4 m=${x::4}
	if (( ${x:4:1} >= 5 )); then
		if (( ++m > 9999 )); then
			(( ++n ))
			m=0
		fi
	fi
	REPLY+=$n.$m
}

# echo "${|lldecmin2txt $lat_decimal $lon_decimal;}"
function lldecmin2txt {
	local lat=$1 lon=$2

	[[ $lat = *.* ]] || lat+=.
	[[ $lon = *.* ]] || lon+=.
	lat=${|decmin2txt "${lat%.*}" ".${lat#*.}" N S 2;}
	lon=${|decmin2txt "${lon%.*}" ".${lon#*.}" E W 3;}
	REPLY="$lat  $lon"
}

# distance lat1 lon1 lat2 lon2 → metres (rounded to millimetres), error < ¼%
distance() (
	set -e
	# make GNU bc use POSIX mode and shut up
	export BC_ENV_ARGS=-qs

	# assignment of constants, variables and functions
	# p: multiply with to convert from degrees to radians (π/180)
	# r: earth radius in metres
	# d: distance
	# h: haversine intermediate
	# i,j: (lat,lon) point 1
	# x,y: (lat,lon) point 2
	# k: delta lat
	# l: delta lon
	# m: sin(k/2) (square root of hav(k))
	# n: sin(l/2) (  partial haversine  )
	# n(x): arcsin(x)
	# r(x,n): round x to n decimal digits
	# v(x): sign (Vorzeichen)
	# w(x): min(1, sqrt(x)) (Wurzel)

	bc -l <<-EOF
	scale=64
	define n(x) {
		if (x == -1) return (-2 * a(1))
		if (x == 1) return (2 * a(1))
		return (a(x / sqrt(1 - x*x)))
	}
	define v(x) {
		if (x < 0) return (-1)
		if (x > 0) return (1)
		return (0)
	}
	define r(x, n) {
		auto o
		o = scale
		if (scale < (n + 1)) scale = (n + 1)
		x += v(x) * 0.5 * A^-n
		scale = n
		x /= 1
		scale = o
		return (x)
	}
	define w(x) {
		if (x >= 1) return (1)
		return (sqrt(x))
	}
	/* WGS84 reference ellipsoid: große Halbachse (metres), Abplattung */
	i = 6378136.600
	x = 1/298.257223563
	/* other axis */
	j = i * (1 - x)
	/* mean radius resulting */
	r = (2 * i + j) / 3
	/* coordinates */
	p = (4 * a(1) / 180)
	i = (p * $1)
	j = (p * $2)
	x = (p * $3)
	y = (p * $4)
	/* calculation */
	k = (x - i)
	l = (y - j)
	m = s(k / 2)
	n = s(l / 2)
	h = ((m * m) + (c(i) * c(x) * n * n))
	d = 2 * r * n(w(h))
	r(d, 3)
	EOF
)
