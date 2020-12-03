use aoc_rust_2019::intcode::IntCodeComputer;

fn main() {
    let mut part1 = IntCodeComputer::from_file("day9.txt");
    let mut part2 = part1.clone();

    part1.add_input(1);
    part1.run();
    println!("part 1: {}", part1.get_output());

    part2.add_input(2);
    part2.run();
    println!("part 2: {}", part2.get_output());
}
