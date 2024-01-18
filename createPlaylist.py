from spotifyBrain import SpotifyBrain
from inputValidator import InputValidator 

# The main file that...
# 1. Gets recently played tracks
# 2. Asks the user to choose x seed tracks
# 3. Get y recommended tracks
# 4. Ask the user to choose new or existing playlist
# 5a. Create the playlist and populate with recommended tracks
# 5b. Add tracks to an existing playlist

def main():
    print("Welcome to the Spotify Recents Recommender 3000!")
    spotify_brain = SpotifyBrain()
    validator = InputValidator()

    num_to_visualise = validator.get_valid_int(input("How many of your recently played tracks would you like to choose from? [1-50]: "), 50)

    print(f"Here are the last {num_to_visualise} tracks you listened to on Spotify:")
    last_played_tracks = spotify_brain.get_last_played_tracks(num_to_visualise)
    for index, track in enumerate(last_played_tracks, start=1):
        print(f"{index} -  {track}")
    
    # choosing tracks to use as a seed to generate a playlist
    indexes = validator.get_valid_seeds(input(f"Enter up to 5 indexes [1-{num_to_visualise}] of tracks to use as seeds, separated by a space: "), num_to_visualise)

    seed_tracks = [last_played_tracks[int(index)-1] for index in indexes]

    # choosing how many tracks they want recommended in the new playlist
    limit = validator.get_valid_int(input("How many tracks would you like recommended? [1-100]: "), 100)

    # get recommended based off seed tracks
    print("Here are the recommended tracks: ")
    recommended_tracks = spotify_brain.get_track_recommendations(seed_tracks, limit)
    for index, track in enumerate(recommended_tracks, start=1):
        print(f"{index} -  {track}")

    new_playlist = validator.get_playlist_preference(input("Would you like to add recommended tracks to a new or existing playlist? (new/existing): "))

    if new_playlist:
        playlist_name = input("Playlist name: ")
        playlist = spotify_brain.create_playlist(playlist_name)
        print(f"{playlist_name} was created successfully.")
    
    else:
        playlists = spotify_brain.get_existing_playlists()
        num_playlists = len(playlists)

        print(f"Here are {num_playlists} of your Playlists: ")
        for index, pl in enumerate(playlists, start=1):
            print(f"{index} -  {pl.name}")

        playlist_idx = validator.get_valid_int(
            input("Please enter the index of the playlist you wish to add the recommended tracks to: "), num_playlists)

        playlist = playlists[int(playlist_idx)-1]

    spotify_brain.populate_playlist(playlist, recommended_tracks)
    print(f"{limit} recommended tracks successfully uploaded to Playlist, '{playlist.name}'.")
    

main()
