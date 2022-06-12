#! /usr/bin/env python3

import re
import shutil
import subprocess
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from contextlib import contextmanager
from inspect import cleandoc
from os import chdir, getcwd, mkdir
from types import SimpleNamespace


def run(*command: str) -> None:
    """
    Run a command and ensure it is successful.

    Args:
        *command: The command to run.
    """
    subprocess.run(command, check=True)


@contextmanager
def cd(destination: str) -> None:
    """
    Change the current working directory to the specified one within the yielded context.

    Args:
        destination: The directory to cd into.
    """
    current_working_directory = getcwd()

    try:
        chdir(destination)
        yield
    finally:
        chdir(current_working_directory)


@contextmanager
def commit(message: str) -> None:
    """
    Commit (git) any changes that occur within the yielded context.

    Args:
        message (str): The commit message.
    """
    yield

    run('git', 'add', '.')
    run('git', 'commit', '--message', message)


def match_and_replace(matchers_and_replacers: dict[str, str], file: str) -> None:
    """
    Match and replace regexes with the provided string - in the specified file.

    Args:
        matchers_and_replacers: A dict containing the regex to match as its keys, and the replacement string as its
                                values.
        file: The file name.
    """
    with open(file) as stream:
        contents = stream.read()

        for match, replace in matchers_and_replacers.items():
            contents = re.sub(match, replace, contents)

    with open(file, 'w') as stream:
        stream.write(contents)


def create_file(name: str, content: str) -> None:
    """
    Create a file with the specified contents.

    Args:
        name: Filename.
        content: File contents.
    """
    with open(name, 'w') as stream:
        stream.write(f"{cleandoc(content)}\n")


