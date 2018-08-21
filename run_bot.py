from discord import Message, Member
from discord.ext.commands import Bot, when_mentioned_or, Context
from data import cfg
from datetime import datetime, timedelta

bot = Bot(when_mentioned_or(cfg.command_prefix))

last_dynamic_time: datetime = datetime.min

dynamic_interval_seconds = 3600

dynamic_trigger_id = '253452911722364928'
dynamic_resp = 'dynamic is best type, it should be the only type in C#'

enabled = True


def can_toggle_bot_enabled(user: Member):
    return user.id == '175734927273361408'


def is_mentioned(id_, msg):
    return any(m.id == id_ for m in msg.mentions)


def time_passed_from(dt, time):
    return (datetime.now() - dt).total_seconds() >= time


@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}')


@bot.event
async def on_message(msg: Message):
    global last_dynamic_time

    if not enabled and not (msg.content.startswith('!on') or msg.content.startswith('!off')):
        return

    await bot.process_commands(msg)

    if is_mentioned(dynamic_trigger_id, msg) and time_passed_from(last_dynamic_time, dynamic_interval_seconds):
        last_dynamic_time = datetime.now()
        await bot.send_message(msg.channel, dynamic_resp)


@bot.command('nick', pass_context=True)
async def cmd_nick(ctx: Context, nick=None):
    if not nick:
        return await bot.reply('missing the new nickname')

    await bot.change_nickname(ctx.message.server.get_member(bot.user.id), nick)


@bot.command('ripmod')
async def cmd_rip_mod(*ignored):
    await bot.say('Master Yi is skillful champ')


@bot.command('on', pass_context=True)
async def cmd_on(ctx, *ignored):
    global enabled
    enabled = True

    if not can_toggle_bot_enabled(ctx.message.author):
        return await bot.reply('only Axiom_Infinite can use this command')

    await bot.say('bot has been enabled')


@bot.command('off', pass_context=True)
async def cmd_off(ctx, *ignored):
    global enabled

    if not can_toggle_bot_enabled(ctx.message.author):
        return await bot.reply('only Axiom_Infinite can use this command')

    enabled = False

    await bot.say('bot has been disabled')


bot.run(cfg.oauth)
