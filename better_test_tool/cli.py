import click
import pyperclip

from better_test_tool.launchers import NoseTestsLauncher, PytestLauncher
from better_test_tool.parser import ParserTests
from better_test_tool.utils import get_version


def copy_to_clipboard(result):
    click.secho('Copied to clipboard', fg='blue')
    pyperclip.copy(result)


@click.group()
@click.version_option(version=get_version())
def cli():
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def parse(path):
    file_parser = ParserTests()
    try:
        files_number = file_parser.parse(path)
    except ValueError as error:
        click.secho(str(error), fg='red')
        return
    else:
        click.secho('Parsing completed. Found {} files.'.format(files_number), fg='green')


@cli.command()
@click.argument('path')
@click.option('-m', '--method')
@click.option('-cp', '--copy', is_flag=True)
def nosetests(path, method, copy):
    nose_launcher = NoseTestsLauncher()
    result = nose_launcher.generate(path, method)
    if copy:
        copy_to_clipboard(result)

    click.echo(result)


@cli.command()
@click.argument('path')
@click.option('-m', '--method')
@click.option('-cp', '--copy', is_flag=True)
def pytest(path, method, copy):
    pytest_launcher = PytestLauncher()
    result = pytest_launcher.generate(path, method)
    if copy:
        copy_to_clipboard(result)

    click.echo(result)
