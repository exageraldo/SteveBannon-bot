from helpers import (get_all_groups, get_all_users, remove_all_bots,
					 all_of_all_user_ids, get_more_engaged_users)
from telegram import (send_message, get_group_all_members,
					  send_image, get_all_dialogs)


class SteveBannonClient(object):
	
	@staticmethod
	def send_message_to_all_groups(text):
		all_dialogs = get_all_dialogs()
		all_groups = get_all_groups(all_dialogs)
		for group in all_groups:
			send_message(group.id, text)

	@staticmethod
	def send_message_to_all_people(text):
		all_dialogs = get_all_users()
		all_users = get_all_users(all_dialogs)
		all_users = remove_all_bots(all_users)
		for user in all_users:
			send_message(user.id, text)

	@staticmethod
	def send_image_to_all_groups(path_to_image, caption=None):
		all_dialogs = get_all_dialogs()
		all_groups = get_all_groups(all_dialogs)
		all_groups = [group.id for group in all_groups]
		end_image(all_groups, path_to_image, caption)

	@staticmethod
	def send_image_to_all_people(path_to_image, caption=None):
		all_dialogs = get_all_users()
		all_users = get_all_users(all_dialogs)
		all_users = remove_all_bots(all_users)
		all_users = [user.id for user in all_users]
		send_image(all_users, path_to_image, caption)

	@staticmethod
	def send_message_brute_force(text):
		all_dialogs = get_all_users()
		all_users = all_of_all_user_ids(all_dialogs)
		for user_id in all_users:
			send_message(user_id, text)

	@staticmethod
	def send_image_brute_force(path_to_image, caption=None):
		all_dialogs = get_all_users()
		all_users_id = all_of_all_user_ids(all_dialogs)
		send_image(all_users_id, path_to_image, caption)

	@staticmethod
	def get_group_more_engaged(groups=None, total=1000, show=10):
		groups = groups if isinstance(groups, list) else [groups]
		if not groups:
			all_dialogs = get_all_dialogs()
			groups = [g.id for g in get_all_groups(all_dialogs)]
		for group in groups:
			users, group = get_more_engaged_users(group, total, show)
			print(group.title)
			for index, user in enumerate(users):
				user_ = user['entity']
				print(
					f'{index+1} - {user_.first_name}'
					f' (@{user_.username})'
					f' {user['count']}/{total}'
				)