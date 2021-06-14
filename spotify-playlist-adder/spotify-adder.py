import spotipy
import spotipy.util as util

"""
execute the following commands in the terminal before running the script (get values from dev console @spotify)
export SPOTIPY_CLIENT_ID='f179b87f993a4202af1df06d722f2637'
export SPOTIPY_CLIENT_SECRET='afe14e0cc70747fcb41b3bae56c3da29'
export SPOTIPY_REDIRECT_URI='http://localhost:8080'
"""

# creating spotipy instance with read and write scope
username = "31y5yewyo4dp3aratpdqxy4lqd2u"
# noinspection PyDeprecation
read_token = util.prompt_for_user_token(username, "user-library-read")
read_scoped = spotipy.Spotify(auth=read_token)

# noinspection PyDeprecation
write_token = util.prompt_for_user_token(username, "user-library-modify")
write_scoped = spotipy.Spotify(auth=write_token)


def select_info(track_list):
    tracks_info = []

    # json file returned for search result and saved tracks cannot be used in same way
    # therefore, we change 'tracks' when search is performed, to "items" from the json file
    # refer json file for more
    tracks = track_list.get("tracks")
    if tracks is not None:
        tracks = tracks["items"]
    else:
        tracks = [track["track"] for track in track_list["items"]]

    if tracks is None:
        return tracks_info

    for track in tracks:
        track_name = track["name"]
        artist = track["artists"][0]["name"]
        track_id = track["id"]

        tracks_info.append((
            track_name,
            artist,
            track_id
        ))

    return tracks_info


def read_saved_tracks():
    saved_tracks = read_scoped.current_user_saved_tracks()
    track_info = select_info(saved_tracks)
    return track_info


def search_result_for_input(search_item):
    search_result = read_scoped.search(search_item)
    search_tracks = select_info(search_result)

    return search_tracks


def save_new_track(found_item, selection):
    try:
        parsed_select = int(selection)
        selected_track = found_item[parsed_select]
        print(f"Adding {selected_track[0]} to saved tracks")
        write_scoped.current_user_saved_tracks_add(tracks=[selected_track[2]])

    except ValueError as error:
        print(f"Invalid number entered. Error code {error}")


def main():
    run = True
    while run:
        print("0. Saved Tracks\n1. Add new track\n2. Exit")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
            if choice == 0:
                tracks = read_saved_tracks()
                for track in tracks:
                    print(f"{track[0]} by {track[1]}")

            if choice == 1:
                search_item = input("Enter track to search: ")
                found_item = search_result_for_input(search_item)
                for index, item in enumerate(found_item):
                    print(f"{index}. {item[0]} by {item[1]} ({item[2]})")
                selection = input("Enter index of correct track: ")

                save_new_track(found_item, selection)

            if choice == 2:
                # exit the loop
                run = False

        except ValueError as error:
            print(f"Enter valid number. Error: {error}")




if __name__ == "__main__":
    main()
