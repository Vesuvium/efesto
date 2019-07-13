# -*- coding: utf-8 -*-
import click

from peewee import OperationalError, ProgrammingError

from .App import App
from .Config import Config
from .Tokens import Tokens
from .Version import version


class Cli:
    installation_error = ('An error occured during tables creation. '
                          'Please check your database credentials.')

    @click.group()
    def main():
        pass

    @staticmethod
    @main.command()
    def install():
        """
        Installs efesto using App.install
        """
        click.echo('Setting up efesto...')
        try:
            App.install()
        except (OperationalError, ProgrammingError):
            click.echo(Cli.installation_error)
            exit(1)
        click.echo('Installation successful!')

    @staticmethod
    @main.command()
    @click.argument('user')
    @click.argument('expiration', default=100)
    def token(user, expiration):
        """
        Get an authentication token for an user
        """
        config = Config()
        token = Tokens.encode(config.JWT_SECRET, expiration=expiration,
                              sub=user, aud=config.JWT_AUDIENCE)
        click.echo(token)

    @staticmethod
    @main.command()
    @click.argument('item_type')
    @click.argument('identifier')
    @click.option('--superuser', is_flag=True)
    def create(item_type, identifier, superuser):
        """
        Creates an item
        """
        if item_type == 'users':
            if App.create_user(identifier, superuser):
                return click.echo(f'User {identifier} created.')
            return click.echo(f'User {identifier} already exists.')

    @staticmethod
    @main.command()
    @click.argument('filename')
    def load(filename):
        """
        Loads the specified blueprint.
        """
        App.load(filename)

    @staticmethod
    @main.command()
    def version():
        click.echo('Version {}'.format(version))

    @staticmethod
    @main.command()
    def run():
        return App.run()
