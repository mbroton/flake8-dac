from __future__ import annotations

import contextlib
import io

import gruper


def test_valid_stdin():
    with contextlib.ExitStack() as stack:
        inp = stack.enter_context(open('tests/data/input_valid.txt'))

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            d = gruper.group(inp.readlines())
            gruper.dac_print(d)

        model = stack.enter_context(open('tests/data/output_valid.txt'))
        assert out.getvalue() == ''.join(model.readlines())


def test_stdin_with_no_matches():
    with contextlib.ExitStack() as stack:
        inp = stack.enter_context(open('tests/data/input_no_matches.txt'))

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            d = gruper.group(inp.readlines())
            gruper.dac_print(d)

        assert out.getvalue() == 'Found 0 problems\n'


def test_get_rule_url():
    url = gruper.get_rule_url('G123')
    expected = 'https://www.flake8rules.com/rules/G123.html'
    assert url == expected


def test_groupping_and_sorting():
    inp = """../path/path.py:16:80: E501 line too long (93 > 79 characters)
../path/path/path.py:21:1: W293 blank line contains whitespace
../path/path/path.py:28:39: W292 no newline at end of file
../path/path/path/path/path.py:28:1: W293 blank line contains whitespace"""
    out = {
        'E501': [
            '../path/path.py:16:80: E501 line too long (93 > 79 characters)',
        ],
        'W293': [
            '../path/path/path.py:21:1: W293 blank line contains whitespace',
            '../path/path/path/path/path.py:28:1: W293 blank line contains whitespace',
        ],
        'W292': [
            '../path/path/path.py:28:39: W292 no newline at end of file',
        ],
    }
    out = {
        k: v for k, v in sorted(
            out.items(), key=lambda item: len(item[1]), reverse=True,
        )
    }
    actual = gruper.group(inp.splitlines())
    assert actual == out
    assert list(actual) == list(out)
