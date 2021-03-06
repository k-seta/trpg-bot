# TRPG-BOT
## Description
TRPG のオンラインセッションを行う際の補助として使うための discord の bot です。

## Requirements
- Python >= 3.6.9
- Poetry >= 1.0.5
- heroku-cli >= 7.26.2
- docker-compose >= 1.12.0

## Usage
```
in Discord

you > /ping
bot > pong

you > /3d6
bot > @you がサイコロを振ったよ
      => 9    [2, 3, 4]

you > /2d6 + 12
bot > @you がサイコロを振ったよ
      => 16    [3, 1], [12]
```

## Development
1. `git clone https://github.com/k-seta/trpg-bot.git` を実行する
1. clone してきた repository 内で `poetry install` を実行して、 pip の依存関係を解決する
1. discord bot の token は環境変数から取得するので、 `export DISCORD_BOT_TOKEN={discord bot の token}` を実行する
1. discord の global チャンネルのIDは環境変数から取得するので、`export GLOBAL_CHANNEL_ID={discord の global channel id}`
1. redis の URL は環境変数から取得するので、 `export REDIS_URL=redis://localhost:6379` を実行する
1. dropbox の token は環境変数から取得するので、 `export DROPBOX_TOKEN={dropbox の token}` を実行する
1. `docker-compose up -d` を実行して、redisをdockerで起動する
1. `poetry shell` を実行して、 virtualenv を起動する
1. `python trpg_bot/trpg_bot.py` で bot の client をローカルで起動できる

## Deploy
1. [heroku](https://jp.heroku.com/) で app を作成する
1. `heroku config:set DISCORD_BOT_TOKEN={discord bot の token} --app "{heroku の app 名}"` を実行して、 PaaS 上に環境変数を設定する
1. `heroku git:remote -a {heroku の app 名}` を実行して、 heroku アプリの repository をローカルに登録する
1. `poetry run pip freeze | grep -v "pkg-resources" > requirements.txt` で、デプロイ用の依存関係設定ファイルを作成する
1. `git push heroku master` でデプロイする

## LICENSE
このソフトウェアは、MITライセンスのもとで公開されています。詳細は、 [LICENSE](https://github.com/k-seta/trpg-bot/blob/master/LICENSE) (英語) をご覧ください。
