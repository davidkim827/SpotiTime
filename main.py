from config import sp
import sys
from datetime import datetime
import time

"""Make sure to be playing something on a device and this script chooses the current device in play to run on"""

results = sp.current_user_playlists(limit=50)
all_playlists = dict(sorted({item.get("name").lower(): item.get("uri") for item in results["items"]}.items(), key=lambda x: x[0]))
inverted_all_playlists = {v: k for k, v in all_playlists.items()}


def get_playlists_to_play():
    return_playlists = []

    count = 1
    choices = {}
    for playlist in all_playlists.keys():
        choices[count] = playlist
        print(f"{count}. {playlist}")
        count += 1

    print(
        "Please type the number for the playlists that you would like to have played at certain times," +
        " delimited by commas (e.g. 1,2,3,7)\n"
    )
    for playlist_num in input("Playlists: ").split(","):
        return_playlists.append(choices.get(int(playlist_num)))
    return tuple(return_playlists)


def create_playlist_dict(playlists=()):
    if not playlists:
        return "No playlists to be found."

    playlists_dict = {}
    for playlist in playlists:
        playlist_id = all_playlists.get(playlist)
        if not playlist_id:
            print(f"Could not find playlist name: {playlist}")
            if input(f"Continue? Y/N").lower() == "n":
                sys.exit(0)
            print(f"Continuing without playlist: {playlist}")
            continue
        playlists_dict[playlist] = playlist_id

    return playlists_dict


def build_timed_playlist():
    id_time_dict = {}

    for playlist, id_ in create_playlist_dict(get_playlists_to_play()).items():
        print(
            "\n\nPlease type in what time you would like to have this playlist scheduled to play (e.g. 8:00pm | 7:30am | now) \n"
        )
        time = input(f"{playlist}: ")
        if time.lower() == "now":
            time = datetime.now().strftime("%Y %m %d %I:%M%p")
        else:
            time = datetime.now().date().strftime("%Y %m %d") + f" {time}"

        time = datetime.strptime(time.strip().upper(), "%Y %m %d %I:%M%p")
        id_time_dict[id_] = time
    return id_time_dict

def play_timed_playlists(playlist_ordered):
    stop = False
    while not stop:
        for playlist_element in range(len(playlist_ordered)):
            try:
                next_playlist_info = playlist_ordered[playlist_element + 1]
                next_playlist_time = next_playlist_info[1]
            except:
                next_playlist_time = 0

            current_playlist_info = playlist_ordered[playlist_element]
            curr_uri = current_playlist_info[0]
            curr_playlist_time = current_playlist_info[1]

            now = datetime.now()
            while now < curr_playlist_time:
                now = datetime.now()
                time.sleep(5)

            print(f"Now playing: {inverted_all_playlists.get(curr_uri)}")
            sp.volume(volume_percent=30)
            sp.start_playback(context_uri=curr_uri)
            sp.repeat(state="context")
            sp.shuffle(state=True)
            if not next_playlist_time:
                break
            sleep_time = (next_playlist_time - curr_playlist_time).total_seconds()
            time.sleep(sleep_time - 300) if sleep_time - 300 >= 0 else time.sleep(0)
        stop = input("Type out 'STOP' to stop\n")
        if stop.lower() == "stop":
            stop = True

    sp.pause_playback()


p = build_timed_playlist()
playlists_ordered = sorted(p.items(), key=lambda x: x[1])
play_timed_playlists(playlists_ordered)

