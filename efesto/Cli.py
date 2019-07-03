# -*- coding: utf-8 -*-
import click

from peewee import OperationalError, ProgrammingError

from .App import App
from .Blueprints import Blueprints
from .Config import Config
from .Generator import Generator
from .Tokens import Tokens
from .Version import version
from .models import Base, Fields, Types, Users, db


class Cli:

    @click.group()
    def main():
        pass

    @main.command()
    def quickstart():
        """
        Quickstart efesto, creating default tables
        """
        print('Setting up efesto...')
        config = Config()
        Base.init_db(config.DB_URL)
        try:
            db.create_tables([Fields, Types, Users])
        except OperationalError:
            print('An error occured during tables creation. '
                  'Please check your database credentials.')
            exit(1)
        except ProgrammingError:
            print('An error occurred during tables creation. '
                  'Please check your database.')
            exit(1)
        print('Quickstart finished successfully!')

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

    @main.command()
    @click.argument('identifier')
    @click.option('--superuser', is_flag=True)
    def create_user(identifier, superuser):
        config = Config()
        Base.init_db(config.DB_URL)
        user = Users(identifier=identifier, group=1, owner_permission=1,
                     group_permission=1, others_permission=1,
                     superuser=superuser)
        user.save()

    @main.command()
    @click.argument('filename')
    def load_blueprint(filename):
        """
        Load the specified blueprint file
        """
        config = Config()
        Base.init_db(config.DB_URL)
        Blueprints().load(filename)

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

    @main.command()
    def version():
        click.echo('Version {}'.format(version))

    @main.command()
    def run():
        return App.run()
