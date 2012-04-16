#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
our @ARGV;

open( INPUT, "< " . $ARGV[0] ) || die "Couldn't open input $!";

sub trim($)
{
    my $string = shift;
    $string =~ s/^\s+//;
    $string =~ s/\s+$//;
    return $string;
}
#           &       Data  & Total Pred  &        Top  &  SingleTop  &        Wbx  &        Wcx  &        Wqq  &  ZJets  &        QCD  \\
#           \hline
#           1 Jet  1 Tag   &       10487   &     10443.6   &       276.2   &       706.8   &      1023.2   &      6321.7   &      1050.3   &       320.5   &       744.8   \\
my $VAR1 = [
          '#               ',
          '       Data  ',
          ' Total Fit  ',
          '        Top  ',
          '  SingleTop  ',
          '        Wbx  ',
          '        Wcx  ',
          '        Wqq  ',
          '      ZJets  ',
          '        QCD  \\\\
'
        ];

my @header = split /&/, <INPUT>;
print Dumper \@header;
my $dummy = <INPUT>;
my (%qcd_total, %zjet_total, %wjet_total, %singletop_total, %top_total);
while (<INPUT>) {
    my ($title, $data, $total_pred, $top, $singletop, $wbx, $wcx, $wqq, $zjets, $qcd) = split /&/;
    $title =~ /(\d+) Jets?\s*(\d+) Tag/;
    my $tagKey = "$1j_$2t";
    $qcd =~ s/\s*\\\\//;
    print '($title, $data, $total_pred, $top, $singletop, $wbx, $wcx, $wqq, $zjets, $qcd)'. "\n";
    print join(",",$title, $data, $total_pred, $top, $singletop, $wbx, $wcx, $wqq, $zjets, $qcd) ;
    $qcd_total{$tagKey} = trim( $qcd );
    $zjet_total{$tagKey} = trim( $zjets );
    $singletop_total{$tagKey} = trim( $singletop );
    $top_total{$tagKey} = trim( $top );
    $wjet_total{$tagKey} = trim( $wbx ) + trim( $wcx ) + trim( $wqq );
    #$top = trim( $top ); $singletop = trim( $singletop ); $zjets = trim( $zjets )l;;;
}

sub printForJSON {
    my $name = shift;
    my $keyVal = shift;
    my @list;
    while ( my ($key, $value) = each( %$keyVal ) ) {
        push @list,  "\"$key\" : $value"
    }
    return   "\"$name\" : {" . join(',',@list) . "}";
}

print '{' . join(',',
printForJSON( "QCD_total", \%qcd_total ),
printForJSON( "Top_total", \%top_total ),
printForJSON( "SingleTop_total", \%singletop_total ),
printForJSON( "WJet_total", \%wjet_total ),
printForJSON( "ZJet_total", \%zjet_total ), ) . "}\n";


