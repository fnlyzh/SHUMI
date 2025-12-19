from datetime import timedelta

def merge_sessions(sessions, merge_gap_minutes, min_duration_minutes):
	"""
	Merge consecutive sessions in the same category/subcategory if the gap is <= merge_gap_minutes.
	Drop sessions shorter than min_duration_minutes after merging.
	"""
	if sessions is None:
		return []

	sessions.sort(key=lambda s: s.start_time)
	merged = [sessions[0]]

	for s in sessions[1:]:
		last = merged[-1]
		if (s.category == last.category and s.subcategory == last.subcategory and
			(s.start_time - last.end_time) <= timedelta(minutes=merge_gap_minutes)):
			# merge
			last.end_time = max(last.end_time, s.end_time)
		else:
			merged.append(s)

	# filter out short sessions
	final_sessions = [
		s for s in merged
		if (s.end_time - s.start_time).total_seconds() / 60 >= min_duration_minutes
	]
	return final_sessions
