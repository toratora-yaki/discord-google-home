require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const GoogleHomePlayer = require('google-home-player');
const client = new Client({ 
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ] 
});

// Google Nest Hubの設定
const nestHubIP = process.env.NEST_HUB_IP || '192.168.1.x'; // あなたのGoogle Nest HubのIPアドレス
const googleHome = new GoogleHomePlayer(nestHubIP);

// Discordボットのセットアップ
client.once('ready', () => {
  console.log(`${client.user.tag} がオンラインになりました！`);
});

// メッセージを検出して読み上げる
client.on('messageCreate', async (message) => {
  // ボット自身のメッセージは無視
  if (message.author.bot) return;
  
  // 特定のチャンネルのみ反応する場合（オプション）
  // if (message.channelId !== 'あなたのチャンネルID') return;
  
  // メッセージのフォーマット
  const speakText = `${message.author.username}さんからのメッセージ: ${message.content}`;
  
  // Google Nest Hubで読み上げ
  googleHome.speak(speakText)
    .then(() => {
      console.log(`読み上げ: ${speakText}`);
    })
    .catch((err) => {
      console.error('エラーが発生しました:', err);
    });
});

// ボットログイン
client.login(process.env.DISCORD_TOKEN);