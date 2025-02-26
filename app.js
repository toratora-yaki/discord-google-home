require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const googlehome = require('google-home-notifier');
const client = new Client({ 
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ] 
});

// Google Nest Hubの設定
const nestHubIP = process.env.NEST_HUB_IP || '192.168.1.x'; // あなたのGoogle Nest HubのIPアドレス
const language = 'ja'; // 日本語
googlehome.device('Google-Nest-Hub', language);
googlehome.ip(nestHubIP);

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
  googlehome.notify(speakText, (res) => {
    console.log(`読み上げ: ${speakText}`);
    console.log(res);
  });
});

// ボットログイン
client.login(process.env.DISCORD_TOKEN);