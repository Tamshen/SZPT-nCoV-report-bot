import logging
import sys
from logging import handlers
import uuid
from include import *
from flask import Flask, request, jsonify
from peewee import SqliteDatabase
from apscheduler.schedulers.background import BackgroundScheduler
from shutil import copyfile
import argparse

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def userAdd():
    data = request.json
    token = uuid.uuid4()
    User.get_or_create(
        token=token,
        name=data['name'],
        user_id=data['user_id'],
        user_pwd=data['user_pwd']
    )
    return jsonify({'status': 'success!','data': {'token': token}})


@app.route('/get/<token>')
def userInfo(token):
    try:
        results = User.select(User.token, User.name, User.id, User.latest_response_time, User.status, User.update_time)\
        .where(User.token == token).dicts().get()
        return jsonify({'data': results})
    except:
        return jsonify({'data': 'undefined'})


@app.route('/del/<token>', methods=['POST'])
def userDel(token):
    results = User.select().where(User.token == token).get()
    results.status = Status.removed
    results.save()
    return jsonify({'status': 'deleted!'})


@app.route('/check-now/<token>')
def userCheck(token):
    now = time.localtime()
    if now.tm_hour == 23 and now.tm_min > 30:
        return jsonify({'msg': '今日填报时间已过'})
    user = User.select().where(User.token == token).get()
    msg = send(user.user_id, user.user_pwd)
    if msg[0] == 0:
        user.latest_response_time = datetime.datetime.now()
        user.status = Status.normal
        user.save()
        logger.info(f"用户: {user.token}\t学号: {user.user_id} 签到成功")
    else:
        user.status = Status.warning
        user.save()
        logger.info(f"用户: {user.token}\t学号: {user.user_id} 签到失败\t原因: {msg[1]}")
    return jsonify({'msg': msg[1]})


def backup_db():
    logger.info("backup started!")
    copyfile('./nCoV-robot.db', './backup/nCoV-robot.{}.db'.format(str(datetime.datetime.now()).replace(":","").replace(" ","_")))
    logger.info("backup finished!")


def checkin_all():
    try:
        backup_db()
    except:
        pass
    logger.info("checkin_all started!")
    for user in User.select().where(User.status == Status.normal):
        msg = send(user.user_id, user.user_pwd)
        if msg[0] == 0:
            user.latest_response_time = datetime.datetime.now()
            user.save()
            logger.info(f"用户: {user.token}\t学号: {user.user_id} 签到成功")
        else:
            user.status = Status.warning
            user.save()
            logger.info(f"用户: {user.token}\t学号: {user.user_id} 签到失败\t原因: {msg[1]}")
    logger.info("check_all success!")


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


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

    scheduler.add_job(
        func=checkin_all,
        id='checkin_all',
        trigger="cron",
        hour=CRON_HOUR,
        minute=CRON_MINUTE,
        max_instances=1,
        replace_existing=False,
        misfire_grace_time=10,
    )

    scheduler.start()
    logger.info(["name: %s, trigger: %s, handler: %s, next: %s" % (job.name, job.trigger, job.func, job.next_run_time) for job in scheduler.get_jobs()])

    # exit()
    app.after_request(after_request)
    app.run(debug=DEBUG_MODE, host=BIND_HOST, port=BIND_PORT)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,handlers=[
        logging.handlers.TimedRotatingFileHandler(
            "log/main", when='midnight', backupCount=30, encoding='utf-8',
            atTime=datetime.time(hour=0, minute=0)
        ),
        logging.StreamHandler(sys.stdout)
    ])
    logger = logging.getLogger('Main')

    logger.info("======== Starting ==========")
    scheduler = BackgroundScheduler(timezone=CRON_TIMEZONE)
    main()
