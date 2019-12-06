use strict;
use warnings;
use 5.020;

my $grid1;
my $grid2;

sub walk {
    my $grid = shift;
    my @instructions = split /,/, shift;
    my $wire = shift;
    my $x = 0;
    my $y = 0;
    my $steps = 0;
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
            $grid->{$y + $dy * $n}{$x + $dx * $n} //= ++$steps;
        }
        $x += $dx * $distance;
        $y += $dy * $distance;
    }
}

sub find_best_intersection {
    my $grid1 = shift;
    my $grid2 = shift;
    my $min = undef;
    for my $y (keys %$grid1) {
        for my $x (keys %{$grid1->{$y}}) {
            next unless defined $grid2->{$y}{$x};
            my $mdis = $grid1->{$y}{$x} + $grid2->{$y}{$x};
            say "$x,$y => $grid1->{$y}{$x} + $grid2->{$y}{$x} = $mdis";
            $min = $mdis if not defined $min or $mdis < $min;
        }
    }
    say '---';
    say "$min";
    say '---';
}

$grid1 = {};
$grid2 = {};
walk($grid1, "R75,D30,R83,U83,L12,D49,R71,U7,L72");
walk($grid2, "U62,R66,U55,R34,D71,R55,D58,R83");
find_best_intersection($grid1, $grid2);

$grid1 = {};
$grid2 = {};
walk($grid1, 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51');
walk($grid2, 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7');
find_best_intersection($grid1, $grid2);

$grid1 = {};
$grid2 = {};
my ($line1, $line2) = <>;
chomp $line1;
chomp $line2;
walk($grid1, $line1);
walk($grid2, $line2);
find_best_intersection($grid1, $grid2);

say '19228 is too low';
