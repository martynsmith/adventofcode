use strict;
use warnings;
use 5.020;

my $total = 0;
while (<>) {
    my $fuel =int($_ / 3) - 2;

    my $fuel_for_fuel = int($fuel / 3) - 2;

    while ($fuel_for_fuel >= 0) {
        $fuel += $fuel_for_fuel;
        $fuel_for_fuel = int($fuel_for_fuel / 3) - 2;
    }

    $total += $fuel;
}

say $total;
