use aoc_rust_2019::intcode::IntCodeComputer;

fn main() {
    let mut p1computer = IntCodeComputer::from_file("day5.txt");
    let mut p2computer = p1computer.clone();

    p1computer.add_input(1);
    p1computer.run();
    let mut part1 = 0;
    loop {
        match p1computer.get_maybe_output() {
            Some(value) => part1 = value,
            None => break,
        }
    }
    println!("part 1: {}", part1);

    p2computer.add_input(5);
    p2computer.run();
    let mut part2 = 0;
    loop {
        match p2computer.get_maybe_output() {
            Some(value) => part2 = value,
            None => break,
        }
    }
    println!("part 2: {}", part2);
}
