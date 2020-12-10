#!/usr/bin/env python

import re

required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

data = open('day4.txt').read()
passports = [dict(f.split(':') for f in re.split(r'\s+', p) if f) for p in re.split(r'\n\n+', data)]

def part1_is_valid(p):
    return required_fields.issubset(p.keys())

def part2_is_valid(p):
    if not required_fields.issubset(p.keys()):
        return False

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    if not (1920 <= int(p['byr']) <= 2002):
        return False

    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    if not (2010 <= int(p['iyr']) <= 2020):
        return False

    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if not (2020 <= int(p['eyr']) <= 2030):
        return False

    # hgt (Height) - a number followed by either cm or in:
    match = re.search(r'^(\d+)(cm|in)$', p['hgt'])
    if not match:
        return False

    # If cm, the number must be at least 150 and at most 193.
    if match.group(2) == 'cm' and not (150 <= int(match.group(1)) <= 193):
        return False

    # If in, the number must be at least 59 and at most 76.
    if match.group(2) == 'in' and not (59 <= int(match.group(1)) <= 76):
        return False

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if not re.search(r'^#[0-9a-f]{6}$', p['hcl']):
        return False

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if p['ecl'] not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
        return False

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    if not re.search(r'^\d{9}$', p['pid']):
        return False

    return True

print(f"part1: {len([p for p in passports if part1_is_valid(p)])}")
print(f"part2: {len([p for p in passports if part2_is_valid(p)])}")
