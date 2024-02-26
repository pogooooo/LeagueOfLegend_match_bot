import discord
from discord.ext import commands
import sqlite3
from datetime import datetime
import match_list as ml

current_day = datetime.now().strftime("%m/%d")

connection = sqlite3.connect('match_list.db')
cursor = connection.cursor()

id_match = 1

cursor.execute('''
    CREATE TABLE IF NOT EXISTS lol_match (
        id INTEGER,
        owner TEXT NOT NULL,
        time TEXT NOT NULL,
        day TEXT,
        message_id INTEGER,
        participants TEXT
    )''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS match_participant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        message_id INTEGER
    )''')

connection.commit()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'봇이 {bot.user}로 로그인했습니다.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("없는 명령어 사용")
    raise error


@bot.command(name="목록초기화")
async def end(ctx):
    cursor.execute("DELETE FROM lol_match")
    query = f"DELETE FROM sqlite_sequence WHERE name='lol_match';"
    cursor.execute(query)

    cursor.execute("DELETE FROM match_participant")
    query = f"DELETE FROM sqlite_sequence WHERE name='match_participant';"
    cursor.execute(query)

    global id_match
    id_match = 1

    connection.commit()


@bot.command(name="내전만들기")
async def create_match(ctx, participants, time, day="none") :

    current_time = datetime.now().strftime("%H:%M")
    global id_match

    if time < current_time :
        await ctx.send("현재 시간보다 늦은 시간으로 설정해주세요.")
        return()

    if participants != "10인" and participants != "20인":
        await ctx.send("인원을 10인 또는 20인으로 설정해 주세요.")
        return()

    try:
        if day == "none":
            day = current_day
        elif datetime.strptime(day, "%m/%d") < datetime.now():
            await ctx.send("현재 날짜보다 이른 날짜로 설정할 수 없습니다.")
            return ()
    except ValueError:
        await ctx.send(f"날짜 형식은 {current_day}로 입력해 주세요.{day}")
        return ()

    ml.print_start_match(ctx.author.name, day, time, participants, id_match)
    image_path = "C:/Users/poggo/Downloads/Programing/lol_team_match/start_match_screenshot.png"

    with open(image_path, 'rb') as file:
        embed = discord.Embed(
            title=f"{ctx.author.name}의 {id_match}번 내전",
            description="",
            color=discord.Color.blurple()  # 여기서 색상을 지정합니다.
        )
        file = discord.File(file)
        send_message = await ctx.send(embed=embed, file=file)
    await send_message.add_reaction("✅")

    cursor.execute("INSERT INTO lol_match (id, owner, time, day, message_id, participants) VALUES (?, ?, ?, ?, ?, ?)",
                   (id_match, ctx.author.name, time, day, send_message.id,participants))
    cursor.execute('UPDATE last_id SET id = ?', (cursor.lastrowid,))
    connection.commit()
    id_match += 1


@bot.command(name="내전목록")
async def match_list(ctx) :

    cursor.execute("SELECT * FROM lol_match")
    matchs = cursor.fetchall()

    if not matchs :
        await ctx.send("내전이 없습니다.")
        return()

    ml.print_match_list(matchs)
    image_path = "C:/Users/poggo/Downloads/Programing/lol_team_match/match_list_screenshot.png"

    with open(image_path, 'rb') as file:
        file = discord.File(file)
        await ctx.send(file=file)


@bot.event
async def reaction_application(reaction, user):
    channel = reaction.message.channel
    message = reaction.message

    cursor.execute("SELECT * FROM lol_match")
    matchs = cursor.fetchall()

    if user.bot: return

    for i in matchs:
        if i[4] == message.id :
            pass


@bot.command(name="참가신청")
async def application(ctx, number):
    cursor.execute("SELECT * FROM lol_match")
    matchs = cursor.fetchall()

    for i in matchs:
        message_id = i[4]
        if i[0] == int(number):
            cursor.execute("INSERT INTO match_participant (user_name, message_id) VALUES (?, ?)",
                           (ctx.author.name, message_id))
            connection.commit()
            await ctx.send(f"{ctx.author.name}이(가) {message_id} 내전에 참가하였습니다.")

@bot.command(name="테스트")
async def test(ctx):
    cursor.execute("SELECT * FROM match_participant")
    participants = cursor.fetchall()

    cursor.execute("DELETE FROM lol_match WHERE id = 3")

    # 2. 종료된 경기 이후의 경기들의 ID 수정
    cursor.execute("UPDATE lol_match SET id = id - 1 WHERE id > 3")
    cursor.execute("INSERT INTO lol_match (owner, time, day, message_id, participants) VALUES (?, ?, ?, ?, ?)",
                   ("hyun", "23:00", "02/13", 121112, "10인"))



bot.run('MTIwMDc2MTEwNTMyOTQyMjMzNg.GktKpz.kEgKBWXEJDVNeKqFeRKeeqokaWQeq5EZVvHccw')