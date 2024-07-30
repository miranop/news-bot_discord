import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('news.db')
c = conn.cursor()

#テーブルの作成

sql1 =( """CREATE TABLE IF NOT EXISTS articles(
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
sql2 = ('''
    CREATE TABLE IF NOT EXISTS urls (
        url TEXT PRIMARY KEY
    )
''')
c.execute(sql1)
c.execute(sql2)

def save_article(article_id):
    c.execute('INSERT OR IGNORE INTO articles (id, timestamp) VALUES(?,?)',(article_id,datetime.now()))
    conn.commit()

def check_article(article_id):
    c.execute('SELECT 1 FROM articles WHERE id = ?',(article_id,))
    return c.fetchone() is not None

def delete_article(days = 7):
    delete_day = datetime.now() - timedelta(days=days)
    delete_day_str = delete_day.strftime('%Y-%m-%d %H:%M:%S')
    c.execute('DELETE FROM articles WHERE timestamp < ?',(delete_day_str,))
    conn.commit()

def save_rss(url):
    c.execute('INSERT OR IGNORE INTO urls (url) VALUES (?)',(url,))
    conn.commit()

def get_urls():
    c.execute('SELECT url FROM urls')
    return [row[0] for row in c.fetchall()]