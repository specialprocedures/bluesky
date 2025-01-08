def starter_pack_url_to_uri(url: str) -> str:
    """
    Converts a BlueSky URL to a URI for use with the atproto library.

    Args:
        url (str): The BlueSky starter-pack URL to convert.

    Returns:
        str: The converted URI.

    Raises:
        ValueError: If the URL does not match the expected BlueSky starter-pack structure.
    """
    if "bsky.app/starter-pack/" not in url:
        raise ValueError(
            "URL does not match the expected BlueSky starter-pack structure."
        )

    # Split the URL into domain and identifier
    parts = url.split("bsky.app/starter-pack/")
    if len(parts) != 2:
        raise ValueError("Unexpected URL format.")

    domain_and_identifier = parts[1]
    try:
        domain, identifier = domain_and_identifier.split("/", 1)
    except ValueError:
        raise ValueError("Invalid domain or identifier in the URL.")

    # Construct and return the URI
    return f"at://{domain}/app.bsky.starterPack/{identifier}"


def user_list_url_to_uri(client, url: str) -> str:
    """
    Converts a BlueSky URL to a URI for use with the atproto library.

    Args:
        url (str): The BlueSky list URL to convert.
        E.g. https://bsky.app/profile/dangreenjourno.bsky.social/lists/3laobag2a5f27

    Returns:
        str: The converted URI.

    Raises:
        ValueError: If the URL does not match the expected BlueSky list structure.
    """

    if "bsky.app/profile/" not in url or "/lists/" not in url:
        raise ValueError("URL does not match the expected BlueSky list structure.")

    user, domain, identifier = url.split("/")[-3:]

    did = client.resolve_handle(user).did

    return f"at://{did}/app.bsky.graph.list/{identifier}"


def paginated_fetch(endpoint, params=None):
    """
    Fetches all items from a paginated endpoint.

    Args:
        endpoint: The endpoint to fetch data from.
        params (dict): Optional parameters to pass to the endpoint.

    Returns:
        list: A list of items from the paginated endpoint.
    """
    cursor = None
    items = []

    while True:
        # Fetch data from the endpoint
        response = endpoint(params={**params, "cursor": cursor})

        if endpoint.__name__ == "get_list":
            items.extend(response.items)

        elif endpoint.__name__ == "get_follows":
            follows = response.follows
            items.extend(follows)
        else:
            raise ValueError("Invalid endpoint.")

        cursor = response.cursor

        # Break the loop if there are no more items to fetch
        if not cursor:
            break

    return items


def fetch_list_member_profiles(client, uri: str) -> list:
    """
    Fetches all members of a BlueSky list using cursor-based pagination.
    """
    list_members = paginated_fetch(
        client.app.bsky.graph.get_list, params={"list": uri, "limit": 30}
    )

    handles = [member.subject.handle for member in list_members]

    # The client.get_profiles() method is capped at 25 handles per request
    profiles = []
    for i in range(0, len(handles), 25):
        profile_tup = client.get_profiles(handles[i : i + 25])
        profiles.extend(profile_tup["profiles"])

    return profiles


def get_users_from_list(client, url: str) -> list:
    """
    Retrieves all users from a BlueSky list.

    Args:
        client: The atproto client object for API interaction.
        url (str): The BlueSky list URL.

    Returns:
        list: A list of users included in the list.

    Raises:
        ValueError: If the URL conversion or list fetching fails.
    """
    # Convert the list URL to a URI
    uri = user_list_url_to_uri(client, url)

    # Fetch and return members from the list
    return fetch_list_member_profiles(client, uri)


def get_users_from_starter_pack(client, url: str) -> list:
    """
    Retrieves all users from a BlueSky starter pack.

    Args:
        client: The atproto client object for API interaction.
        url (str): The BlueSky starter-pack URL.

    Returns:
        list: A list of users included in the starter pack.

    Raises:
        ValueError: If the URL conversion or list fetching fails.
    """
    # Convert the starter pack URL to a URI
    uri = starter_pack_url_to_uri(url)

    # Fetch the starter pack metadata
    starter_pack = client.app.bsky.graph.get_starter_pack(params={"starterPack": uri})
    starter_list_uri = starter_pack.starter_pack.list.uri

    # Fetch and return members from the starter pack list
    return fetch_list_member_profiles(client, starter_list_uri)


def get_follows(client, did: str) -> list:
    """
    Retrieves all users that a given user follows.

    Args:
        client: The atproto client object for API interaction.
        did (str): The user's DID.

    Returns:
        list: A list of users that the given user follows.

    """
    follows = paginated_fetch(
        client.app.bsky.graph.get_follows, params={"actor": did, "limit": 30}
    )

    return follows
