# %%
from dotenv import load_dotenv
import os
from atproto import Client
from utils import (
    fetch_list_member_profiles,
    user_list_url_to_uri,
    starter_pack_url_to_uri,
    get_users_from_starter_pack,
    get_follows,
)
import pandas as pd

# %%
# take environment variables from .env and asign
load_dotenv()
usr, pwd = os.getenv("bsky_usr"), os.getenv("bsky_pwd")

# Instantiate the client and login
client = Client()
client.login(usr, pwd)


# Thirsk and Malton lists:
with open("tnm_lists.txt", "r") as f:
    tnm_lists = [i.strip() for i in f.readlines() if i.startswith("https")]

# %%
profiles = []
for url in tnm_lists:
    profiles.extend(get_users_from_starter_pack(client, url))

# %%
from tqdm import tqdm

profile_dicts = []
relations = []
for profile in tqdm(profiles):
    # Get basic profile information and add to profile_dicts
    profile_dict = dict(profile)

    # Drop object keys
    for key in ["associated", "viewer"]:
        profile_dict.pop(key, None)

    profile_dicts.append(profile_dict)

    follows = get_follows(client, profile.did)
    follow_dids = [follow.did for follow in follows]

    for did in follow_dids:
        relations.append({"source": profile.did, "target": did})

profile_dicts[0]

nodes = pd.DataFrame(profile_dicts)
edges = pd.DataFrame(relations)
# %%

# %%

# %%

follows = client.get_follows(profiles[0].did)

# %%
from utils import paginated_fetch


follows = get_follows(client, profiles[0].did)
# %%
len(follows)
# %%
profiles[0]
# %%
profile_dicts[0]
# %%
