import click
from src.dbconnection import DBConnection
from src.survey import *
import uuid


def init_db():
    """init a database connection
    :arg
        driver: the db driver
        server: the db host
        database: the db name
        user: the username
        password: username's password"""
    driver = click.prompt(
        "db driver",
        default="{SQL Server}"
    )
    server = click.prompt(
        "server",
        default="LAPTOP-BARTHE\DAENERYS"
    )
    database = click.prompt(
        "database",
        default="Survey_Sample_A18"
    )
    user = click.prompt(
        "username",
        default="sa"
    )
    password = click.prompt(
        "password",
        hide_input=True
    )
    conn = DBConnection(driver=driver, server=server, database=database, user=user, password=password)

    return (conn)


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    ctx.obj


@cli.command('init-db')
@click.pass_context
def dbconnect(ctx):
    """create a database object in the context"""
    ctx.obj = init_db()


@cli.command()
@click.pass_context
def get_view_surveydata(ctx):
    """get data from vw_AllSurveyData if it exists
    :arg
     ctx: A db instance
    :return
     the result query of the view vw_AllSurveyData
    :except Invalid object name"""
    query_str = str("""SELECT * FROM vw_AllSurveyData""")
    if ctx.obj is None:
        ctx.obj = init_db()
    conn = ctx.obj.get_connection()

    try:
        vw_AllSurveyData = pandas.io.sql.read_sql(query_str, conn)
        print(vw_AllSurveyData)
    except Exception as ex:
        print ("Invalid object name vw_AllSurveyData.")


@cli.command()
@click.pass_context
def generate_last_survey_structure(ctx):
    """Create as file lastsurveystructure.csv in db folder"""
    if ctx.obj is None:
        ctx.obj = init_db()
    conn = ctx.obj.get_connection()
    generatelastsurveystructure(conn)


@cli.command()
def get_last_survey_structure():
    """Get the last survey structure"""
    try:
        df = getlastsurveystructure()
        print(df)
    except Exception as ex:
        print("No survey structure file. Generate one first.")


@cli.command()
@click.argument("query", type=str, required=True)
@click.pass_context
def update_survey_structure(ctx, query):
    """Trigger view creation while updating
    the survey structure's table
    Generate a file with always-fresh survey data in db folder
    :arg
        ctx: a databse instance
        query: the query to execute
    :except

    """
    if ctx.obj is None:
        ctx.obj = init_db()
    conn = ctx.obj.get_connection()
    try:
        ctx.obj.execute_query(query)
        # trigger the view creation
        trg_query = getdynamicsurveydata(conn)
        ctx.obj.execute_query(trg_query)

        # update the last known survey structure
        generatelastsurveystructure(conn)

        # extract the “always-fresh” pivoted survey data, in a CSV file
        fresh_surveydata = str("""SELECT * FROM vw_AllSurveyData""")
        surveydata = pandas.io.sql.read_sql(fresh_surveydata, conn)
        PATH = ".\src\db"
        _id = uuid.uuid4()
        surveydata.to_csv(path_or_buf=os.path.join(PATH, "survey-data"+str(_id)+".csv"), sep=",", header=True,
                                       index=None)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    cli()

