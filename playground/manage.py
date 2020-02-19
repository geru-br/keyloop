import logging
import click
import transaction


from playground.main import main

logger = logging.getLogger(__name__)


@click.group()
@click.option("--quiet", default=False, is_flag=True)
@click.pass_context
def cli(ctx, quiet):

    ctx.ensure_object(dict)


@cli.group()
@click.option(
    "--force-commit",
    is_flag=True,
    default=False,
    help="Commit at the and of the script.",
)
@click.pass_context
def app(ctx, force_commit=True):
    """
    Initialize a pyramid app. Try manage app --help
    """

    pyramid_app = main()

    ctx.obj["app"] = pyramid_app

    if ctx.parent.params["quiet"]:
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.DEBUG)

    return pyramid_app


@app.resultcallback()
def transaction_commit(result, **kwargs):

    context = click.get_current_context(silent=True)

    if not context.obj.get("force-commit"):
        click.confirm(
            "{} Commit transaction?".format(click.style("ATTENTION", bold=True)),
            abort=True,
        )

    transaction.commit()
    click.echo("Transaction commited.")


@app.command("initialize-db")
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Attempt to initialize db without prompting for confirmation.",
)
@click.pass_context
def initialize_db(ctx, force):
    """
    Initialize DB, this command will drop and create all tables, indexes and constraints
    """

    if not force:
        click.confirm(
            "{} Are you sure you want to initialize the database?".format(
                click.style("ATTENTION", bold=True)
            ),
            abort=True,
        )

    ctx.obj["force-commit"] = True
    from playground.models import Base

    Base.metadata.drop_all()
    click.echo("All tables dropped")
    Base.metadata.create_all()
    click.echo("All tables created")


if __name__ == "__main__":
    cli()
