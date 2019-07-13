# -*- coding: utf-8 -*-
import click
from click.testing import CliRunner

from efesto.App import App
from efesto.Blueprints import Blueprints
from efesto.Cli import Cli
from efesto.Tokens import Tokens
from efesto.Version import version
from efesto.models import Base, db

from peewee import OperationalError, ProgrammingError

from pytest import fixture, mark


@fixture
def quickstart(patch, magic):
    patch.object(Base, 'init_db')
    db.create_tables = magic()


@fixture
def runner():
    return CliRunner()


@fixture
def app(patch):
    patch.object(App, 'run')


def test_cli():
    message = ('An error occured during tables creation. '
               'Please check your database credentials.')
    assert Cli.installation_error == message


def test_cli_install(patch, runner):
    patch.object(click, 'echo')
    patch.object(App, 'install')
    result = runner.invoke(Cli.install)
    assert App.install.call_count == 1
    assert result.exit_code == 0


@mark.parametrize('error', [OperationalError, ProgrammingError])
def test_cli_install_error(patch, runner, error):
    patch.object(click, 'echo')
    patch.object(App, 'install', side_effect=ProgrammingError)
    result = runner.invoke(Cli.install)
    click.echo.assert_called_with(Cli.installation_error)
    assert result.exit_code == 1


def test_cli_token(patch, runner, app):
    patch.object(Tokens, 'encode')
    patch.object(click, 'echo')
    result = runner.invoke(Cli.token, ['user'])
    Tokens.encode.assert_called_with('secret', expiration=100, sub='user',
                                     aud='efesto')
    click.echo.assert_called_with(Tokens.encode())
    assert result.exit_code == 0


def test_cli_token_expiration(patch, runner, app):
    patch.object(Tokens, 'encode')
    result = runner.invoke(Cli.token, ['user', '200'])
    Tokens.encode.assert_called_with('secret', expiration=200, sub='user',
                                     aud='efesto')
    assert result.exit_code == 0


def test_cli_create_user(patch, runner):
    patch.object(App, 'create_user')
    result = runner.invoke(Cli.create_user, ['identifier'])
    App.create_user.assert_called_with('identifier', False)
    assert result.exit_code == 0


def test_cli_create_user__superuser(patch, runner):
    patch.object(App, 'create_user')
    result = runner.invoke(Cli.create_user, ['identifier', '--superuser'])
    App.create_user.assert_called_with('identifier', True)
    assert result.exit_code == 0


def test_cli_load_blueprint(patch, runner, quickstart):
    patch.object(Blueprints, 'load')
    runner.invoke(Cli.load_blueprint, ['filename'])
    Blueprints.load.assert_called_with('filename')
    assert Base.init_db.call_count == 1


def test_cli_version(patch, runner):
    patch.object(click, 'echo')
    runner.invoke(Cli.version, [])
    click.echo.assert_called_with('Version {}'.format(version))


def test_cli_run(app, runner):
    result = runner.invoke(Cli.run)
    assert App.run.call_count == 1
    assert result.exit_code == 0
