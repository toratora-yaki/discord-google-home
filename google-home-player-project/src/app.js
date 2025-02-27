require('dotenv').config();
const { GoogleHome } = require('google-home-player');
const config = require('./config/index');

const nestHubIP = config.nestHubIP;
const googleHome = new GoogleHome(nestHubIP);

// 音声を再生する関数
const playAudio = (text) => {
  googleHome.playText(text, (res) => {
    console.log(`再生中: ${text}`);
    console.log(res);
  });
};

// アプリケーションのエントリーポイント
const main = () => {
  const message = "こんにちは、Google Homeからのメッセージです。";
  playAudio(message);
};

main();