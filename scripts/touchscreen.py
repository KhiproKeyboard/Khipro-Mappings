#!/usr/bin/env python3
"""M17N .mim to JSON converter - Touchscreen Adoption."""

import json
import re
import os
from collections import OrderedDict


def parse_mim_file(filename):
    result = OrderedDict()
    current_group = None
    in_map = False

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()

            if not line or line.startswith(';;'):
                continue

            stripped_line = line.strip()

            if stripped_line == '(map':
                in_map = True
                continue
            elif stripped_line.startswith('(state') or stripped_line.startswith('(init'):
                in_map = False
                current_group = None
                continue

            if not in_map:
                continue

            if stripped_line.startswith('(') and not stripped_line.startswith('("'):
                match = re.match(r'\((\w+)', stripped_line)
                if match:
                    group_name = match.group(1).upper()
                    if group_name == 'ONGKO':
                        current_group = None
                        continue
                    current_group = group_name
                    result[current_group] = OrderedDict()
                continue

            if current_group is None:
                continue

            for key, value in re.findall(r'\("([^"]+)"\s+"([^"]*)"\)', stripped_line):
                result[current_group][key] = value

    return result


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    input_file = os.path.join(repo_root, 'bn-khipro.mim')
    output_dir = os.path.join(repo_root, 'output')
    output_file = os.path.join(output_dir, 'touchscreen.json')

    os.makedirs(output_dir, exist_ok=True)

    mappings = parse_mim_file(input_file)

    if "BIRAM" in mappings:
        disallowed_biram = [".", "...", "..", "$", "$f", ".f", ".ff", "+", "-", "+f", "-f", "$$", "=", "=f"]
        mappings["BIRAM"] = OrderedDict(
            (k, v) for k, v in mappings["BIRAM"].items()
            if k not in disallowed_biram
        )
        mappings["BIRAM"]["।ff"] = "৺"

    if "DIACRITIC" in mappings:
        disallowed_diacritics = ["`", "``", "```", "``f"]
        mappings["DIACRITIC"] = OrderedDict(
            (k, v) for k, v in mappings["DIACRITIC"].items()
            if k not in disallowed_diacritics
        )

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, ensure_ascii=False, indent=2)

    print(f"-> {output_file}")


if __name__ == '__main__':
    main()
