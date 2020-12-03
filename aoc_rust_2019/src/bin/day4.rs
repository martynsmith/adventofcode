struct Digits {
    n6: i32,
    n5: i32,
    n4: i32,
    n3: i32,
    n2: i32,
    n1: i32,
}

impl Digits {
    fn new(n: i32) -> Digits {
        Digits {
            n6: n / 100000,
            n5: n / 10000 % 10,
            n4: n / 1000 % 10,
            n3: n / 100 % 10,
            n2: n / 10 % 10,
            n1: n % 10,
        }
    }
}

fn has_double(d: &Digits) -> bool {
    return d.n6 == d.n5 || d.n5 == d.n4 || d.n4 == d.n3 || d.n3 == d.n2 || d.n2 == d.n1;
}

fn has_exclusive_double(d: &Digits) -> bool {
    return (d.n6 == d.n5 && d.n5 != d.n4)
        || (d.n6 != d.n5 && d.n5 == d.n4 && d.n4 != d.n3)
        || (d.n5 != d.n4 && d.n4 == d.n3 && d.n3 != d.n2)
        || (d.n4 != d.n3 && d.n3 == d.n2 && d.n2 != d.n1)
        || (d.n3 != d.n2 && d.n2 == d.n1);
}

fn is_incrementing(d: &Digits) -> bool {
    return d.n6 <= d.n5 && d.n5 <= d.n4 && d.n4 <= d.n3 && d.n3 <= d.n2 && d.n2 <= d.n1;
}

fn main() {
    let range_start = 124075;
    let range_end = 580769;
    let mut part1 = 0;
    let mut part2 = 0;
    for i in range_start..range_end {
        let d = Digits::new(i);
        let is_incrementing_result = is_incrementing(&d);
        if has_double(&d) && is_incrementing_result {
            part1 += 1;
        }
        if has_exclusive_double(&d) && is_incrementing_result {
            part2 += 1;
        }
    }
    println!("part 1: {}", part1);
    println!("part 2: {}", part2);
}
