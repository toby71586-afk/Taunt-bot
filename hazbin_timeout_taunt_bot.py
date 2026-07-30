import discord
import asyncio
import random
import logging
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("taunt-bot")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TIMEOUT_CHANNEL_ID = int(os.getenv("TIMEOUT_CHANNEL_ID", "0"))
MOD_CHANNEL_ID = int(os.getenv("MOD_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

CHARACTERS = {
    "Charlie": {"color": 0xCC0000, "dms": ["Oh honey, a timeout? That's okay! Everyone needs a moment to breathe!", "Timeouts are just... thinking breaks! Use this time to reflect on kindness!", "I believe in second chances! And third chances! And fourth chances!", "Take all the time you need! We'll be here when you're ready to be nice!", "Every soul deserves redemption! Even if they need a timeout first!"], "roasts": ["Aww, you wrote '{msg}'? That's so... cute! Like a puppy trying to bark!", "'{msg}'? Sweetie, I believe in you! But maybe think before you type next time?", "Oh honey, '{msg}' is not the flex you think it is. Let's work on that.", "'{msg}'? That's adorable. You're adorable. Timeout is for learning!", "I know you're upset, but '{msg}' isn't helping your case! Try kindness!"]},
    "Vaggie": {"color": 0x9B59B6, "dms": ["You messed up. Now sit there and think about it.", "I warned you. Now deal with the consequences.", "Enjoy your timeout. Maybe use it to learn some manners.", "Don't test me. I've killed angels. A timeout is mercy.", "Rules exist for a reason. You broke them. Now you sit."], "roasts": ["'{msg}'? That's your defense? Pathetic.", "You had time to type '{msg}' and THAT'S what you came up with?", "I've heard better arguments from a dying sinner. '{msg}' is weak.", "'{msg}'? Wow. Really doubling down on being wrong, huh?", "You typed '{msg}' like it meant something. It didn't."]},
    "Angel Dust": {"color": 0xFF69B4, "dms": ["Ooooh someone's in trou-ble~! Wish I could see your face right now!", "Timeout? Babe, I've been in timeout my whole afterlife. Get used to it.", "Aww, did the widdle baby get put in time out? That's ADORABLE.", "First time? Don't worry, it won't be the last, sweetheart.", "I'd say I feel bad for you, but I'd be lying. This is hilarious."], "roasts": ["'{msg}'? Babe, that's the best you got? I've heard better from a drunk spider.", "'{msg}'? Oh honey, no. Just... no. Sit back down.", "You really typed '{msg}' and thought you ATE. You didn't. You starved.", "'{msg}'? Cute attempt. Really. A for effort, F for execution.", "I've seen corpses with more personality than '{msg}'. And I've seen a LOT of corpses."]},
    "Alastor": {"color": 0x8B0000, "dms": ["Oh, how WONDERFUL! A little sinner in timeout! This is going to be ENTERTAINING!", "I do love the sound of a timeout. So... quiet. So... still. HA!", "Don't worry, my dear! I'll be watching! I'm ALWAYS watching!", "A timeout? How DELIGHTFULLY old-fashioned! I approve!", "Rules were made to be broken! But consequences? Those are FOREVER!"], "roasts": ["'{msg}'! Oh, that's RICH! I'll be broadcasting this on my radio show!", "My dear, '{msg}' is the most ENTERTAINING thing I've heard all century!", "'{msg}'? How DELIGHTFULLY foolish! Do go on, this is marvelous!", "I do love the sound of desperation! And '{msg}' is PERFECT radio material!", "'{msg}'? HA! The sheer AUDACITY! I haven't laughed this hard in decades!"]},
    "Cherri Bomb": {"color": 0xFF4500, "dms": ["HA! You got BUSTED! This is the best show in Hell!", "Timeouts are for quitters! But I guess you're quitting on being free, huh?", "Don't worry, I'll blow something up in your honor while you're stuck in there!", "This is why you don't get caught, dumbass!", "I'd break you out, but honestly? This is too funny to interrupt."], "roasts": ["'{msg}'? That's your big move? I've seen bombs fizzle with more impact.", "'{msg}'? BOOOORING! I'd rather watch paint dry. Actually no, paint is more exciting.", "You wrote '{msg}' like you thought it mattered. It didn't. BOOM. Roasted.", "'{msg}'? That's what you're going with? I've exploded better things by ACCIDENT.", "HA! '{msg}'! You're literally in timeout and still running your mouth! I LOVE it!"]},
    "Niffty": {"color": 0xFF1493, "dms": ["OOH OOH OOH! Someone's in trouble! Can I watch? Can I? CAN I?", "Timeout timeout timeout! This is so EXCITING!", "I like bad boys! Especially ones in timeout! STAB STAB-- oh wait, timeout means no stabbing!", "You're so still! Like a little statue! A BAD statue!", "I once put myself in timeout for a whole week! It was FUN!"], "roasts": ["'{msg}'! Hee hee! That's so FUNNY! Can I keep it? Please please please?", "'{msg}'? You're so BAD! I love bad messages! STAB-- oh wait, no stabbing!", "'{msg}'! That's a MESS! Let me clean it up! *frenetic scrubbing noises*", "Ooh '{msg}'! That's SPARKLY! Like a little trash gem!", "'{msg}'? You wrote that? You're so TALL and WRONG! Hee hee!"]},
    "Husk": {"color": 0xFFA500, "dms": ["Heh. Welcome to the club, loser.", "Timeout, huh? Get in line. I've been in timeout for decades.", "You know what's good in timeout? Nothing. Absolutely nothing.", "First rule of Hell: don't get caught. You failed.", "I'd pour you a drink, but you're in timeout. Sucks to be you."], "roasts": ["'{msg}'? That's what you wasted your one message on? Pathetic.", "You typed '{msg}' like anyone cares. News flash: they don't.", "'{msg}'? I've heard better from a dying cat. And I hate cats.", "You're in timeout and '{msg}' is your masterpiece? No wonder you got caught.", "'{msg}'? *sigh* I need another drink. And I haven't even finished this one."]},
    "Lucifer": {"color": 0xFFD700, "dms": ["A timeout? I invented timeouts. Literally. Fell from Heaven for it.", "You think THIS is bad? I spent MILLENNIA in timeout.", "Timeouts are for learning. What did we learn? Probably nothing.", "I could snap my fingers and end your timeout. But I won't. That's the fun part.", "Welcome to consequences, my dude. They suck."], "roasts": ["'{msg}'? I've heard better comebacks from Adam. And Adam was an idiot.", "You wrote '{msg}'? I literally invented free will and THIS is what you do with it?", "'{msg}'? That's almost impressive. Almost. Not quite. Not at all.", "I fell from Heaven for pride and even I wouldn't type '{msg}'.", "'{msg}'? Wow. Even I'm disappointed. And I have VERY low expectations."]},
    "Rosie": {"color": 0xFF69B4, "dms": ["Oh my, a naughty little soul in timeout! How PRECIOUS!", "Don't worry dear, I'll save you a seat at dinner! We're having... whatever you're having!", "Timeouts build character! And I do love a well-seasoned character!", "The colony doesn't approve of your behavior. But I think you're DELICIOUSLY bad!", "Sit tight, sweetie! I'll check on you later with a little... snack!"], "roasts": ["'{msg}'? Oh my, that's DELICIOUS! I'll be savoring that one!", "Dear, '{msg}' is just the most FLAVORFUL thing you could have said!", "'{msg}'? How TASTY! You really know how to season a conversation!", "Oh sweetie, '{msg}' is absolutely PRECIOUS. Like a little appetizer!", "'{msg}'? Mmm, I can practically TASTE the desperation. Exquisite!"]},
    "Vox": {"color": 0x00BFFF, "dms": ["Oh, I've got cameras on you. This is GOLDEN content.", "Timeouts are so last century. But watching you suffer? That's timeless.", "I'm broadcasting this to all of Hell. You're famous now. You're WELCOME.", "You know what's better than television? Watching you sit in timeout. LIVE.", "Don't worry, I'll make sure everyone sees what happens when you cross the rules."], "roasts": ["'{msg}' is trending. Not for a good reason though. #LMAO", "'{msg}'? I'm putting this on every screen in Hell. You're a STAR.", "You had airtime and chose '{msg}'? No wonder you're in timeout.", "'{msg}'? That's your broadcast? Canceled. Immediately.", "I've got 4K footage of you typing '{msg}'. It's going VIRAL."]},
    "Valentino": {"color": 0x8B008B, "dms": ["Darling, you're in timeout? How EMBARRASSING for you.", "I could get you out. For a price. But honestly? This is better entertainment.", "You look so helpless in there. I LOVE it.", "Contracts don't have timeout clauses, sweetheart. You're on your own.", "Maybe next time you'll think twice before breaking MY rules."], "roasts": ["'{msg}'? Darling, that's not a contract negotiation. That's a cry for help.", "You typed '{msg}' like you had leverage. You don't. You never did.", "'{msg}'? Cute. But I own your attention. And right now? You're boring me.", "Darling, '{msg}' is not the performance I was hoping for. Try again.", "'{msg}'? I've had better lines from background extras. And I killed them."]},
    "Velvette": {"color": 0xFF00FF, "dms": ["OMG this is SO going on my story! #TimeoutFail #GetRekted", "You're trending! Not for a good reason though. #Timeout", "I'm literally live-streaming this. Say hi to your fans!", "A timeout? How old-school. But the drama? CHEF'S KISS.", "Don't worry sweetie, I'll edit the footage to make you look even worse!"], "roasts": ["'{msg}'? Bestie, no. Delete this. Delete your whole account.", "'{msg}' is giving... desperate. And not the good kind of desperate.", "You typed '{msg}' and posted it? In THIS economy? Tragic.", "'{msg}'? The cringe is CRIMINAL. I'm posting this everywhere.", "Sweetie, '{msg}' is not the serve you think it is. It's a flop."]},
    "Carmilla Carmine": {"color": 0xC0C0C0, "dms": ["A timeout? I've put entire armies in timeout. You're not special.", "Use this time wisely. Reflect on your choices. Or don't. I don't care.", "I built an empire by learning from my mistakes. You? You're in timeout.", "Discipline is the foundation of power. You're learning the hard way.", "This is mercy. If I really wanted to punish you, you wouldn't be breathing."], "roasts": ["'{msg}'? I've conquered empires with better strategy than that.", "You wrote '{msg}' like it was a weapon. It's a toy.", "'{msg}'? That's your opening move? I've seen angels fight harder.", "I built an arms empire. '{msg}' wouldn't even qualify as a peashooter.", "'{msg}'? Weak. I've had more threatening conversations with my daughters."]},
    "Zestial": {"color": 0x2F4F2F, "dms": ["I have seen countless souls in timeout over the centuries. You are but one of many.", "Patience, young one. The timeout shall pass. The lesson? That remains.", "Time is the great teacher. And you have been given time. Use it wisely.", "I once put an overlord in timeout for a century. He came out a better demon.", "This too shall pass. But the memory of your shame? That lingers."], "roasts": ["'{msg}'? I have heard wiser words from newly fallen souls.", "Centuries I have watched. And '{msg}' is among the least impressive.", "'{msg}'? Time has witnessed many great words. These are not among them.", "Young one, '{msg}' reveals more about you than you realize. And it is not flattering.", "I have seen the rise and fall of empires. '{msg}' will be forgotten by sunrise."]},
    "Zeezi": {"color": 0x9370DB, "dms": ["A timeout? How quaint. I remember my first timeout. Centuries ago.", "The powerful don't get timeouts. They give them. Remember that.", "I've watched Hell's politics for eons. This is not the worst fate.", "Every overlord has been in timeout at some point. This builds character.", "Sit quietly. Think about your choices. Or don't. The outcome is the same."], "roasts": ["'{msg}'? I have watched Hell's politics for eons. That is not a strategy.", "You wrote '{msg}' like you had power. Adorable.", "'{msg}'? In the grand game of Hell, that move is checkmate in one. For your opponent.", "I've seen better plays from fresh souls. And they were eaten.", "'{msg}'? The powerful don't say things like that. You have proven you are not powerful."]}
}

CHARACTER_NAMES = list(CHARACTERS.keys())

@client.event
async def on_ready():
    log.info(f"Logged in as {client.user}")
    log.info(f"Connected to {len(client.guilds)} guild(s)")
    for g in client.guilds:
        log.info(f"  - {g.name} (ID: {g.id})")
    log.info(f"MOD_CHANNEL_ID: {MOD_CHANNEL_ID}")
    mod_channel = client.get_channel(MOD_CHANNEL_ID)
    if mod_channel:
        log.info(f"Mod channel found: {mod_channel.name}")
    else:
        log.warning(f"Mod channel {MOD_CHANNEL_ID} not found! Check MOD_CHANNEL_ID variable.")

@client.event
async def on_member_update(before, after):
    if before.timed_out_until != after.timed_out_until and after.timed_out_until is not None:
        log.info(f"{after.display_name} was timed out until {after.timed_out_until}")
        char_name = random.choice(CHARACTER_NAMES)
        char = CHARACTERS[char_name]
        taunt = random.choice(char["dms"])
        try:
            dm = await after.create_dm()
            embed = discord.Embed(title=f"{char_name} says...", description=taunt, color=char["color"])
            embed.set_footer(text="You've been timed out. The characters are watching. Try replying if you dare.")
            await dm.send(embed=embed)
            log.info(f"DM sent to {after.display_name} from {char_name}")
        except discord.Forbidden:
            log.warning(f"Could not DM {after.display_name} - DMs closed")
        except Exception as e:
            log.error(f"Error DMing {after.display_name}: {e}")
        mod_channel = client.get_channel(MOD_CHANNEL_ID)
        if mod_channel:
            mod_embed = discord.Embed(title=f"{char_name} taunted {after.display_name}", description=f"**User:** {after.mention} ({after.display_name})\n**Taunt:** {taunt}", color=char["color"])
            mod_embed.set_footer(text="They think it's a private DM. Let them.")
            await mod_channel.send(embed=mod_embed)
            log.info(f"Posted taunt to mod channel for {after.display_name}")
        else:
            log.warning(f"Mod channel {MOD_CHANNEL_ID} not found - can't post taunt")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if isinstance(message.channel, discord.DMChannel):
        log.info(f"DM received from {message.author.name}: {message.content}")
        found_member = None
        found_guild = None
        for guild in client.guilds:
            member = guild.get_member(message.author.id)
            if member and member.timed_out_until and member.timed_out_until > discord.utils.utcnow():
                found_member = member
                found_guild = guild
                break
        if found_member:
            char_name = random.choice(CHARACTER_NAMES)
            char = CHARACTERS[char_name]
            roast = random.choice(char["roasts"]).replace("{msg}", message.content[:100])
            embed = discord.Embed(title=f"{char_name} fires back!", description=roast, color=char["color"])
            embed.set_footer(text=f"Keep talking. They're loving this.")
            await message.channel.send(embed=embed)
            log.info(f"Roasted {found_member.display_name} with {char_name}: {roast}")
            mod_channel = client.get_channel(MOD_CHANNEL_ID)
            if mod_channel:
                mod_embed = discord.Embed(title=f"{char_name} roasted {found_member.display_name}", description=f"**User said:** {message.content}\n**Guild:** {found_guild.name}\n**Roast:** {roast}", color=char["color"])
                mod_embed.set_footer(text="The conversation continues...")
                await mod_channel.send(embed=mod_embed)
        else:
            log.info(f"{message.author.name} sent DM but is not currently timed out")

client.run(DISCORD_TOKEN)
