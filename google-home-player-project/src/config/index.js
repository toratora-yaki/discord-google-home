require('dotenv').config();

const config = {
  nestHubIP: process.env.NEST_HUB_IP || '192.168.1.x', // Google HomeデバイスのIPアドレス
  language: process.env.LANGUAGE || 'ja', // 使用する言語
};

module.exports = config;