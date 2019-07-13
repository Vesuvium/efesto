# -*- coding: utf-8 -*-
import click

from peewee import OperationalError, ProgrammingError

from .App import App
from .Blueprints import Blueprints
from .Config import Config
from .Generator import Generator
from .Tokens import Tokens
from .Version import version
from .models import Base, Types, db


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
    @click.argument('identifier')
    @click.option('--superuser', is_flag=True)
    def create_user(identifier, superuser):
        App.create_user(identifier, superuser)
        click.echo(f'User {identifier} created.')

    @staticmethod
    @main.command()
    @click.argument('filename')
    def load_blueprint(filename):
        """
        Load the specified blueprint file
        """
        config = Config()
        Base.init_db(config.DB_URL)
        Blueprints().load(filename)

    @staticmethod
    @main.command()
    def generate():
        """
        Generates dynamic tables from existing types
        """
        config = Config()
        Base.init_db(config.DB_URL)
        types = Types.select().execute()
        generator = Generator()
        for dynamic_type in types:
            generator.generate(dynamic_type)
        db.create_tables(generator.models.values(), safe=True)

    @staticmethod
    @main.command()
    def version():
        click.echo('Version {}'.format(version))

    @staticmethod
    @main.command()
    def run():
        return App.run()
