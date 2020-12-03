const WIDTH: u8 = 25;
const HEIGHT: u8 = 6;
const LAYER_SIZE: usize = (WIDTH * HEIGHT) as usize;

fn main() {
    let source = std::fs::read_to_string("day8.txt").expect("couldn't read input file");

    let mut src = source.as_str();
    let mut min_zeros = LAYER_SIZE;
    let mut part1 = 0;
    let mut part2 = vec![2; LAYER_SIZE];

    while src.len() > LAYER_SIZE {
        let (layer, remaining) = src.split_at(LAYER_SIZE);
        src = remaining;

        // part1
        let layer_counts = layer.bytes().fold((0, 0, 0), |(c0, c1, c2), v| match v {
            48 => (c0 + 1, c1, c2),
            49 => (c0, c1 + 1, c2),
            50 => (c0, c1, c2 + 1),
            10 => (c0, c1, c2),
            _ => panic!("invalid number: {}", v),
        });
        if layer_counts.0 < min_zeros {
            min_zeros = layer_counts.0;
            part1 = layer_counts.1 * layer_counts.2;
        }

        // part2
        for (index, value) in layer.bytes().enumerate() {
            if part2[index] != 2 {
                continue;
            }
            match value {
                48 => part2[index] = 0,
                49 => part2[index] = 1,
                _ => {}
            }
        }
    }

    println!("part 1: {}", part1);
    println!("part 2:");
    for y in 0..HEIGHT {
        for x in 0..WIDTH {
            print!(
                "{}",
                match part2[(x + y * WIDTH) as usize] {
                    1 => '█',
                    _ => ' ',
                }
            );
        }
        println!("");
    }
}
