import os
import discord
from dotenv import load_dotenv
import pychromecast
from gtts import gTTS
import threading
from flask import Flask, send_file
import uuid
import tempfile

# .env ファイルから環境変数を読み込む
load_dotenv()

# 設定
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NEST_HUB_IP = os.getenv('NEST_HUB_IP', '192.168.1.x')
CHANNEL_ID = os.getenv('CHANNEL_ID')  # 監視するDiscordチャンネルID
HOST_IP = os.getenv('HOST_IP', '192.168.1.y')  # このサーバーを実行するマシンのIPアドレス
HOST_PORT = int(os.getenv('HOST_PORT', '5000'))

# 音声ファイルの一時保存用ディレクトリ
TEMP_DIR = tempfile.gettempdir()

# FlaskアプリとDiscordクライアントのセットアップ
app = Flask(__name__)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 現在の音声ファイル
current_audio_file = None

# Flaskルート - 生成された音声ファイルを提供
@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_file(os.path.join(TEMP_DIR, filename), mimetype='audio/mp3')

# Chromecastデバイスを検出・接続する関数
def connect_to_chromecast():
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Google-Nest-Hub"])
    if not chromecasts:
        print("名前での検索に失敗しました。IPアドレスで接続を試みます。")
        chromecasts, browser = pychromecast.get_chromecasts()
        for cast in chromecasts:
            if cast.host == NEST_HUB_IP:
                cast.wait()
                return cast
        print("Google Nest Hubが見つかりませんでした。")
        return None
    else:
        cast = chromecasts[0]
        cast.wait()
        return cast

# テキストをGoogle Nest Hubで読み上げる関数
def speak_on_nest_hub(text):
    global current_audio_file
    
    try:
        # 前の音声ファイルがあれば削除
        if current_audio_file and os.path.exists(os.path.join(TEMP_DIR, current_audio_file)):
            try:
                os.remove(os.path.join(TEMP_DIR, current_audio_file))
            except:
                pass
        
        # テキストを音声ファイルに変換
        filename = f"temp_{uuid.uuid4()}.mp3"
        filepath = os.path.join(TEMP_DIR, filename)
        tts = gTTS(text=text, lang='ja')
        tts.save(filepath)
        current_audio_file = filename
        
        # Chromecastに接続
        cast = connect_to_chromecast()
        if cast is None:
            print("Google Nest Hubに接続できませんでした。")
            return
        
        # メディアプレーヤーを取得
        mc = cast.media_controller
        
        # 音声ファイルのURLを作成
        audio_url = f"http://{HOST_IP}:{HOST_PORT}/audio/{filename}"
        
        # Chromecastでメディアを再生
        mc.play_media(audio_url, 'audio/mp3')
        mc.block_until_active()
        
        print(f"読み上げ完了: {text}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# Discordボットのイベントハンドラ
@client.event
async def on_ready():
    print(f'{client.user} がオンラインになりました！')

@client.event
async def on_message(message):
    # ボット自身のメッセージは無視
    if message.author == client.user:
        return
    
    # 特定のチャンネルのみ反応する場合
    if CHANNEL_ID and str(message.channel.id) != CHANNEL_ID:
        return
    
    # メッセージのフォーマット
    speak_text = f"{message.author.name}さんからのメッセージ: {message.content}"
    
    # 非同期でGoogle Nest Hubに読み上げさせる
    threading.Thread(target=speak_on_nest_hub, args=(speak_text,)).start()

# Webサーバーをバックグラウンドで実行
def run_flask():
    app.run(host='0.0.0.0', port=HOST_PORT)

# メインプログラム
if __name__ == '__main__':
    # Flaskサーバーをバックグラウンドスレッドで起動
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print(f"Webサーバーを起動しました: http://{HOST_IP}:{HOST_PORT}")
    
    # Discordボットを起動
    client.run(DISCORD_TOKEN)