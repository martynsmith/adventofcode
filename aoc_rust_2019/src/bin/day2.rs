use aoc_rust_2019::intcode::IntCodeComputer;

fn main() {
    let template = IntCodeComputer::from_file("day2.txt");
    let mut computer = template.clone();
    computer.program[1] = 12;
    computer.program[2] = 2;
    computer.run();
    println!("part 1: {}", computer.program[0]);

    for noun in 0..100 {
        for verb in 0..100 {
            let mut computer = template.clone();
            computer.program[1] = noun;
            computer.program[2] = verb;
            computer.run();
            if computer.program[0] == 19690720 {
                println!("part 2: {}{}", noun, verb);
                std::process::exit(0);
            }
        }
    }
}
