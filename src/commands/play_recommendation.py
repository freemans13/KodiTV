from threading import Timer
import mysql.connector
from src.utils.series_info import series_info
from src.utils.find_and_delete_recordings import find_and_delete_recordings
from src.utils.KodiResource import KodiResource
import src.parameters as parameters


def play_something(title=None):
    connection = mysql.connector.connect(user=parameters.DB_USER, database=parameters.DB_NAME)
    cursor = connection.cursor()

    select_season_info = ("select s.show_id, e.season, max(e.episode) last_episode "
                          "from shows s "
                          "inner join episodes e on s.show_id = e.show_id "
                          "where s.title = %s "
                          "group by s.show_id, e.season "
                          "order by e.season desc "
                          "limit 1; ")

    cursor.execute(select_season_info, (title,))
    next_episode = 0
    for (show_id, season, last_episode) in cursor:
        next_episode = last_episode + 1
        print("seen", season, last_episode, "looking for", season, next_episode)
    kodi = KodiResource()
    record_dict = kodi.pvr_get_recordings()

    resume_current = False
    player_recording = None
    recording_ids = []
    if next_episode > 0:
        print("Check for new episode...")
        for record in record_dict:
            # print(record)
            if record['label'].lower() == title.lower():
                # print(record['label'], record['recordingid'])
                recording_ids.append(record['recordingid'])
        record_details_dict = kodi.pvr_get_recording_details_batch(recording_ids)

        for line in record_details_dict:
            episode_dict = series_info(line['plot'])

            if episode_dict['episode'] < next_episode - 2:
                find_and_delete_recordings(line['label'], plot=line['plot'])

            if episode_dict['episode'] == next_episode - 1 and line['resume']['position'] > 0:
                print("Resume current episode", next_episode - 1)
                player_recording = {"id": line['recordingid'], "title": line['label']}
                resume_current = True

            if episode_dict['episode'] == next_episode:
                print("Found next episode", next_episode)
                player_recording = {"id": line['recordingid'], "title": line['label']}

        if not player_recording:
            print("No unwatched future episodes")

    if not player_recording and len(record_dict) > 0:
        # for recording in record_dict:
        player_recording = {"id": record_dict[0]['recordingid'],
                            "title": record_dict[0]['label']}
    if player_recording:
        print('Playing', player_recording['title'])
        if resume_current:
            # Kodi asks user if they want to start from beginning or to resume, by default it highlights the resume
            # option, therefore we want send a post to "select" current choice. This is my hack for getting around
            # Kodi's api limitation in that there is no command to skip the option. The delay is because our player.open
            # post doesnt give a response until the set programme is being played, so we create a timer delay ,rather
            # than a time.sleep, for the select request to run despite there no request
            # after given seconds for Kodi to catch up
            t = Timer(2.0, kodi.input_select)
            t.start()
            print("play")
            kodi.player_open(player_recording['id'])

        else:
            kodi.player_open(player_recording['id'])
        return player_recording['title']
    return "nothing"
# play_something()
