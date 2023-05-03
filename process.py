# pylint: disable=E1101
# pylint: disable=E1120
# pylint: disable=R0913
"""
Process text files according to homework
instructions.
"""
import datetime
import os
from typing import Any, Tuple

import click
import pandas as pd  # type: ignore

from geography_helper import state_name_to_abbrev
from postgres_helper import create_fill_local_table_from_csv
from text_helper import parse_name

COMPANIES_FILE = "companies.csv"
GOLF_FILE = "unity_golf_club.csv"
SOFTBALL_FILE = "us_softball_league.tsv"

GOLF_DATE_FORMAT = "%Y/%m/%d"
SOFTBALL_DATE_FORMAT = "%m/%d/%Y"

ERRORS_FILE = "parsing_errors.csv"
PREPARED_FILE = "prepared_records.csv"
PREPARED_TABLE_NAME = "prepared_records"


def format_softball_row(row: pd.Series) -> Tuple[Any, ...]:
    """
    Tranform necessary columns in the input row.
    """
    return (
        *parse_name(row["name"]),
        state_name_to_abbrev(row["us_state"]),
    )


@click.command()
@click.option("--companies_file", prompt="Companies file path", default=COMPANIES_FILE)
@click.option("--golf_file", prompt="Golf file path", default=GOLF_FILE)
@click.option("--softball_file", prompt="Softball file path", default=SOFTBALL_FILE)
@click.option("--dbname", prompt="Database name")
@click.option("--dbuser", prompt="Postgres username", default="postgres")
@click.option("--password", hide_input=True, prompt="Postgres password")
def process_files(
    companies_file: str,
    golf_file: str,
    softball_file: str,
    dbname: str,
    dbuser: str,
    password: str,
) -> None:
    """
    Load, transform, quality check,
    write output files, and load them
    into the database.
    """
    companies_df = pd.read_csv(companies_file)
    golf_df = pd.read_csv(
        golf_file,
        converters={
            "dob": lambda x: datetime.datetime.strptime(x, GOLF_DATE_FORMAT),
            "last_active": lambda x: datetime.datetime.strptime(x, GOLF_DATE_FORMAT),
        },
    )
    softball_df = pd.read_csv(
        softball_file,
        sep="\t",
        converters={
            "date_of_birth": lambda x: datetime.datetime.strptime(
                x, SOFTBALL_DATE_FORMAT
            ),
            "last_active": lambda x: datetime.datetime.strptime(
                x, SOFTBALL_DATE_FORMAT
            ),
        },
    )

    (
        softball_df["first_name"],
        softball_df["last_name"],
        softball_df["us_state"],
    ) = zip(*softball_df.apply(format_softball_row, axis="columns"))

    softball_df = softball_df.rename(
        columns={
            "date_of_birth": "dob",
            "joined_league": "member_since",
            "us_state": "state",
        }
    )

    golf_df["source"] = "unity golf club"
    softball_df["source"] = "us softball league"

    combined_df = pd.concat(
        [golf_df, softball_df], axis="rows", join="inner", ignore_index=True
    )
    # Do a left merge to accommodate records that have a `company_id`
    # that we don't expect. These end up with a NULL `company_name`.`
    combined_df = combined_df.merge(
        companies_df, how="left", left_on="company_id", right_on="id"
    )
    combined_df = combined_df.rename(columns={"name": "company_name"})
    combined_df = combined_df.drop(columns={"company_id", "id"})

    errors_df = combined_df.loc[
        (combined_df["dob"] > combined_df["last_active"])
        | (
            combined_df["member_since"]
            > pd.DatetimeIndex(combined_df["last_active"]).year
        )
    ]

    good_df = (
        pd.merge(combined_df, errors_df, indicator=True, how="outer")
        .query('_merge=="left_only"')
        .drop("_merge", axis="columns")
    )

    errors_df.to_csv(ERRORS_FILE, index=False, date_format=GOLF_DATE_FORMAT)
    good_df.to_csv(PREPARED_FILE, index=False, date_format=GOLF_DATE_FORMAT)

    prepared_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {PREPARED_TABLE_NAME}
    (
    first_name text
    , last_name text
    , dob date
    , last_active date
    , score int
    , member_since int
    , state text
    , source text
    , company_name text
    )
    ;
    """

    create_fill_local_table_from_csv(
        database=dbname,
        user=dbuser,
        password=password,
        table_name=PREPARED_TABLE_NAME,
        create_sql=prepared_table_sql,
        csv_path=os.path.join(os.getcwd(), PREPARED_FILE),
    )


if __name__ == "__main__":
    process_files()
