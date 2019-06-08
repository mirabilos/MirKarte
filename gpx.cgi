#!/usr/bin/perl -T
# From MirOS: www/files/wp.cgi,v 1.28 2018/08/29 02:13:26 tg Exp $
#-
# Copyright © 2013, 2014, 2019
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

use strict;
use warnings;

# magic to allow including relative to dirname($0)
use FindBin qw/$Bin/;
BEGIN {
	if ($Bin =~ m!([\w\./]+)!) {
		$Bin = $1;
	} else {
		die "Bad directory $Bin\n";
	}
}
use lib $Bin;
# include wp.pm, hopefully from dirname($0)
use wp;

# for gpx.sh calls
chdir($Bin) or die;

my $output = "";
my $query = "";
my $found = 0;

if (defined($ENV{QUERY_STRING})) {
	for my $p (split(/[;&]+/, $ENV{QUERY_STRING})) {
		next unless $p;
		$p =~ y/+/ /;
		my ($key, $val) = split(/=/, $p, 2);
		next unless defined($key);

		next unless ($key eq "q");
		next unless defined($val);
		$val =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/chr(hex($1))/eg;
		next if $val =~ /[\t\r\n]/;
		$query = $val;
	}
	if ($query eq "") {
		my $p = $ENV{QUERY_STRING};
		$p =~ y/+/ /;
		$p =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/chr(hex($1))/eg;
		next if $p =~ /[\t\r\n]/;
		$query = $p;
	}
}

# ltrim and rtrim
$query =~ s/^\s+//;
$query =~ s/\s+$//;

# handle early, before uppercasing
my ($code, $label, $url) = explwp($query);
if ($code eq 'm/') {
	&redirect($url);
}
if ($code =~ m!^(gh|Gh)$!) {
	$output = $label;
	$found = 2;
	$query = "";
}

# early drop invalid requests
$query = "" unless $query =~ /^[0-9A-Za-z_-]*$/;
# uppercase, nice to the user
$query =~ y/a-z/A-Z/;

# local substitution helper
sub chkwp($) {
	my ($q) = @_;
	my ($code, $label, $url) = explwp($q);

	# once only
	$found = -1 unless $found == 0;

	# not implemented yet
	if ($code ne "") {
		$output = $url;
		$found = 1 if $found == 0;
	}

	# via ./gpx.sh
	if ($code =~ m!^(GD|VX|gh|Gh)$!) {
		$output = $label;
		$found = 2 if $found == 1;
	}

	# via redirect
	if ($code =~ m!^(OC)$!) {
		$output = $label;
		$found = 3 if $found == 1;
	}

	return ($url);
}

if ($query ne "") {
	substwps($query);
}

if ($found == 3) {
	&redirect("http://www.opencaching.de/search.php?searchbywp=1&showresult=1&output=GPX&f_inactive=0&f_ignored=0&wp=$output") if
	    ($output =~ m!^OC!);

	# fall through
	$found = 0;
}

if ($found == 2) {
	delete $ENV{'PATH'};
	my $gpx = qx(./gpx.sh $output);

	if ($? == 0 && $gpx =~ m!<wpt!) {
		print("Content-type: application/force-download\r\n");
		printf("Content-Length: %d\r\n", length $gpx);
		print("Content-Disposition: attachment; filename=\"$output.gpx\"\r\n");
		print("X-Content-Type-Options: nosniff\r\n");
		print("\r\n$gpx");
		exit(0);
	}

	# fall through
	$found = 0;
}

$output = "http://www.mirbsd.org/wp.htm" unless ($found > 0);
&redirect($output);
