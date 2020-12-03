use aoc_rust_2019::intcode::IntCodeComputer;
use std::collections::HashMap;

fn paint(canvas: &mut HashMap<(i32, i32), i64>, icc: &mut IntCodeComputer) {
    let mut direction = (0, -1);
    let mut position = (0, 0);

    while !icc.halted {
        icc.add_input(match canvas.get(&position) {
            Some(colour) => *colour,
            None => 0,
        });
        icc.run();
        canvas.insert(position, icc.get_output());
        direction = match icc.get_output() {
            0 => {
                if direction.0 == 0 {
                    (direction.1, 0)
                } else {
                    (0, -direction.0)
                }
            }
            1 => {
                if direction.0 == 0 {
                    (-direction.1, 0)
                } else {
                    (0, direction.0)
                }
            }
            _ => panic!("invalid direction output"),
        };
        position = (position.0 + direction.0, position.1 + direction.1);
    }
}

fn main() {
    let mut p1_icc = IntCodeComputer::from_file("day11.txt");
    let mut p2_icc = p1_icc.clone();
    let mut p1_canvas = HashMap::<(i32, i32), i64>::new();
    let mut p2_canvas = HashMap::<(i32, i32), i64>::new();

    paint(&mut p1_canvas, &mut p1_icc);
    println!("part 1: {}", p1_canvas.len());

    p2_canvas.insert((0, 0), 1);
    paint(&mut p2_canvas, &mut p2_icc);

    let min_x = p2_canvas.keys().map(|k| k.0).min().unwrap();
    let max_x = p2_canvas.keys().map(|k| k.0).max().unwrap();
    let min_y = p2_canvas.keys().map(|k| k.1).min().unwrap();
    let max_y = p2_canvas.keys().map(|k| k.1).max().unwrap();

    for y in min_y..max_y + 1 {
        for x in min_x..max_x + 1 {
            print!(
                "{}",
                match p2_canvas.get(&(x, y)) {
                    Some(v) => {
                        match v {
                            1 => "█",
                            _ => " ",
                        }
                    }
                    None => " ",
                }
            );
        }
        println!("");
    }
}
