from telethon import TelegramClient
import telethon.sync
import functools
import json
import time


with open('config.json') as config_file:
    data = json.load(config_file)


client = TelegramClient(
	data['session_name'],
	data['api_id'],
	data['api_hash']
)


def client_session(func):
    @functools.wraps(func)
    def action(*args, **kwargs):
        with client:
            result = func(client, *args, **kwargs)
        return result
    return action