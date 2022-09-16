import discord,json,os,random
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

bot = commands.Bot()

with open('config.json','r',encoding='utf-8') as file:
    data=json.load(file)
TOKEN=data["token"]
OWNER=data["owner"]
GUILD=data["guild"]

@bot.event
async def on_ready(): 
    print(f'>>{bot.user}上線<<')
    print('>>>>> 此項目由機車製作，使用請標註來源，感謝尊重 <<<<<')
    print('>>>>> 有任何問題請至 https://discord.gg/ouou <<<<<')

@slash_command(description='給予用戶錢錢',guild_ids=[GUILD])
async def help(ctx):
    with open('help.txt','r',encoding='utf-8') as file:
        data=file.read()
    embed=discord.Embed(title="Money Bot", description=data,color=discord.Colour.random())
    await ctx.respond(embed=embed)


@slash_command(description='給予用戶錢錢',guild_ids=[GUILD])
async def mset(ctx,
        user:Option(discord.User,"要給的用戶"),count:Option(int,"要給的錢數")):
    if ctx.author.id == OWNER:
        jfile=f"money/{user.id}.json"
        if os.path.isfile(jfile):
            with open(jfile,'r') as file:
                data=json.load(file)
                l=data["money"]
                data["money"]=count+l
            with open(jfile,'w') as file:
                json.dump(data,file)
            await ctx.respond(f"{user.mention} 得到機車發的 `{count}`元")
        else:
            with open(jfile,'w') as file:
                data={"money":count}
                json.dump(data,file)
            await ctx.respond('他還沒有錢包，所以我幫他創了一個')
    else:
        await ctx.respond(f'只有<@{OWNER}>可以用喔~',allowed_mentions=discord.AllowedMentions(users=False))

@slash_command(description='查看你目前的錢數',guild_ids=[GUILD])
async def money(ctx):
    jfile=f'money/{ctx.author.id}.json'
    if os.path.isfile(jfile):
        with open(jfile,'r') as file:
            data=json.load(file)
        money=data["money"]
        embed=discord.Embed(title="您的錢包", description=f"您目前有【{money}】元",color=discord.Colour.random())
        await ctx.respond(embed=embed)
    else:
        with open(jfile,'w') as file:
            data={"money":0}
            json.dump(data,file)
        await ctx.respond('您還沒有錢包，所以我幫您創了一個')

@slash_command(description='工作賺錢錢',guild_ids=[GUILD])
@commands.cooldown(1,3600,commands.BucketType.user)
async def work(ctx):
    count=random.randint(0,100)
    jfile=f'money/{ctx.author.id}.json'
    if os.path.isfile(jfile):
        with open(jfile,'r') as file:
            data=json.load(file)
        l=data["money"]
        data["money"]=l+count
        with open(jfile,'w') as file:
            json.dump(data,file)
        with open(jfile,'r') as file:
            data=json.load(file)
        now=data["money"]
        embed=discord.Embed(title="工作", description=f"你透過工作賺到{count}元\n你現在有{now}元",color=discord.Colour.random())
        await ctx.respond(embed=embed)
    else:
        with open(jfile,'w') as file:
            data={"money":count}
            json.dump(data,file)
        await ctx.respond(f'您還沒有錢包，所以我幫您創了一個,並獲得了工資{count}元')

@slash_command(description='賭博?',guild_ids=[GUILD])
async def bet(ctx,count:Option(int,"要購買的數量(一個100)")):
    jfile= f"money/{ctx.author.id}.json"
    if os.path.isfile(jfile):
        with open(jfile,'r') as file:
            data=json.load(file)
        l=data["money"]
        if l < count*100-1:
            await ctx.respond(f'你的錢不夠吶')
        if l > count*100-1:
            for r in range(count):
                with open(jfile,'r') as file:
                    data=json.load(file)
                l=data["money"]
                m=random.randint(0,200)
                data["money"]=l-100+m
                with open(jfile,'w') as file:
                    json.dump(data,file)
                with open(jfile,'r') as file:
                    data=json.load(file)
                m=data["money"]
                embed=discord.Embed(title="刮刮樂", description=f"你買了{count}張刮刮樂\n你原本有{l}元 | 現在有{m}元!",color=discord.Colour.random())
                await ctx.respond(embed=embed)
    else:
        with open(jfile,'w') as file:
            data={"money":0}
            json.dump(data,file)
        await ctx.respond('您還沒有錢包，所以我幫您創了一個')

bot.run(TOKEN)