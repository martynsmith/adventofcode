extern crate itertools;

use itertools::Itertools;

use aoc_rust_2019::intcode::IntCodeComputer;

fn main() {
    let template = IntCodeComputer::from_file("day7.txt");

    let phase_permutations = (0i64..5).permutations(5);
    let mut part1 = 0;

    for phases in phase_permutations {
        let mut amps = [
            template.clone(),
            template.clone(),
            template.clone(),
            template.clone(),
            template.clone(),
        ];
        let mut signal = 0;
        for (phase, amp) in phases.iter().zip(amps.iter_mut()) {
            amp.add_input(*phase);
            amp.add_input(signal);
            amp.run();
            signal = amp.get_output()
        }
        if signal > part1 {
            part1 = signal;
        }
    }

    println!("part 1: {}", part1);

    let phase_permutations = (5i64..10).permutations(5);
    let mut part2 = 0;

    for phases in phase_permutations {
        let mut amps = [
            template.clone(),
            template.clone(),
            template.clone(),
            template.clone(),
            template.clone(),
        ];
        let mut signal = 0;
        for (phase, amp) in phases.iter().zip(amps.iter_mut()) {
            amp.add_input(*phase);
        }
        let mut amps_iter = amps.iter_mut().peekable();
        while let Some(amp) = amps_iter.next() {
            if amp.halted {
                break;
            }

            amp.add_input(signal);
            amp.run();
            signal = amp.get_output();

            if amps_iter.peek().is_none() {
                amps_iter = amps.iter_mut().peekable();
            }
        }
        if signal > part2 {
            part2 = signal;
        }
    }

    println!("part 2: {}", part2);
}
