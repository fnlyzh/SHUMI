from datetime import datetime, timezone

def get_time_log_channel(member, category_name, cfg):
    """
    Returns the time-log text channel for a category.
    precondition: cfg.channels[category_name]['time_log'] stores the ID of the text channel.
    """
    try:
        text_channel_id = cfg.channels[category_name]["time_log"]
    except IndexError:
        raise IndexError(f"time-log channel under '{category_name}' does not exist")
    return member.guild.get_channel(text_channel_id)

def is_join(before, after, cfg):
    """Returns True if member joined a tracked VC in cfg"""
    if after.channel is None:
        return False
    category_name = after.channel.category.name.lower()
    if category_name not in cfg.channels:
        return False
    if before.channel == after.channel:
        return False
    return True

def is_leave(before, after, cfg):
    """Returns True if member left a tracked VC in cfg"""
    if before.channel is None:
        return False
    category_name = before.channel.category.name.lower()
    if category_name not in cfg.channels:
        return False
    if after.channel == before.channel:
        return False
    return True

def build_duration_message(member, start_time, category, voice_channel):
    # can use any time zone because we be doing duration
    start_utc = start_time.replace(tzinfo=timezone.utc)
    end_utc = datetime.now(timezone.utc)
    duration = end_utc - start_utc

    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours == 0 and minutes == 0:
        duration_str = f"{int(seconds)} seconds"
    else:
        duration_str = f"{int(hours)} hours and {int(minutes)} minutes"

    return f"{member.mention} completed: {category} - {voice_channel}. Duration: {duration_str}"
