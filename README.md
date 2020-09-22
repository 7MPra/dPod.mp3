# dPod.mp3
dPod.mp3は、音声ファイルをDiscordのボイスチャットに流すことができるBOTです。

# How to Use
## すぐに使う場合
https://tenp.pw/9ycWAbR
からbotを追加してください
## 自分で構築する場合
```
git clone https://github.com/TMP-tenpura/dPod.mp3.git
#ここでdiscordbot.pyの変数TOKENをあなたのトークンに変更しておいて下さい
#ここまでにHerokuのframeworkの中にPython, ffmpeg, libopusが含まれていることを確認して下さい
heroku git:clone -a YourApp
ls -1 dPod.mp3 | cp -t Yourapp
cd Yourapp
git push heroku master
```
botをDiscord内のサーバーに招待してからDiscord内で`;mp3;help`と発言することで使用可能なコマンドを確認できます。
