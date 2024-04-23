# 自己対戦の方法

## 1. Agent を待ち受け状態にする

### a. 仮想環境の構築、有効化

```
$ python3 -m venv venv	# 仮想環境の作成
$ . venv/bin/activate	# 仮想環境の有効化
$ pip install -r res/requirements.txt	# ライブラリのインストール
```

### b. 実行

```
$ python3 multiprocess.py
```

## 2. ゲームサーバーを起動する

```sh
$ make run
```
