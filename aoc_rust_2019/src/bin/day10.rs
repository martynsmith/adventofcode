use std::collections::{HashMap, HashSet};

#[derive(Debug, Eq, PartialEq, Hash, Clone)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let input = std::fs::read_to_string("day10.txt").expect("Couldn't read file");

    let mut x = 0i32;
    let mut y = 0i32;

    let mut asteroids: HashSet<Point> = HashSet::new();

    for c in input.chars() {
        match c {
            '.' => x += 1,
            '#' => {
                asteroids.insert(Point { x, y });
                x += 1
            }
            '\n' => {
                x = 0;
                y += 1;
            }
            _ => panic!("unexpected char: {}", c),
        }
    }

    let mut part1 = (0usize, Point { x: 0, y: 0 });

    for p in asteroids.iter() {
        let mut visible: HashSet<i32> = HashSet::with_capacity(asteroids.len());

        for vp in asteroids.iter() {
            if p.x == vp.x && p.y == vp.y {
                continue;
            }
            let ax = (vp.x - p.x) as f32;
            let ay = (vp.y - p.y) as f32;
            let angle = (ax.atan2(ay) * 1e8) as i32;
            visible.insert(angle);
        }

        if visible.len() > part1.0 {
            part1 = (visible.len(), p.clone());
        }
    }

    let mut asteroids_for_angle: HashMap<i32, Vec<(i32, Point)>> = HashMap::new();
    let origin = part1.1.clone();

    let mut angles = HashSet::<i32>::new();

    for vp in asteroids {
        if origin.x == vp.x && origin.y == vp.y {
            continue;
        }
        let ax = vp.x - origin.x;
        let ay = vp.y - origin.y;
        let angle = ((ax as f32).atan2(ay as f32) * 1e8) as i32;
        angles.insert(angle);
        match asteroids_for_angle.get_mut(&angle) {
            Some(value) => value.push((ax.abs() + ay.abs(), vp)),
            None => {
                asteroids_for_angle.insert(angle, [(ax.abs() + ay.abs(), vp)].to_vec());
            }
        }
    }

    for v in asteroids_for_angle.values_mut() {
        v.sort_by_key(|d| -d.0);
    }

    // let angles = asteroids_for_angle.keys().collect::<Vec<&i32>>();
    let mut angles: Vec<i32> = angles.into_iter().collect();
    angles.sort();
    angles.reverse();

    let mut nuked_count = 0;
    let mut part2 = Point { x: 0, y: 0 };

    while asteroids_for_angle.len() > 0 {
        for key in &angles {
            match asteroids_for_angle.get_mut(&key) {
                Some(item) => match item.pop() {
                    Some((_, p)) => {
                        nuked_count += 1;
                        if nuked_count == 200 {
                            part2 = p.clone();
                        }
                    }
                    None => {
                        asteroids_for_angle.remove_entry(&key);
                    }
                },
                None => {}
            }
            // asteroids_for_angle.remove(key);
        }
    }

    println!("part 1: {} ({}, {})", part1.0, part1.1.x, part1.1.y);
    println!("part 2: {:}", part2.x * 100 + part2.y);
}
