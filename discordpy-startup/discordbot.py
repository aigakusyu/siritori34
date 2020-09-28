# インストールした discord.py を読み込む
import discord
import pandas as pd
import random
import codecs
siritori =""
use_word = []

with codecs.open('https://raw.githubusercontent.com/aigakusyu/discordpy-startup/master/s_hyou1.csv', "r", "UTF-8", "ignore") as file:
    siritori = pd.read_table(file, delimiter=",")

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ['DISCORD_BOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    def check(msg):
        return msg.author == message.author

    if message.content.startswith("/start"):

        await message.channel.send("しりとりスタート！　しりとり")
        siri = str('しりとり')

        while True:

            wait_message = await client.wait_for("message", check=check)

            i = random.randint(0,100)

            if wait_message.content[-1] == str("ん"):
                await message.channel.send("おわりやで")
                break

            elif wait_message.content in use_word:
                await message.channel.send("同じ言葉を使っちゃったね")
                await message.channel.send("残念！、またあそんでね")
                break

            elif (wait_message.content[0]) != str(siri[-1]):
                await message.channel.send("しりとりできてないね")
                await message.channel.send("残念！、またあそんでね")
                break

            siri = str(siritori[wait_message.content[-1]][i])

            if siritori[wait_message.content[-1]][i] in use_word:
                await message.channel.send("考え中...")
                while True:
                    i = random.randint(0,100)
                    if siritori[wait_message.content[-1]][i] not in use_word:
                        siri = str(siritori[wait_message.content[-1]][i])
                        break
                    elif str(siritori[wait_message.content[-1]][i]) == 'nan':
                        await message.channel.send("まけね")

            elif str(siritori[wait_message.content[-1]][i]) == 'nan':

                for n in range(10):
                    siri = "今回は私の負けみたい…あなた強いわね！"
                    i = random.randint(0,100)
                    if str(siritori[wait_message.content[-1]][i]) != 'nan':
                        siri = str(siritori[wait_message.content[-1]][i])
                        break
                break

            await message.channel.send(siritori[wait_message.content[-1]][i])
            use_word.append(wait_message.content)
            use_word.append(siritori[wait_message.content[-1]][i])

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
