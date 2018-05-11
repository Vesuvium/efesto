# -*- coding: utf-8 -*-
import click
from click.testing import CliRunner

from efesto.App import App
from efesto.Blueprints import Blueprints
from efesto.Cli import Cli
from efesto.Tokens import Tokens
from efesto.models import Base, Fields, Types, Users, db

from peewee import OperationalError, ProgrammingError

from pytest import fixture


@fixture
def quickstart(patch):
    patch.object(Base, 'init_db')
    patch.object(db, 'create_tables')


@fixture
def runner():
    return CliRunner()


@fixture
def app(patch):
    patch.object(App, 'run')


def test_quickstart(runner, quickstart):
    result = runner.invoke(Cli.quickstart)
    assert Base.init_db.call_count == 1
    db.create_tables.assert_called_with([Fields, Types, Users])
    assert result.exit_code == 0


def test_quickstart_operational_error(runner, quickstart):
    db.create_tables.side_effect = OperationalError
    result = runner.invoke(Cli.quickstart)
    assert result.exit_code == 1


def test_quickstart_programming_error(runner, quickstart):
    db.create_tables.side_effect = ProgrammingError
    result = runner.invoke(Cli.quickstart)
    assert result.exit_code == 1


def test_cli_token(patch, runner, app):
    patch.object(Tokens, 'encode')
    patch.object(click, 'echo')
    result = runner.invoke(Cli.token, ['user'])
    Tokens.encode.assert_called_with('secret', expiration=100, sub='user')
    click.echo.assert_called_with(Tokens.encode())
    assert result.exit_code == 0


def test_cli_token_expiration(patch, runner, app):
    patch.object(Tokens, 'encode')
    result = runner.invoke(Cli.token, ['user', '200'])
    Tokens.encode.assert_called_with('secret', expiration=200, sub='user')
    assert result.exit_code == 0


def test_cli_create_user(patch, runner, quickstart):
    patch.init(Users)
    patch.object(Users, 'save')
    result = runner.invoke(Cli.create_user, ['identifier'])
    dictionary = {'identifier': 'identifier', 'group': 1,
                  'group_permission': 1, 'owner_permission': 1,
                  'others_permission': 1, 'owner_permission': 1,
                  'superuser': False}
    Users.__init__.assert_called_with(**dictionary)
    assert Users.save.call_count == 1
    assert result.exit_code == 0


def test_cli_create_user_superuser(patch, runner, quickstart):
    patch.init(Users)
    patch.object(Users, 'save')
    result = runner.invoke(Cli.create_user, ['identifier', '--superuser'])
    dictionary = {'identifier': 'identifier', 'group': 1,
                  'group_permission': 1, 'owner_permission': 1,
                  'others_permission': 1, 'owner_permission': 1,
                  'superuser': True}
    Users.__init__.assert_called_with(**dictionary)
    assert Users.save.call_count == 1
    assert result.exit_code == 0


def test_cli_load_blueprint(patch, runner, quickstart):
    patch.object(Blueprints, 'load')
    runner.invoke(Cli.load_blueprint, ['filename'])
    Blueprints.load.assert_called_with('filename')
    assert Base.init_db.call_count == 1


def test_cli_run(app, runner):
    result = runner.invoke(Cli.run)
    assert App.run.call_count == 1
    assert result.exit_code == 0
