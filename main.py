import requests
import time

def get_cookie():
    print("type your cookie")
    cookie = input("> ").strip()
    return cookie


def get_csrf_token(session):
    r = session.post("https://auth.roblox.com/v2/logout")
    return r.headers.get("x-csrf-token")


def get_friends(session, user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
    r = session.get(url)
    r.raise_for_status()
    return r.json().get("data", [])


def unfriend(session, friend_id):
    url = f"https://friends.roblox.com/v1/users/{friend_id}/unfriend"
    r = session.post(url)
    return r.status_code == 200


def main():
    cookie = get_cookie()

    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie
    session.headers.update({"Referer": "https://www.roblox.com"})

    # get x-csrf token
    print("generating x-csrf token")
    csrf = get_csrf_token(session)
    if not csrf:
        print("couldn't get the x-csrf token, maybe invalid cookie?")
        return
    session.headers["x-csrf-token"] = csrf

    # checking cookie
    print("validating cookie")
    r = session.get("https://users.roblox.com/v1/users/authenticated")
    if r.status_code != 200:
        print("invalid cookie")
        return

    user_data = r.json()
    user_id = user_data["id"]
    username = user_data["name"]
    print(f"logged as: {username} (id: {user_id})")

    # search for the friend list
    print("searching for friend list")
    friends = get_friends(session, user_id)

    print(f"you have {len(friends)} friends")

    # remove all friends
    for f in friends:
        print(f"removing: {f['name']} (id: {f['id']})...", end="")
        ok = unfriend(session, f["id"])
        if ok:
            print(" ✔")
        else:
            print(" ❌")
        time.sleep(1)  # you can edit that but i dont think its necessary

    print("\n all friends got removed")


if __name__ == "__main__":
    main()
