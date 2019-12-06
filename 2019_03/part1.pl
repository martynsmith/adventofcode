use strict;
use warnings;
use 5.020;

my $grid;

sub walk {
    my @instructions = split /,/, shift;
    my $wire = shift;
    my $x = 0;
    my $y = 0;
    for my $i (@instructions) {
        my $dx = 0;
        my $dy = 0;
        my ($direction, $distance) = $i =~ /(\w)(\d+)/;
        given ($direction) {
            when ('U') { $dy = -1 }
            when ('D') { $dy = +1 }
            when ('L') { $dx = -1 }
            when ('R') { $dx = +1 }
        }
        for my $n (1..$distance) {
            if (defined $grid->{$y + $dy * $n}{$x + $dx * $n}) {
                $grid->{$y + $dy * $n}{$x + $dx * $n} = 'X';
            }
            else {
                $grid->{$y + $dy * $n}{$x + $dx * $n} = $wire;
            }
        }
        $x += $dx * $distance;
        $y += $dy * $distance;
    }
}

sub find_distance {
    my $grid = shift;
    my $min = undef;
    for my $y (keys %$grid) {
        for my $x (keys %{$grid->{$y}}) {
            next unless $grid->{$y}{$x} eq 'X';
            my $mdis = abs($x) + abs($y);
            say "$x,$y => $mdis";
            $min = $mdis if not defined $min or $mdis < $min;
        }
    }
    say "$min";
    say '---';
}

# $grid = {};
# walk("R8,U5,L5,D3", 1);
# walk("U7,R6,D4,L4", 2);
# find_distance($grid);

$grid = {};
walk("R75,D30,R83,U83,L12,D49,R71,U7,L72", 1);
walk("U62,R66,U55,R34,D71,R55,D58,R83", 2);
find_distance($grid);
exit;


$grid = {};
walk('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 1);
walk('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 2);
find_distance($grid);

$grid = {};
my ($line1, $line2) = <>;
chomp $line1;
chomp $line2;
walk($line1, '1');
walk($line2, '2');
find_distance($grid);
