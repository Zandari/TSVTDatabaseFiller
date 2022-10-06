import logging
import argparse
import models
from peewee import SqliteDatabase


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Data scraping and inclusion in the database"
    )

    arg_parser.add_argument(
        '--init',
        action='store_true',
        help="Creating new database"
    )
    arg_parser.add_argument(
        '--update',
        action='store_true',
        help="Updating existing database"
    )

    args = arg_parser.parse_args()
    print(args)

    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Data filler service was started")

    database = SqliteDatabase('1.db')
    models.database_proxy.initialize(database)

    if args.init:
        database.create_tables([
            models.TNVED,
            models.Region,
            models.FederalDistrict,
            models.TSVTRecord,
        ])
