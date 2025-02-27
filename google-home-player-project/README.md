# google-home-player-project/google-home-player-project/README.md

# Google Home Player Project

このプロジェクトは、`google-home-player`パッケージを使用してGoogle Homeデバイスに音声を再生する機能を実装したアプリケーションです。

## 概要

このアプリケーションは、Discordボットや他のソースからのメッセージを受信し、それをGoogle Homeデバイスで音声再生することを目的としています。

## セットアップ手順

1. リポジトリをクローンします。

   ```
   git clone <repository-url>
   cd google-home-player-project
   ```

2. 依存関係をインストールします。

   ```
   npm install
   ```

3. `.env`ファイルを作成し、Google HomeデバイスのIPアドレスやAPIキーを設定します。

   ```
   NEST_HUB_IP=192.168.1.x
   DISCORD_TOKEN=your_discord_token
   ```

4. アプリケーションを起動します。

   ```
   npm start
   ```

## 使用方法

アプリケーションが起動すると、指定されたGoogle Homeデバイスで音声が再生されます。メッセージを送信することで、音声再生がトリガーされます。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。