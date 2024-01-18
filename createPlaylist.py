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

    num_to_visualise = validator.get_valid_int(input("How many of your recently played tracks would you like to choose from? (1 to 50): "), 50)

    print(f"Here are the last {num_to_visualise} tracks you listened to on Spotify:")
    last_played_tracks = spotify_brain.get_last_played_tracks(num_to_visualise)
    for index, track in enumerate(last_played_tracks, start=1):
        print(f"{index} -  {track}")
    
    # choosing tracks to use as a seed to generate a playlist
    indexes = validator.get_valid_seeds(input("Enter the tracks you want to use as seeds by track id separated by a space (Up to 5 indexes): "), num_to_visualise)

    # check inputted seeds are valid

    # invalid_seeds = True
    # while invalid_seeds:
    #     indexes_list = validator.get_int_list(indexes)

    #     num_seeds = len(indexes_list)
    #     # print(num_seeds, f"[{indexes_list}]")

    #     invalid_num_seeds = (num_seeds <= 0 or num_seeds > 5)
    #     invalid_seed_value = not all((idx > 0 and idx <= len(last_played_tracks)) for idx in indexes_list) 

    #     if (invalid_num_seeds):
    #         indexes = input("You have entered an invalid number of indexes! Please enter between 1 and 5 indexes to be used as seeds: ")
    #         continue 

    #     elif (invalid_seed_value):
    #         indexes = input(f"You have entered an invalid index! Please enter indexes between 1 and {num_to_visualise} (inclusive) from the list above: ")
    #         continue
        
    #     elif (not invalid_num_seeds and not invalid_seed_value):
    #         invalid_seeds = False

    seed_tracks = [last_played_tracks[int(index)-1] for index in indexes]

    # choosing how many tracks they want recommended in the new playlist
    limit = validator.get_valid_int(input("How many tracks would you like recommended? (Between 1 and 100): "), 100)

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
