import feedparser
import discord
from discord.ext import commands,tasks
import db

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

Url_list = db.get_urls()
channel_id = None

# 追加するURLの受け取り
@bot.command()
async def Url(ctx, *,Url: str):
    if Url not in Url_list:
        Url_list.append(Url)
        db.save_rss(Url)
        await ctx.send(f'追加しました')
    else:
        await ctx.send(f'既に存在します')
#追加するチャンネルの受け取り
@bot.command()
async def channel(ctx,id:int):
       global channel_id
       channel_id = id
       await ctx.send(f'チャンネルを登録しました: {id}')
       
@tasks.loop(minutes=5)
async def check_News():
    channel = bot.get_channel(channel_id)
    if channel is None:
        return  # 無効なチャンネルIDの場合は何もしない
    
    for rss in Url_list: #URLlistの中身にあるRSSを全パースする
        feed = feedparser.parse(rss)
        for entry in feed.entries:
            article_id = entry.id
            if not db.check_article(article_id):
                title = entry.title
                link = entry.link
                summary = entry.summary
                
                news = f"Title: {title}\n Link: {link}\n Summary: {summary}"
                await channel.send(news)
                
                # 新しい記事を保存
                db.save_article(article_id)

# 古い記事を削除するタスク
@tasks.loop(hours=24)
async def clean_article():
    db.delete_article(days=7)
    
@bot.event
async def on_ready():
    check_News.start()
    clean_article.start()

bot.run('')


            
            
            
    
    