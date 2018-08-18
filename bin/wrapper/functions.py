#!/usr/bin/env python
import os
import glob
import getpass
import textwrap


def prompt(message, default='', secret=False):
    extra = '>>> '
    if default:
        extra = f'[{default}] ' + extra
    message = f'{message} {extra}'

    if secret:
        _ask = getpass.getpass
    else:
        _ask = input

    answer = _ask(message).strip()
    return answer if answer else default


def choice(message, choices, default=''):
    items = '\n'.join([f'{i}: {item}' for i, item in enumerate(choices, 1)])
    try:
        answer = int(prompt(f"{message}\n{textwrap.indent(items, '  ')}\n", default=default))
        return choices[int(answer) - 1]
    except (ValueError, IndexError):
        print('ERROR: invalid selection!')
        return choice(message, choices, default)


def path(message, pattern='*.*', default='', recurse=False, always=False):
    matches = glob.glob(pattern, recursive=recurse)
    if not matches:
        raise ValueError(f'No files matching pattern {pattern}')
    if len(matches) == 1 and not always:
        answer = matches[0]
    else:
        answer = choice(message, glob.glob(pattern, recursive=recurse), default)
    return os.path.abspath(answer)

