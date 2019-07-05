from telegram import get_group_all_members, user_engagement, get_all_dialogs


def get_all_groups(dialog_list):
	result = []
	for dialog in dialog_list:
		if dialog.is_group:
			result.append(dialog)
	return result


def get_all_users(dialog_list):
	result = []
	for dialog in dialog_list:
		if dialog.is_user:
			result.append(dialog)
	return result


def remove_all_bots(dialog_list):
	from telethon.tl.types import User
	from telethon.tl.custom.dialog import Dialog

	result = []
	for dialog in dialog_list:
		dialog_condition =  (isinstance(dialog, Dialog) and 
							 dialog.entity.to_dict().get('bot'))
		user_condition = (isinstance(dialog, User) and 
							 dialog.bot)
		if dialog_condition or user_condition:
			continue
		result.append(dialog)
	return result


def all_of_all_user_ids(dialog_list):
	result = []
	for dialog in dialog_list:
		if dialog.is_group:
			group_members =  remove_all_bots(
				get_group_all_members(
					dialog.id
				)
			)
			group_members = [member.id for member in group_members]
			result = result + group_members
		
		elif dialog.is_user:
			result.append(dialog.id)

	return list(set(result))


def get_more_engaged_users(group, total=1000, top=10):
	group = group.replace('@', '') if isinstance(group, str) else group
	result = user_engagement(group, total)
	group = result.pop('group_entity')
	user_list = [result[i] for i in result]
	user_list = sorted(
		user_list,
		key=lambda d: d['engagement'],
		reverse=True
	)
	return user_list[:top], group