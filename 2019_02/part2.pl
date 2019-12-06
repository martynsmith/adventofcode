use strict;
use warnings;
use 5.020;
use Data::Dumper;

my ($line) = <>;
chomp $line;
my @initial_program = split /,/, $line;

sub run {
    my ($noun, $verb, @program) = @_;

    my $cursor = 0;

    $program[1] = $noun;
    $program[2] = $verb;

    while ($program[$cursor] != 99) {
        # say join(',', @program);
        my $op = $program[$cursor];
        if ($op == 1) {
            $program[$program[$cursor + 3]] = $program[$program[$cursor + 1]] + $program[$program[$cursor + 2]];
        }
        if ($op == 2) {
            $program[$program[$cursor + 3]] = $program[$program[$cursor + 1]] * $program[$program[$cursor + 2]];
        }
        $cursor += 4;
    }

    return $program[0];
}

for (my $x = 0; $x < 100; $x++) {
    for (my $y = 0; $y < 100; $y++) {
        say $x, ' ', $y, ' ', run($x, $y, @initial_program);
    }
}
