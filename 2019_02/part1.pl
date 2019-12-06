use strict;
use warnings;
use 5.020;
use Data::Dumper;

my ($line) = <>;

chomp $line;

my @program = split /,/, $line;

# @program = (1,9,10,3,2,3,11,0,99,30,40,50);

my $cursor = 0;

$program[1] = 12;
$program[2] = 2;

while ($program[$cursor] != 99) {
    say join(',', @program);
    my $op = $program[$cursor];
    if ($op == 1) {
        $program[$program[$cursor + 3]] = $program[$program[$cursor + 1]] + $program[$program[$cursor + 2]];
    }
    if ($op == 2) {
        $program[$program[$cursor + 3]] = $program[$program[$cursor + 1]] * $program[$program[$cursor + 2]];
    }
    $cursor += 4;
}

say join(',', @program);
