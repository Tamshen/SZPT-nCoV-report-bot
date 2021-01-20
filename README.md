# SZPT nCoV Report Bot v2

A bot for 2019-nCoV daily report to SZPT (Refactored).

### Todo

### Requirements

- Python3 (dev with Python3.9)
- pip

Run pip install -r requirements.txt to install required components.

### Deployment

If you need to run locally, please clone this project and edit `project/config/config.ini`.

Then just run `cd project` and `python main.py`.


In addition, you can also use Github Action to automate reporting.

Just
- Star and fork this repo
- Go to the forked repo Settings > Secrets
- Add the following environment variables:
    - **USERNAME**: Your login username, which is usually your student number.
    - **PASSWORD**: Your login password.
    - **SCKEY**: The [Server-Chan Secret Key](http://sc.ftqq.com/),if you need WeChat notifications.
    - **BOT_TOKEN**: The [Telegram Bot Token](http://t.me/),if you need Telegram notifications.
    - **CHAT_ID**: The [Telegram Bot](http://t.me/) to chat user id.You can find your chat id at [Sean_Bot](http://t.me/Sean_Bot)

**Note**:

If you are not using Server-Chan or Telegram Bot,please set `ENABLE_SERVER_CHAN` and `ENABLE_TELEGRAM` to `0` in `.github/workflow/work.yaml`

### Contributing

Pull requests and issues are always welcome.

### Acknowledgments

#### Inspiration

https://github.com/AtmosphereMao/SZPT_Ehall_xsjkxxbs

### Authors

- LovelyWei https://github.com/LovelyWei

License
This project is licensed under the GPL v3 License - see the [LICENSE](LICENSE) file for details