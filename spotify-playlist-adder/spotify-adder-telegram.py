import spotipy
import spotipy.util as util
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, ConversationHandler, \
    MessageHandler, Filters

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
        # print(f"Adding {selected_track[0]} to saved tracks")
        write_scoped.current_user_saved_tracks_add(tracks=[selected_track[2]])

    except ValueError as error:
        ...
        # print(f"Invalid number entered. Error code {error}")


SEARCH, ADD = range(2)


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Works with spotify saved tracks to edit/display the list\n'
                              '/savedtracks - list saved tracks\n'
                              '/searchtrack - to search on Spotify\n'
                              '/exit - to stop service')


def list_saved(update: Update, context: CallbackContext):
    tracks = read_saved_tracks()
    for track in tracks:
        update.message.reply_text(f"{track[0]} by {track[1]}")


def search_start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Enter track to search')
    return SEARCH


def search_track(update: Update, context: CallbackContext):
    # user = update.message.from_user
    search_item = update.message.text
    # print(search_item)
    global found_tracks
    found_tracks = (search_result_for_input(search_item))
    found_enum = enumerate(found_tracks)
    for index, item in found_enum:
        update.message.reply_text(f"{index}. {item[0]} by {item[1]}")
    # update.message.reply_text('Enter index of track to be added')
    return ADD


def add_track(update: Update, context: CallbackContext):
    track = update.message.text
    save_new_track(found_tracks, track)
    update.message.reply_text('Track added')


def exit_bot(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Happy Listening.', reply_markup=ReplyKeyboardRemove)

    return ConversationHandler.END


def main():
    updater = Updater(token='1801205710:AAG_u35YPurhunzTEnEFLyyTRvYRlYTB2Xw', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('savedtracks', list_saved))
    track_handler = ConversationHandler(
        entry_points=[CommandHandler('searchtrack', search_start)],
        states={
            SEARCH: [MessageHandler(Filters.text and ~Filters.command, search_track)],
            ADD: [MessageHandler(Filters.text and ~Filters.command, add_track)]
        },
        fallbacks=[None],
    )
    dp.add_handler(track_handler)
    dp.add_handler(CommandHandler('exit', exit_bot))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
