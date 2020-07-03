from include import *
from peewee import SqliteDatabase
import argparse


def main():
    # args
    parser = argparse.ArgumentParser(description="SZPT nCoV Report Bot")
    parser.add_argument('--initdb', default=False, action='store_true', help="init database")
    args = parser.parse_args()

    # connect database
    database = SqliteDatabase('nCoV-robot.db')
    database_proxy.initialize(database)

    if args.initdb:
        init_db()
        exit(0)
    login('username', 'password')


if __name__ == '__main__':
    main()
