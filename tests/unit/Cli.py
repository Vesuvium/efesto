#   Copyright (C) 2018  Jacopo Cascioli
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
import click
from click.testing import CliRunner

from efesto.App import App
from efesto.Cli import Cli
from efesto.Tokens import Tokens
from efesto.Version import version

from psyker.exceptions import ConnectionError

from pytest import fixture


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


def test_cli_install_error(patch, runner):
    patch.object(click, 'echo')
    patch.object(App, 'install', side_effect=ConnectionError('url'))
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


def test_cli_create__user(patch, runner):
    patch.object(click, 'echo')
    patch.object(App, 'create_user')
    result = runner.invoke(Cli.create, ['users', 'identifier'])
    App.create_user.assert_called_with('identifier', False)
    click.echo.assert_called_with('User identifier created.')
    assert result.exit_code == 0


def test_cli_create__user_none(patch, runner):
    patch.object(click, 'echo')
    patch.object(App, 'create_user', return_value=None)
    runner.invoke(Cli.create, ['users', 'identifier'])
    click.echo.assert_called_with('User identifier already exists.')


def test_cli_create__user_superuser(patch, runner):
    patch.object(App, 'create_user')
    result = runner.invoke(Cli.create, ['users', 'identifier', '--superuser'])
    App.create_user.assert_called_with('identifier', True)
    assert result.exit_code == 0


def test_cli_load(patch, runner):
    patch.object(App, 'load')
    runner.invoke(Cli.load, ['filename'])
    App.load.assert_called_with('filename')


def test_cli_version(patch, runner):
    patch.object(click, 'echo')
    runner.invoke(Cli.version, [])
    click.echo.assert_called_with('Version {}'.format(version))


def test_cli_run(app, runner):
    result = runner.invoke(Cli.run)
    assert App.run.call_count == 1
    assert result.exit_code == 0
