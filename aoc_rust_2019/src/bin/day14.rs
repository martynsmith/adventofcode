extern crate regex;
use regex::Regex;

use std::collections::{HashMap, HashSet, VecDeque};

#[derive(Debug)]
struct Chemical<'a> {
    quantity: u64,
    label: &'a str,
}

impl<'a> Chemical<'a> {
    fn new(quantity: u64, label: &'a str) -> Chemical {
        Chemical {
            quantity: quantity,
            label: label,
        }
    }
}

#[derive(Debug)]
struct Reaction<'a> {
    resulting_quantity: u64,
    source_chemicals: Vec<Chemical<'a>>,
}

fn calculate_deps<'a>(
    label: &'a str,
    reaction_for: &'a HashMap<&str, Reaction>,
) -> HashSet<&'a str> {
    match reaction_for.get(label) {
        Some(reaction) => {
            let mut deps = HashSet::new();
            for c in &reaction.source_chemicals {
                if c.label == "ORE" {
                    continue;
                }
                deps.insert(c.label);
                let subdeps = calculate_deps(c.label, reaction_for);
                deps.extend(subdeps);
            }
            deps
        }
        None => panic!("bad label: {}", label),
    }
}

fn ore_required(
    fuel: u64,
    reaction_for: &HashMap<&str, Reaction>,
    ordered_labels: &VecDeque<&str>,
) -> u64 {
    let mut need: HashMap<&str, u64> = HashMap::new();
    need.insert("FUEL", fuel);

    for label in ordered_labels {
        let required = match need.get(label) {
            Some(quantity) => *quantity,
            None => 0,
        };
        let get_per_reaction = match reaction_for.get(label) {
            Some(reaction) => reaction.resulting_quantity,
            None => panic!("Nope"),
        };
        for source in &reaction_for.get(label).unwrap().source_chemicals {
            let mut existing = match need.get_mut(source.label) {
                Some(quantity) => *quantity,
                None => 0,
            };

            let reaction_count = ((required as f64) / (get_per_reaction as f64)).ceil();
            existing += (reaction_count as u64) * source.quantity;

            need.insert(source.label, existing);
        }
        need.remove(label);
    }

    match need.get("ORE") {
        Some(q) => *q,
        None => 0,
    }
}

fn main() {
    let re = Regex::new(r"(\d+) (\w+)").unwrap();
    let lines = std::fs::read_to_string("day14.txt").expect("Couldn't ready day14.txt");

    let mut reaction_for: HashMap<&str, Reaction> = HashMap::new();

    for line in lines.trim().split("\n") {
        let mut ic = Vec::<Chemical>::new();
        for cap in re.captures_iter(line) {
            ic.push(Chemical::new(
                cap[1].parse().unwrap(),
                cap.get(2).unwrap().as_str(),
            ));
        }
        match ic.pop() {
            Some(target) => {
                reaction_for.insert(
                    target.label,
                    Reaction {
                        resulting_quantity: target.quantity,
                        source_chemicals: ic,
                    },
                );
            }
            None => panic!("Nope"),
        }
    }

    let mut deps_for: HashMap<&str, HashSet<&str>> = HashMap::new();

    for label in reaction_for.keys() {
        deps_for.insert(label, calculate_deps(label, &reaction_for));
    }

    let mut to_order: HashSet<&str> = HashSet::new();
    for label in deps_for.keys() {
        to_order.insert(*label);
    }

    let mut ordered: VecDeque<&str> = VecDeque::new();
    let mut ordered_set: HashSet<&str> = HashSet::new();

    while to_order.len() > 0 {
        for label in to_order.clone() {
            if deps_for.get(label).unwrap().is_subset(&ordered_set) {
                to_order.remove(label);
                ordered.push_front(label);
                ordered_set.insert(label);
                break;
            }
        }
    }

    println!("part 1: {}", ore_required(1, &reaction_for, &ordered));

    // binary search for part 2
    let target_ore = 1000000000000;
    let mut min_fuel = 1;
    let mut max_fuel = target_ore;

    while max_fuel - min_fuel > 1 {
        let new_fuel = min_fuel + (max_fuel - min_fuel) / 2;
        if ore_required(new_fuel, &reaction_for, &ordered) < target_ore {
            min_fuel = new_fuel;
        } else {
            max_fuel = new_fuel;
        }
    }

    println!("part 2: {}", min_fuel);
}
