extern crate regex;
use regex::Regex;

extern crate num;
use num::integer::lcm;

fn step_dimension(dimension: &mut Vec<i32>, moon_count: usize) {
    let index_combinations: Vec<(usize, usize)> =
        vec![(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)];

    for (i1, i2) in index_combinations.iter() {
        if dimension[*i1] < dimension[*i2] {
            dimension[*i1 + moon_count] += 1;
            dimension[*i2 + moon_count] -= 1;
        }
        if dimension[*i1] > dimension[*i2] {
            dimension[*i1 + moon_count] -= 1;
            dimension[*i2 + moon_count] += 1;
        }
    }
    for i in 0..4 {
        dimension[i] += dimension[i + moon_count];
    }
}

fn main() {
    let mut dx = vec![];
    let mut dy = vec![];
    let mut dz = vec![];

    // parse file
    let moon_regexp = Regex::new(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>").unwrap();
    let moons = std::fs::read_to_string("day12.txt").expect("Couldn't ready day11.txt");
    for line in moons.trim().split("\n") {
        let captures = moon_regexp.captures(line).unwrap();
        dx.push(captures[1].parse().unwrap());
        dy.push(captures[2].parse().unwrap());
        dz.push(captures[3].parse().unwrap());
    }

    let moon_count = dx.len();
    dx.resize(moon_count * 2, 0);
    dy.resize(moon_count * 2, 0);
    dz.resize(moon_count * 2, 0);

    let mut dx_steps = 0u64;
    let mut dy_steps = 0u64;
    let mut dz_steps = 0u64;

    let initial_dx = dx.clone();
    let initial_dy = dy.clone();
    let initial_dz = dz.clone();

    for _ in 0..1000 {
        step_dimension(&mut dx, moon_count);
        step_dimension(&mut dy, moon_count);
        step_dimension(&mut dz, moon_count);
        dx_steps += 1;
        dy_steps += 1;
        dz_steps += 1;
        if dx == initial_dx {
            panic!("dx too soon");
        }
        if dy == initial_dy {
            panic!("dy too soon");
        }
        if dz == initial_dz {
            panic!("dz too soon");
        }
    }

    let mut part1 = 0;
    for i in 0..moon_count {
        part1 += (dx[i].abs() + dy[i].abs() + dz[i].abs())
            * (dx[i + moon_count].abs() + dy[i + moon_count].abs() + dz[i + moon_count].abs());
    }
    println!("part 1: {}", part1);

    loop {
        step_dimension(&mut dx, moon_count);
        dx_steps += 1;
        if dx == initial_dx {
            break;
        }
    }

    loop {
        step_dimension(&mut dy, moon_count);
        dy_steps += 1;
        if dy == initial_dy {
            break;
        }
    }

    loop {
        step_dimension(&mut dz, moon_count);
        dz_steps += 1;
        if dz == initial_dz {
            break;
        }
    }
    println!("part 2: {}", lcm(lcm(dx_steps, dy_steps), dz_steps));
}
