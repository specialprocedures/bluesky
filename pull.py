# %%
from dotenv import load_dotenv
import os
from atproto import Client
from utils import get_users_from_starter_pack

# take environment variables from .env and asign
load_dotenv()
usr, pwd = os.getenv("bsky_usr"), os.getenv("bsky_pwd")

# Instantiate the client and login
client = Client()
client.login(usr, pwd)


mp_list = "https://bsky.app/starter-pack/alexrosecharity.bsky.social/3laf2u2ybnm2k"

users = get_users_from_starter_pack(client, mp_list)

# %%
users
# %%
len(users)
# %%
type(users[0][1])
# %%
