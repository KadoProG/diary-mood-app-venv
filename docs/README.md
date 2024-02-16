Python のバージョンは `3.11.0` で検証しています

## よく使うコマンド

### マイグレート

```bash
python manage.py migrate
```

### サーバの起動

```bash
python manage.py runserver localhost:8000
```

### ファイルのフォーマット

```bash
black .
```

## Python 開発時コマンド

### Django プロジェクトを作成

`django-admin startproject myApp` を実行する
(myApp がディレクトリ名となる)

### 必要なパッケージをインストール

```bash
pip install -r requirements.txt
```

### アプリケーションの作成

```bash
python manage.py startapp {アプリケーション名}
```
