# %%
from dotenv import load_dotenv
import os
from atproto import Client
from utils import get_users_from_starter_pack

load_dotenv()  # take environment variables from .env.

usr, pwd = os.getenv("bsky_usr"), os.getenv("bsky_pwd")

client = Client()
client.login(usr, pwd)


mp_list = "https://bsky.app/starter-pack/alexrosecharity.bsky.social/3laf2u2ybnm2k"


users = get_users_from_starter_pack(client, mp_list)
