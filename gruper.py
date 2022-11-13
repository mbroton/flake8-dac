from __future__ import annotations

import os
import re
import sys
import typing

from rich import print
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text


def get_rule_url(rule: str) -> str:
    return f'https://www.flake8rules.com/rules/{rule.upper()}.html'


def group(lines: list[str]) -> dict[str, list[str]]:
    data: dict[str, list[str]] = {}
    for line in lines:
        match = re.search(r'\d+\:\d+\:\s(\w\d{3})', line)
        if match:
            code = match.group(1)
            if code not in data:
                data[code] = []
            data[code].append(line)
    data = {
        k: v for k, v in sorted(
            data.items(), key=lambda item: len(item[1]), reverse=True,
        )
    }
    return data


def dac_print(data: dict[str, list[str]]) -> None:
    console = Console()
    sum = 0
    for code, matches in data.items():
        head = Text(f'> {code} ({len(matches)}) ')
        head.stylize('bold red', 2, 6)
        link = Text(get_rule_url(code))
        link.stylize('dim', 0, 50)
        console.rule(head + link, style='dim blue', align='left')

        aa = '\n'.join([m for m in matches])
        panel = Panel.fit(aa, border_style='dim blue')
        pad = Padding(panel, (1, 4))
        print(pad)
        sum += len(matches)
    print(f'Found {sum} problems')


def main(stream: typing.IO) -> int:
    is_pipe = not os.isatty(stream.fileno())
    if not is_pipe:
        print('no stdin')
        return 1

    groupped = group(stream.readlines())
    dac_print(groupped)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.stdin))
