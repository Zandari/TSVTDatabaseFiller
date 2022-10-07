import logging
import argparse
import models
import csv
from time import time
from peewee import SqliteDatabase


def set_static_data():
    csv_files = [
        (models.Country, "static\\COUNTRIES.csv"),
        (models.FederalDistrict, "static\\FEDERAL_DISTRICTS.csv"),
        (models.MeasureUnit, "static\\MEASURE_UNITS.csv"),
        (models.Region, "static\\REGIONS.csv"),
        (models.TNVED, "static\\TNVED.csv")
    ]
    for model, path in csv_files:
        with open(path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for record in reader:
                model.create(**record)


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

    logging.getLogger().setLevel(logging.INFO)
    logging.info("Data filler service was started")

    t = time()

    database = SqliteDatabase('1.db')
    models.database_proxy.initialize(database)
    database.connect()

    if args.init:
        logging.info("Creating tables...")
        database.create_tables([
            models.MeasureUnit,
            models.TNVED,
            models.Region,
            models.FederalDistrict,
            models.Country,
            models.TSVTRecord,
        ])
        database.commit()
        logging.info("Done")

    if args.init:
        logging.info("Setting static data...")
        set_static_data()
        logging.info("Done")

