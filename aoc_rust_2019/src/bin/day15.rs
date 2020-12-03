use aoc_rust_2019::intcode::IntCodeComputer;
use std::collections::{HashMap, HashSet};

#[derive(Debug)]
enum Direction {
    North,
    South,
    West,
    East,
}

use Direction::*;

#[derive(Debug, Eq, PartialEq, Hash, Clone)]
struct Vector {
    x: i64,
    y: i64,
}

impl Vector {
    fn travel(&self, direction: &Direction) -> Vector {
        match direction {
            Direction::North => Vector {
                x: self.x,
                y: self.y - 1,
            },
            Direction::South => Vector {
                x: self.x,
                y: self.y + 1,
            },
            Direction::West => Vector {
                x: self.x + 1,
                y: self.y,
            },
            Direction::East => Vector {
                x: self.x - 1,
                y: self.y,
            },
        }
    }
}

impl std::ops::Add<&Vector> for &Vector {
    type Output = Vector;
    fn add(self, rhs: &Vector) -> Vector {
        Vector {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

fn vector_for(direction: Direction) -> Vector {
    match direction {
        Direction::North => Vector { x: 0, y: -1 },
        Direction::South => Vector { x: 0, y: 1 },
        Direction::West => Vector { x: 1, y: 0 },
        Direction::East => Vector { x: -1, y: 0 },
    }
}

fn instruction_for(direction: &Direction) -> i64 {
    match direction {
        Direction::North => 1,
        Direction::South => 2,
        Direction::West => 3,
        Direction::East => 4,
    }
}

fn print_map(map: &HashMap<Vector, char>) {
    let min_x = map.keys().map(|k| k.x).min().unwrap();
    let max_x = map.keys().map(|k| k.x).max().unwrap();
    let min_y = map.keys().map(|k| k.y).min().unwrap();
    let max_y = map.keys().map(|k| k.y).max().unwrap();
    println!("---");
    for y in min_y..max_y + 1 {
        for x in min_x..max_x + 1 {
            print!(
                "{}",
                match map.get(&Vector { x: x, y: y }) {
                    Some(c) => c,
                    None => &' ',
                }
            )
        }
        println!("");
    }
    println!("");
}

fn main() {
    let mut drone = IntCodeComputer::from_file("day15.txt");

    let mut map: HashMap<Vector, char> = HashMap::new();
    let mut unmapped: HashSet<Vector> = HashSet::new();
    let mut current_position = Vector { x: 0, y: 0 };

    map.insert(current_position.clone(), 'X');
    unmapped.insert(current_position.travel(&North));
    unmapped.insert(current_position.travel(&South));
    unmapped.insert(current_position.travel(&West));
    unmapped.insert(current_position.travel(&East));

    while unmapped.len() > 0 {
        let a = map.len();
        println!("current position: {:?}", current_position);
        for direction in &[North, South, West, East] {
            let potential_position = current_position.travel(direction);
            if unmapped.contains(&potential_position) {
                drone.add_input(instruction_for(direction));
                drone.run();
                match drone.get_output() {
                    0 => {
                        // Hit a wall
                        println!("    {:?} is a wall ({:?})", direction, potential_position);
                        unmapped.remove(&potential_position);
                        map.insert(potential_position, '#');
                    }
                    1 => {
                        println!("    moved {:?} ({:?})", direction, potential_position);
                        // Moved to new location
                        unmapped.remove(&potential_position);
                        map.insert(potential_position.clone(), '.');
                        current_position = potential_position.clone();
                        for d in &[North, South, West, East] {
                            let potentially_unmapped_position = current_position.travel(d);
                            if !map.contains_key(&potentially_unmapped_position) {
                                unmapped.insert(potentially_unmapped_position);
                            }
                        }
                        break;
                    }
                    o => panic!("Unexpected drone output: {}", o),
                }
            }
        }
        if map.len() == a {
            break;
        }
    }

    print_map(&map);
    println!("{:?}", unmapped);
}
