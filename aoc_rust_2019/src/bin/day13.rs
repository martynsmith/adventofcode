use aoc_rust_2019::intcode::IntCodeComputer;

fn main() {
    let mut part1_icc = IntCodeComputer::from_file("day13.txt");
    let mut part2_icc = part1_icc.clone();
    let mut part1 = 0;
    part1_icc.run();
    while part1_icc.has_output() {
        part1_icc.get_output();
        part1_icc.get_output();
        if part1_icc.get_output() == 2 {
            part1 += 1;
        }
    }
    println!("part 1: {}", part1);

    part2_icc.program[0] = 2;
    let mut paddle_x = 0;
    let mut ball_x = 0;
    let mut part2 = 0;
    while !part2_icc.halted {
        part2_icc.run();
        while part2_icc.has_output() {
            let x = part2_icc.get_output();
            let y = part2_icc.get_output();
            let v = part2_icc.get_output();
            if v == 3 {
                paddle_x = x;
            }
            if v == 4 {
                ball_x = x;
            }
            if x == -1 && y == 0 {
                part2 = v;
            }
        }
        if paddle_x < ball_x {
            part2_icc.add_input(1);
        } else if paddle_x > ball_x {
            part2_icc.add_input(-1);
        } else {
            part2_icc.add_input(0);
        }
    }
    println!("part 2: {}", part2);
}
