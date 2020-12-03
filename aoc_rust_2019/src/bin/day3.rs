use std::collections::HashMap;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

#[derive(Eq, PartialEq, Hash, Debug, Copy, Clone)]
struct Point {
    x: i64,
    y: i64,
}

fn get_grid(line: &str) -> HashMap<Point, i64> {
    let mut grid = HashMap::new();
    grid.reserve(160000);

    let mut pos = Point { x: 0, y: 0 };
    let mut steps = 1;

    for instruction in line.trim().split(",") {
        let (direction, distance) = instruction.split_at(1);
        let distance: i64 = distance.parse().expect("Not a number");
        let action: Box<dyn Fn(Point) -> Point> = match direction {
            "U" => Box::new(|p: Point| Point { x: p.x, y: p.y - 1 }),
            "D" => Box::new(|p: Point| Point { x: p.x, y: p.y + 1 }),
            "L" => Box::new(|p: Point| Point { x: p.x - 1, y: p.y }),
            "R" => Box::new(|p: Point| Point { x: p.x + 1, y: p.y }),
            _ => panic!("Invalid direction: {}", direction),
        };
        for _ in 1..distance + 1 {
            pos = action(pos);
            grid.insert(pos, steps);
            steps += 1;
        }
    }
    return grid;
}

fn main() {
    let file = File::open("day3.txt").expect("Error opening file");
    let mut reader = BufReader::new(file);
    let mut line1 = String::new();
    let mut line2 = String::new();
    reader.read_line(&mut line1).expect("Couldn't read file");
    reader.read_line(&mut line2).expect("Couldn't read file");

    let grid1 = get_grid(&line1);
    let grid2 = get_grid(&line2);

    let mut part1: i64 = std::i64::MAX;
    let mut part2: i64 = std::i64::MAX;

    for p1 in grid1.keys() {
        if !grid2.contains_key(p1) {
            continue;
        }
        if p1.x.abs() + p1.y.abs() < part1 {
            part1 = p1.x.abs() + p1.y.abs();
        }
        let g1distance = grid1.get(p1).expect("nope");
        let g2distance = grid2.get(p1).expect("nope");
        if g1distance + g2distance < part2 {
            part2 = g1distance + g2distance;
        }
    }
    println!("part1: {}", part1);
    println!("part2: {}", part2);
}
