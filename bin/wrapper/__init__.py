#!/usr/bin/env python
import os
import re
import json
import yaml
import glob
import jinja2
import string
import secrets
import getpass
import textwrap

from passlib.hash import sha512_crypt


@jinja2.contextfunction
def anchor(ctx, value):
    if value not in ctx.parent['refs']:
        ctx.parent['refs'].append(value)
    return f'*{value}'


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


random = secrets.SystemRandom()


def crypt(password, salt=None, rounds=5000):
    if salt is None:
        salt = ''.join(random.choices(string.digits + string.ascii_letters, k=16))
    return sha512_crypt.hash(password, salt=salt, rounds=rounds)


FUNCTIONS = {
    'id': anchor,
    'prompt': prompt,
    'choice': choice,
    'path': path,
}


def render_yaml(path):
    env = jinja2.Environment(
            loader = jinja2.FileSystemLoader(os.path.dirname(path)),
            keep_trailing_newline = True,
            undefined = jinja2.StrictUndefined,
    )
    env.globals['env'] = os.environ.get
    env.globals['refs'] = []
    env.filters['crypt'] = crypt

    template = env.get_template(os.path.basename(path))
    output = template.render(**FUNCTIONS)

    for ref in env.globals['refs']:
        output = re.sub(r'^( *)({0}):(?! [&\*]{0})(.*)?$'.format(ref),
                        r'\1\2: &\2\3', output, count=1, flags=re.M)

    return yaml.safe_load(output)


class TemplateFile(object):
    def __init__(self, config):
        self.config = config
        self.path = self.config['file']['path']

    def write(self):
        dirname = os.path.dirname(self.path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(self.path, 'w') as fd:
            self._write(fd)

    def _write(self):
        return NotImplemented

    @classmethod
    def pick(cls, config):
        for k in cls.__subclasses__():
            if k.__name__.startswith(config['file']['format'].capitalize()):
                return k(config)
        else:
            raise RuntimeError('Cannot find a TemplateFile class matching the given format.')


class JsonTemplateFile(TemplateFile):
    def _write(self, fd):
        json.dump(self.config['file']['data'], fd, indent=2)


# FIXME: all of the original yaml config should be within jinja2 raw blocks
#        except for user input, and then handling of those variables should be separated here.
class TextTemplateFile(TemplateFile):
    def _write(self, fd):
        template = jinja2.Template(self.config['file']['content'])
        fd.write(template.render(vars=self.config['vars']))


def create_build_dir(config):
    name = config['vars']['name']

    pwd = os.getcwd()
    try:
        os.makedirs(f'build/{name}', exist_ok=True)
        os.chdir(f'build/{name}')

        for fobj in config['files']:
            usercfg = {'vars': config['vars']}
            usercfg.update({'file': fobj})
            TemplateFile.pick(usercfg).write()
    finally:
        os.chdir(pwd)
