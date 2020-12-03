use std::collections::HashMap;

fn count_orbits(body: &str, central_body_for: &HashMap<&str, &str>) -> i32 {
    match central_body_for.get(body) {
        Some(central_body) => 1 + count_orbits(central_body, central_body_for),
        None => 0,
    }
}

fn main() {
    let source = std::fs::read_to_string("day6.txt").expect("Couldn't read input file");
    let mut central_body_for: HashMap<&str, &str> = HashMap::new();

    for line in source.trim().split("\n") {
        let planets: Vec<&str> = line.trim().split(")").collect();
        central_body_for.insert(planets[1], planets[0]);
    }

    let mut part1 = 0;

    for body in central_body_for.keys() {
        part1 += count_orbits(body, &central_body_for);
    }

    println!("part 1: {:?}", part1);

    // First we'll build a map of all the bodies YOU can reach if you just keep
    // going more central
    let mut you_steps_to: HashMap<&str, i32> = HashMap::new();
    let mut you = "YOU";
    let mut step = 0;
    while central_body_for.contains_key(you) {
        match central_body_for.get(you) {
            Some(y) => {
                you_steps_to.insert(y, step);
                you = y;
                step += 1;
            }
            None => {}
        }
    }

    // Now we we walk SAN towards the center looking for any common path with
    // YOU. When we find it, we can just add them together to get the total
    // distance.
    let mut san = "SAN";
    let mut step = 0;
    while central_body_for.contains_key(san) {
        match you_steps_to.get(san) {
            Some(you_steps) => {
                println!("part 2: {}", step + you_steps - 1);
                break;
            }
            None => {}
        }
        match central_body_for.get(san) {
            Some(s) => {
                san = s;
                step += 1;
            }
            None => {}
        }
    }
}
