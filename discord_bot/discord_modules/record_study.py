from dotenv import load_dotenv
import os
from datetime import datetime, timezone
import pytz  # For timezone conversion


load_dotenv()
STUDY_ROLE_ID = int(os.getenv("STUDY_ROLE_ID"))
STUDY_CHANNEL_ID = int(os.getenv("STUDY_CHANNEL_ID"))

SYDNEY_TZ = pytz.timezone("Australia/Sydney")

async def record_study_on_voice(bot, member, before, after):
    role = member.guild.get_role(STUDY_ROLE_ID)
    text_channel = member.guild.get_channel(STUDY_CHANNEL_ID)

    if role is None:
        print(f"Study role ID not found.")
    if text_channel is None:
        print(f"Study channel ID not found.")
    
    if _member_joins_study_vc(before, after):
        if role not in member.roles:
            await member.add_roles(role)
            await text_channel.send(f"{member.mention} started studying.")
    elif _member_leaves_study_vc(before, after):
        if role in member.roles:
            await member.remove_roles(role)
        async for msg in text_channel.history(limit=50, oldest_first=False):
            if msg.author == bot.user and member.mention in msg.content:
                string = _duration_string_maker(msg.created_at, member)
                await msg.delete()
                await text_channel.send(string)
                break
        else:
            print(f"started studying message not found")

def _member_joins_study_vc(before, after):
    if after.channel is None:
        return False
    
    if after.channel.id != STUDY_CHANNEL_ID:
        return False
    
    if before.channel == after.channel:
        return False
    
    return True

def _member_leaves_study_vc(before, after):
    if before.channel is None:
        return False
    
    if before.channel.id != STUDY_CHANNEL_ID:
        return False
    
    if after.channel is None:
        return True
    
    if after.channel.id != STUDY_CHANNEL_ID:
        return True
    
    return False

def _duration_string_maker(start_time, member) -> str:
    """
    Docstring for duration_string_maker
    
    :param start_time: time the start message is created, e.g. msg.created_at
    :return: message to send in study voice channel
    :rtype: str
    """
    start_t = start_time.replace(tzinfo=timezone.utc).astimezone(SYDNEY_TZ)
    end_t = datetime.now(timezone.utc).astimezone(SYDNEY_TZ)

    duration = end_t - start_t
    minutes, seconds = divmod(duration.total_seconds(), 60)

    string = f"{member.mention} completed a study block.\n"
    string += f"Start: {start_t.strftime('%H:%M:%S')}.\n"
    string += f"End: {end_t.strftime('%H:%M:%S')}.\n"
    string += f"Total Duration: {int(minutes)} minutes and {int(seconds)} seconds."

    return string