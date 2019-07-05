from config import client_session
import time


@client_session
def send_message(client, chat, text, loop=1, sleep_time=0.5):
    chat = chat.replace('@', '') if isinstance(chat, str) else chat
    for _ in range(loop):
        client.send_message(
            chat, 
            text
        )
        time.sleep(sleep_time)


@client_session
def send_image(client, chat_list, path_to_image, caption=None, sleep_time=0.5):
    chat_list = chat_list if isinstance(chat_list, list) else [chat_list]
    file = client.upload_file(path_to_image)
    for chat in chat_list:
        client.send_file(chat, file, caption=caption)
        time.sleep(sleep_time)


@client_session
def get_group_all_members(client, group, to_dict=False):
    all_members = client.get_participants(
        group,
        aggressive=True
    )
    if to_dict:
        all_members = [member.to_dict() for member in all_members]

    return all_members


@client_session
def get_all_dialogs(client, limit=None, to_dict=False):
    all_dialogs = client.get_dialogs(limit=limit)

    if to_dict:
        all_dialogs = [dialog.to_dict() for dialog in all_dialogs]

    return all_dialogs


@client_session
def user_engagement(client, group, total=1000, ignore_bot=True, sleep_time=0.75):
    data = {}
    for m in client.iter_messages(group, limit=total):
        sender = m.sender
        if ignore_bot and sender.bot:
            continue
        if sender.id in data:
            data[sender.id]['count'] += 1
            data[sender.id]['engagement'] = data[sender.id]['count']/total
        else:
            data[sender.id] = {
                'id': sender.id,
                'entity': client.get_entity(sender.id),
                'count': 1,
                'last_msg': m.date,
                'engagement': 1/total
            }
            time.sleep(sleep_time)
            data['group_entity'] = client.get_entity(group)
            time.sleep(sleep_time)
    return data