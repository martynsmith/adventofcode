#!/bin/bash

set -euf -o pipefail

cargo build --release

days=$(seq 25)

for day in $days; do
    executable=./target/release/day${day};
    if [ -x $executable ]; then
        echo "*** $day ***"
        echo ''
        time ./target/release/day${day};
        echo ''
    fi
done
