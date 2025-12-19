from datetime import datetime, timezone

from .utils import get_time_log_channel, is_join, is_leave, build_duration_message
from integration.saving import save_voice_session

async def record_voice_time(bot, cfg, member, before, after):
	# Member joined
	if is_join(before, after, cfg):
		category_name = after.channel.category.name
		voice_channel_name = after.channel.name
		text_channel = get_time_log_channel(member, category_name.lower(), cfg)
		if text_channel:
			msg = await text_channel.send(f"{member.mention} started: {category_name} - {voice_channel_name}")
		return

	# Member left
	if is_leave(before, after, cfg):
		category_name = before.channel.category.name
		voice_channel_name = before.channel.name
		text_channel = get_time_log_channel(member, category_name.lower(), cfg)
		if not text_channel:
			return

		# Find last message announcing this member started in this channel
		async for msg in text_channel.history(limit=50, oldest_first=False):
			if (
				msg.author == bot.user
				and member.mention in msg.content
				and f"{category_name} - {voice_channel_name}" in msg.content
			):
				start_time = msg.created_at.replace(tzinfo=timezone.utc)
				end_time = datetime.now(timezone.utc)

				print("[debug]: save voice session")

				try:
					save_voice_session(
						category=category_name,
						subcategory=voice_channel_name,
						start_time=start_time,
					)
				except Exception as err:
					print(f"[error]: save_voice_session failed: {err}")

				print("[debug]: printing duration message")

				duration_message = build_duration_message(member, start_time, category_name, voice_channel_name)
				
				await msg.delete()
				await text_channel.send(duration_message)
				break
