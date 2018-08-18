#!/usr/bin/env python
import os
import re
import json
import yaml
import jinja2

from .filters import crypt
from .functions import prompt, choice, path


def get_j2env(tmpldir):
    j2env = jinja2.Environment(
        loader = jinja2.FileSystemLoader(tmpldir),
        keep_trailing_newline = True,
        undefined = jinja2.StrictUndefined,
    )
    j2env.globals['env'] = os.environ.get
    j2env.filters['crypt'] = crypt
    return j2env


def get_context(tmpldir, outdir):
    saved = os.path.join(outdir, 'vars.yml')
    if os.path.exists(saved):
        with open(saved) as f:
            context = yaml.safe_load(f)
    else:
        env = get_j2env(tmpldir)
        template = env.get_template('vars.yml')
        rendered = template.render(prompt=prompt,
                                   choice=choice,
                                   path=path)
        with open(saved, 'w') as f:
            f.write(rendered)
        context = yaml.safe_load(rendered)
    return context


def get_files(tmpldir, context):
    env = get_j2env(tmpldir)
    template = env.get_template('files.yml')
    rendered = yaml.safe_load(template.render(**context))
    return rendered['files']


class File(object):
    def __init__(self, fobj):
        self.path = fobj['path']
        self.content = fobj['content']

    def _write(self, fd):
        return NotImplemented

    def write(self):
        dirname = os.path.dirname(self.path)
        if dirname:
            self.mkdir_p(dirname)
        with open(self.path, 'w') as f:
            self._write(f)

    @classmethod
    def mkdir_p(cls, path):
        os.makedirs(path, exist_ok=True)

    @classmethod
    def pick(cls, fobj):
        subcls = f'{fobj.get("format", "text").capitalize()}{cls.__name__}'
        for k in cls.__subclasses__():
            if k.__name__ == subcls:
                return k(fobj)
        else:
            raise RuntimeError(
                f'{cls.__name__} subclass named {subcls} is not defined'
            )


class TextFile(File):
    def _write(self, fd):
        fd.write(self.content)


class JsonFile(File):
    def _write(self, fd):
        json.dump(self.content, fd, indent=2)


def mkbuild(path, build):
    path = os.path.abspath(path)
    build = os.path.abspath(build)

    pwd = os.getcwd()
    try:
        File.mkdir_p(build)
        context = get_context(path, build)

        os.chdir(build)
        for fobj in get_files(path, context):
            File.pick(fobj).write()
    finally:
        os.chdir(pwd)
