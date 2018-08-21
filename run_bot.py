from discord import Message, Member
from discord.ext.commands import Bot, when_mentioned_or, Context
from data import cfg
from datetime import datetime

bot = Bot(when_mentioned_or(cfg.command_prefix))

last_dynamic_time: datetime = datetime.min
dynamic_min_interval_seconds = 600
dynamic_trigger_id = '253452911722364928'
dynamic_response = 'dynamic is best type, it should be the only type in C#'


@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}')


@bot.event
async def on_message(msg: Message):
    global last_dynamic_time

    await bot.process_commands(msg)

    if any(m.id == dynamic_trigger_id for m in msg.mentions) and (
            datetime.now() - last_dynamic_time).total_seconds() >= dynamic_min_interval_seconds:
        last_dynamic_time = datetime.now()
        await bot.send_message(msg.channel, dynamic_response)


@bot.command('nick', pass_context=True)
async def cmd_nick(ctx: Context, nick=None):
    if not nick:
        return await bot.reply('missing the new nickname')

    await bot.change_nickname(ctx.message.server.get_member(bot.user.id), nick)


bot.run(cfg.oauth)
