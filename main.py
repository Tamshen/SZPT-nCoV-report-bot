from include import *
from flask import Flask, request, jsonify
from peewee import SqliteDatabase
from apscheduler.schedulers.background import BackgroundScheduler
import argparse

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def userAdd():
    data = request.json
    User.get_or_create(
        token=data['token'],
        name=data['name'],
        user_id=data['user_id'],
        user_pwd=data['user_pwd']
    )
    return jsonify({'status': 'success!'})


@app.route('/list')
def userList():
    results = User.select().dicts().execute()
    return jsonify({'data': list(results)})


@app.route('/delete', methods=['POST'])
def userDel():
    data = request.json
    results = User.select().where(User.token == data['token'], User.user_id == data['user_id']).get()
    results.status = Status.removed
    results.save()
    return jsonify({'status': 'deleted!'})


@app.route('/check-now', methods=['POST'])
def userCheck():
    data = request.json
    results = User.select().where(User.token == data['token'], User.user_id == data['user_id']).get()
    msg = send(results.user_id, results.user_pwd)
    if msg[0] == 0:
        results.latest_response_time = datetime.datetime.now
        results.save()
    return jsonify({'msg': msg[1]})


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

    app.run(debug=True)


if __name__ == '__main__':
    scheduler = BackgroundScheduler(timezone=CRON_TIMEZONE)
    main()
