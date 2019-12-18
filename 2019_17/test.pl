use strict;
use warnings;
use 5.020;

use Data::Dumper;

my $a = "R8L10R8R12R8L8L12R8L10R8L12L10L8R8L10R8R12R8L8L12L12L10L8L12L10L8R8L10R8R12R8L8L12";

say Dumper($a =~ /(.*?)(\1)/g);
