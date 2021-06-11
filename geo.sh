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

function chklatlon {
	local minus plus vmax mins
	local -i10 val
	local -u arg=${2//+([\'\"	 ]|’|′|°|�)/ }
	arg=${arg##+([	 ])}
	arg=${arg%%+([	 ])}

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
	if [[ $arg = ${minus}*([	 ])+([0-9])?(.*([0-9])) ]]; then
		arg=-${arg##$minus*([	 ])}
	elif [[ $arg = ${plus}*([	 ])+([0-9])?(.*([0-9])) ]]; then
		arg=${arg##$plus*([	 ])}
	elif [[ $arg = +([0-9])?(.*([0-9]))*([	 ])$minus ]]; then
		arg=-${arg%%*([	 ])$minus}
	elif [[ $arg = +([0-9])?(.*([0-9]))*([	 ])$plus ]]; then
		arg=${arg%%*([	 ])$plus}
	elif [[ $arg = ${minus}*([	 ]).+([0-9]) ]]; then
		arg=-0${arg##$minus*([	 ])}
	elif [[ $arg = ${plus}*([	 ]).+([0-9]) ]]; then
		arg=0${arg##$plus*([	 ])}
	elif [[ $arg = .+([0-9])*([	 ])$minus ]]; then
		arg=-0${arg%%*([	 ])$minus}
	elif [[ $arg = .+([0-9])*([	 ])$plus ]]; then
		arg=0${arg%%*([	 ])$plus}
	elif [[ $arg = ${minus}*([	 ])+([0-9])+([	 ])@(+([0-9])?(.*([0-9]))|.+([0-9])) ]]; then
		arg=${arg##$minus*([	 ])}
		val=10#${arg%%[	 ]*}
		arg=${arg##*+([	 ])}
		arg=-$(dc -e "20k $arg 60/ ${val}+ps.")
	elif [[ $arg = ${plus}*([	 ])+([0-9])+([	 ])@(+([0-9])?(.*([0-9]))|.+([0-9])) ]]; then
		arg=${arg##$plus*([	 ])}
		val=10#${arg%%[	 ]*}
		arg=${arg##*+([	 ])}
		arg=$(dc -e "20k $arg 60/ ${val}+ps.")
	elif [[ $arg = +([0-9])+([	 ])@(+([0-9])?(.*([0-9]))|.+([0-9]))*([	 ])$minus ]]; then
		arg=${arg%%*([	 ])$minus}
		val=10#${arg%%[	 ]*}
		arg=${arg##*+([	 ])}
		arg=-$(dc -e "20k $arg 60/ ${val}+ps.")
	elif [[ $arg = +([0-9])+([	 ])@(+([0-9])?(.*([0-9]))|.+([0-9]))*([	 ])$plus ]]; then
		arg=${arg%%*([	 ])$plus}
		val=10#${arg%%[	 ]*}
		arg=${arg##*+([	 ])}
		arg=$(dc -e "20k $arg 60/ ${val}+ps.")
	fi
	[[ $arg = '+'* ]] && arg=${arg#+}
	[[ $arg = ?(-)+([0-9]) ]] && arg+=.
	[[ $arg = ?(-).+([0-9]) ]] && arg=${arg/./0.}
	case $arg {
	(+([0-9]).*([0-9]))
		arg=${arg#+}
		val=10#${arg%.*}
		mins=${arg#*.}
		mins=${mins%%*(0)}
		if (( val < vmax )); then
			:
		elif (( val == vmax )) && [[ -z $mins ]]; then
			:
		else
			print -r "value $arg out of range"
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
			print -r "value $arg out of range"
			return 1
		fi
		arg=-$val.${mins:-0}
		;;
	(*)
		print -r "value $arg unrecognised"
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

	x=${|decmin2min $decimal;} || return 1
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

function lldecmin2txt {
	local lat=$1 lon=$2

	[[ $lat = *.* ]] || lat+=.
	[[ $lon = *.* ]] || lon+=.
	lat=${|decmin2txt "${lat%.*}" ".${lat#*.}" N S 2;}
	lon=${|decmin2txt "${lon%.*}" ".${lon#*.}" E W 3;}
	REPLY="$lat  $lon"
}
