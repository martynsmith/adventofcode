pub mod intcode {
    use std::collections::VecDeque;
    use std::fs::File;
    use std::io::prelude::*;
    use std::io::BufReader;

    #[derive(Debug, Clone)]
    pub struct IntCodeComputer {
        pub program: Vec<i64>,
        pub pointer: i64,
        input: VecDeque<i64>,
        output: VecDeque<i64>,
        pub halted: bool,
        relative_base: i64,
    }

    impl IntCodeComputer {
        pub fn new(program: Vec<i64>) -> IntCodeComputer {
            IntCodeComputer {
                program,
                pointer: 0,
                input: VecDeque::new(),
                output: VecDeque::new(),
                halted: false,
                relative_base: 0,
            }
        }

        pub fn from_file(filename: &str) -> IntCodeComputer {
            let file = File::open(filename).expect("Error opening file");
            let mut reader = BufReader::new(file);
            let mut input = String::new();
            reader.read_line(&mut input).expect("Couldn't read file");
            let program: Vec<i64> = input
                .trim()
                .split(",")
                .map(|op| op.parse().unwrap())
                .collect();
            return IntCodeComputer::new(program);
        }

        pub fn add_input(&mut self, value: i64) {
            self.input.push_back(value)
        }

        pub fn get_output(&mut self) -> i64 {
            match self.output.pop_front() {
                Some(output) => output,
                None => panic!("no output!"),
            }
        }

        pub fn get_maybe_output(&mut self) -> Option<i64> {
            self.output.pop_front()
        }

        pub fn has_output(&self) -> bool {
            self.output.len() > 0
        }

        fn grow_self(&mut self, location: usize) {
            if location + 1 > self.program.len() {
                self.program.resize(location + 1, 0);
            }
        }

        fn get_param(&mut self, opvalue: i64, param_number: i64) -> i64 {
            let mode = opvalue / (10i64.pow((param_number as u32) + 1)) % 10;
            match mode {
                0 => {
                    let location = (self.pointer + param_number) as usize;
                    self.grow_self(location);
                    let location = self.program[location] as usize;
                    self.grow_self(location);
                    return self.program[location];
                }
                1 => {
                    let location = (self.pointer + param_number) as usize;
                    self.grow_self(location);
                    return self.program[location];
                }
                2 => {
                    let location = (self.pointer + param_number) as usize;
                    self.grow_self(location);
                    let location = (self.relative_base + self.program[location]) as usize;
                    self.grow_self(location);
                    return self.program[location];
                }
                _ => {
                    panic!("Unknown param mode: {}", mode);
                }
            }
        }

        fn set_param(&mut self, opvalue: i64, param_number: u32, value: i64) {
            let mode = opvalue / (10i64.pow(param_number + 1)) % 10;
            match mode {
                0 => {
                    let write_location =
                        self.program[(self.pointer + (param_number as i64)) as usize] as usize;

                    if write_location + 1 > self.program.len() {
                        self.program.resize(write_location + 1, 0);
                    }

                    self.program[write_location] = value
                }
                2 => {
                    let write_location = (self.relative_base
                        + self.program[(self.pointer + (param_number as i64)) as usize])
                        as usize;

                    if write_location + 1 > self.program.len() {
                        self.program.resize(write_location + 1, 0);
                    }

                    self.program[write_location] = value
                }
                _ => {
                    panic!("Unknown param mode: {}", mode);
                }
            }
        }

        pub fn run(&mut self) {
            if self.halted {
                panic!("trying to run halted intcode computer");
            }
            loop {
                let pointer = self.pointer as usize;
                let opvalue = self.program[pointer];
                let opcode = opvalue % 100;
                match opcode {
                    1 => {
                        let p1 = self.get_param(opvalue, 1);
                        let p2 = self.get_param(opvalue, 2);
                        self.set_param(opvalue, 3, p1 + p2);
                        self.pointer += 4;
                    }
                    2 => {
                        let p1 = self.get_param(opvalue, 1);
                        let p2 = self.get_param(opvalue, 2);
                        self.set_param(opvalue, 3, p1 * p2);
                        self.pointer += 4;
                    }
                    3 => {
                        match self.input.pop_front() {
                            Some(value) => {
                                self.set_param(opvalue, 1, value);
                            }
                            None => return,
                        }
                        self.pointer += 2;
                    }
                    4 => {
                        let value = self.get_param(opvalue, 1);
                        self.output.push_back(value);
                        self.pointer += 2;
                    }
                    5 => {
                        if self.get_param(opvalue, 1) != 0 {
                            self.pointer = self.get_param(opvalue, 2);
                        } else {
                            self.pointer += 3;
                        }
                    }
                    6 => {
                        if self.get_param(opvalue, 1) == 0 {
                            self.pointer = self.get_param(opvalue, 2);
                        } else {
                            self.pointer += 3;
                        }
                    }
                    7 => {
                        if self.get_param(opvalue, 1) < self.get_param(opvalue, 2) {
                            self.set_param(opvalue, 3, 1);
                        } else {
                            self.set_param(opvalue, 3, 0);
                        }
                        self.pointer += 4;
                    }
                    8 => {
                        if self.get_param(opvalue, 1) == self.get_param(opvalue, 2) {
                            self.set_param(opvalue, 3, 1);
                        } else {
                            self.set_param(opvalue, 3, 0);
                        }
                        self.pointer += 4;
                    }
                    9 => {
                        self.relative_base += self.get_param(opvalue, 1);
                        self.pointer += 2;
                    }
                    99 => {
                        self.halted = true;
                        return;
                    }
                    _ => {
                        panic!("Unknown opcode: {}", opcode);
                    }
                }
            }
        }
    }
}