if __name__ == '__main__':
    parser = namedtuple('Parser', ('main', 'subparser', 'subparsers'))(
        (main := ArgumentParser(
            prog='vue3-vite-setup',
            description='A script to setup an opinionated vue3/vite project.',
            allow_abbrev=False
        )),
        main.add_subparsers(title='Action', description='The action to take.', dest='action', required=True),
        SimpleNamespace()
    )

    # create
    parser.subparsers.create = parser.subparser.add_parser(
        'create', description='Create a new project.', add_help=True, allow_abbrev=False)

    parser.subparsers.create.add_argument('name', help="The project's name.")

    arguments: Namespace = parser.main.parse_args()

    match arguments.action:
        case 'create':
            run('yarn', 'create', 'vite', '--template', 'vue-ts', arguments.name)

            with cd(arguments.name):
                with commit('feat: initial commit'):
                    run('git', 'init')

                run('git', 'branch', 'develop')
                run('git', 'checkout', 'develop')

                with commit('fix: install dependencies'):
                    run('yarn')

                with commit('chore: add '
                            'eslint, @typescript-eslint/eslint-plugin, @typescript-eslint/parser, '
                            'eslint-plugin-vue, vue-eslint-parser'):
                    run('yarn', 'add', '--dev', 'eslint', '@typescript-eslint/eslint-plugin@latest',
                        '@typescript-eslint/parser@latest', 'eslint-plugin-vue@latest', 'vue-eslint-parser')

                with commit('chore: configure eslint'):
                    create_file('.eslintrc.js', '''
                        module.exports = {
                            env: {
                                browser: true,
                                es2021: true,
                                node: true,
                            },
                            extends: [
                                "eslint:recommended",
                                "plugin:vue/vue3-recommended",
                                "plugin:@typescript-eslint/recommended",
                            ],
                            parser: "vue-eslint-parser",
                            parserOptions: {
                                ecmaVersion: "latest",
                                parser: "@typescript-eslint/parser",
                                sourceType: "module",
                            },
                            plugins: ["vue", "@typescript-eslint"],
                            rules: {},
                        };
                        ''')

                with commit('chore: add prettier, eslint-config-prettier'):
                    run('yarn', 'add', '--dev', '--exact', 'prettier')
                    run('yarn', 'add', '--dev', 'eslint-config-prettier')

                with commit('chore: configure prettier'):
                    create_file('.prettierrc.json', '{}')

                    match_and_replace({r'extends: \[([\S\s]*?),\s*\]': r'extends: [\1, "prettier"]'}, '.eslintrc.js')

                with commit('chore: setup lint-staged (w/ husky)'):
                    run('npx', 'mrm@2', 'lint-staged')

                with commit('chore: configure lint-staged'):
                    create_file('.lintstagedrc.json', '''
                        {
                            "*.{js,ts,vue}": "eslint --cache --fix",
                            "*.{js,ts,vue,json,html,md,css}": "prettier --write"
                        }
                        ''')

                    match_and_replace({r',\s*"lint-staged": {[\S\s]*?}\n': '\n'}, 'package.json')

                    with open('.gitignore', 'a') as stream:
                        stream.write('\n# eslint\n.eslintcache\n')

                    with cd('.husky'):
                        match_and_replace({'npx lint-staged': 'yarn run lint-staged'}, 'pre-commit')

                with commit('fix: lint & format'):
                    run('yarn', 'run', 'eslint', '--ext', '.js,.ts,.vue', '--ignore-path', '.gitignore', '--fix', '.')
                    run('yarn', 'run', 'prettier', '--ignore-path', '.gitignore', '--write', '.')

                with commit('fix: general cleanup'):
                    with cd('.vscode'):
                        match_and_replace({'Vue.volar': 'johnsoncodehk.volar'}, 'extensions.json')

                    match_and_replace({'id="app"': 'id="application"'}, 'index.html')

                    with cd('src'):
                        match_and_replace({'#app': '#application'}, 'main.ts')

                    match_and_replace(
                        {'<title>Vite App</title>': f"<title>{arguments.name.replace('-', ' ').title()}</title>"},
                        'index.html')

                    create_file('README.md', f'''
                        # {arguments.name}

                        Hello, world!
                        ''')

                    match_and_replace({r'\s*"jsx": "preserve",': '', re.escape(' "src/**/*.tsx",'): ''},
                                      'tsconfig.json')

                    match_and_replace({'//.*': ''}, 'vite.config.ts')

                    with cd('src'):
                        shutil.rmtree('assets')
                        shutil.rmtree('components')

                        create_file('App.vue', '<template>Hello, world!</template>')

                with commit('chore: add vitest, happy-dom, @vue/test-utils'):
                    run('yarn', 'add', '--dev', 'vitest', 'happy-dom', '@vue/test-utils@next')

                with commit('fix: configure vitest'):
                    with open('vite.config.ts', 'r+') as stream:
                        contents = stream.read()
                        stream.seek(0)
                        stream.write(f'/// <reference types="vitest" />\n\n{contents}')

                    match_and_replace({r'plugins: \[(.*)\]': r"plugins: [\1], test: {environment: 'happy-dom'}"},
                                      'vite.config.ts')

                    with cd('src'):
                        create_file('App.spec.ts', '''
                            import { describe, expect, it } from "vitest";
                            import { mount } from "@vue/test-utils";
                            import App from "./App.vue";

                            describe("App.vue", () => {
                              it("can render the application text", () => {
                                const wrapper = mount(App);

                                expect(wrapper.text()).toBe("Hello, world!");
                              });
                            });
                            ''')

                with commit('chore: add cypress'):
                    run('yarn', 'add', '--dev', 'cypress')

                with commit('chore: configure cypress'):
                    mkdir('cypress')
                    with cd('cypress'):
                        create_file('tsconfig.json', '''
                            {
                              "compilerOptions": {
                                "target": "esnext",
                                "lib": ["esnext", "dom"],
                                "types": ["cypress"]
                              },
                            "include": ["**/*.ts"]
                            }
                            ''')

                        mkdir('integration')
                        with cd('integration'):
                            create_file('example.test.ts', '''
                                describe("An Example Test", () => {
                                    it("runs a test", () => {
                                        cy.visit("/");
                                        cy.get("body").should("contain.text", "Hello, world!");
                                    });
                                });
                                ''')

                    create_file('cypress.json', '''
                        {
                            "baseUrl": "http://localhost:4173"
                        }
                        ''')

                with commit('metadata: add test scripts'):
                    match_and_replace(
                        {'"preview": (.*?),': r'"preview": \1, "test:unit": "vitest", "test:e2e": "cypress open",'},
                        'package.json')

                with commit('chore: add tailwindcss, postcss, autoprefixer'):
                    run('yarn', 'add', '--dev', 'tailwindcss', 'postcss', 'autoprefixer')

                with commit('chore: generate tailwindcss configuration'):
                    run('yarn', 'run', 'tailwindcss', 'init', '-p')

                with commit('chore: configure: tailwindcss'):
                    match_and_replace({r'content: \[]': 'content: ["./index.html", "./src/**/*.{vue,js,ts}"]'},
                                      'tailwind.config.js')

                    with cd('src'):
                        create_file('index.css', '''
                            @tailwind base;
                            @tailwind components;
                            @tailwind utilities;
                            ''')

                        match_and_replace({'(import App from "./App.vue");': r'\1; import "./index.css";'}, 'main.ts')
