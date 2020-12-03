use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn run() -> (i32, i32) {
    let lines = read_lines("day1.txt").expect("Couldn't read day1.txt");

    let mut part1 = 0;
    let mut part2 = 0;

    for line in lines {
        let mass: i32 = line
            .expect("bad line")
            .trim()
            .parse()
            .expect("not a number");
        part1 += mass / 3 - 2;

        let mut fuel = mass / 3 - 2;

        while fuel > 0 {
            part2 += fuel;
            fuel = fuel / 3 - 2;
        }
    }

    return (part1, part2);
}

fn main() {
    match run() {
        (part1, part2) => {
            println!("part 1: {}", part1);
            println!("part 2: {}", part2);
        }
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn answers() {
        match run() {
            (part1, part2) => {
                assert_eq!(part1, 3219099);
                assert_eq!(part2, 4825810);
            }
        }
    }
}
