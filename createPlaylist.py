from spotifyBrain import SpotifyBrain

# The main file that...
# 1. Gets recently played tracks
# 2. Asks the user to choose x seed tracks
# 3. Get y recommended tracks
# 4. Ask the user to choose new or existing playlist
# 5a. Create the playlist and populate with recommended tracks
# 5b. Add tracks to an existing playlist

def get_valid_int(to_check):
    invalid = True
    while invalid:
        try:
            int(to_check)
        except:
            to_check = input("Please enter numbers only!: ")
        else:
            return int(to_check)
        
def get_valid_int_list(to_check):
    invalid = True
    while invalid:
        try:
            [eval(i) for i in to_check.strip().split()]
        except:
            to_check = input("Please only enter numbers separated by a space: ")
        else:
            return [eval(i) for i in to_check.strip().split()]
        
# def get_valid_range(to_check, lowBound, upBound, type):
#     valid_range = to_check in range(lowBound, upBound+1)
#     while not valid_range:
#         to_check = get_valid_int(input(f"You have entered an invalid number of {type}! Please choose a number between {lowBound} and {upBound}: "))
#         valid_range = to_check in range(lowBound, upBound+1)
#     return to_check

def get_playlist_preference(to_check):
    invalid = True
    while invalid:
        if to_check.lower() == "new":
            return True
        elif to_check.lower() == "existing":
            return False
        else:
            to_check = input("Please enter either 'new' or 'existing': ")

def main():
    print("Welcome to the Spotify Recents Recommender 3000!")
    spotify_brain = SpotifyBrain()

    num_tracks_to_visualise = get_valid_int(input("How many of your recently played tracks would you like to choose from? (Between 1 and 50): "))

    # check the input is valid
    # get_valid_range(num_tracks_to_visualise, 1, 50, "tracks")

    invalid_limit = (num_tracks_to_visualise <= 0 or num_tracks_to_visualise > 50)
    while invalid_limit:
        num_tracks_to_visualise = get_valid_int(input("You have entered an invalid number of tracks! Please enter a number between 1 and 50: "))
        if (num_tracks_to_visualise > 0 and num_tracks_to_visualise <= 50):
            invalid_limit = False

    last_played_tracks = spotify_brain.get_last_played_tracks(num_tracks_to_visualise)

    print(f"Here are the last {num_tracks_to_visualise} tracks you listened to on Spotify:")
    for index, track in enumerate(last_played_tracks, start=1):
        print(f"{index} -  {track}")
    
    # choosing which tracks to use as a seed to generate a playlist
    indexes = input("Enter the tracks you want to use as seeds by track id separated by a space (Enter between 1 and 5 indexes): ")

    
    # check inputted seeds are valid
    # get_valid_range(num_seeds, 1, 5, "seeds")
    

    invalid_seeds = True
    while invalid_seeds:
        indexes_list = get_valid_int_list(indexes)

        num_seeds = len(indexes_list)
        print(num_seeds, f"[{indexes_list}]")

        invalid_num_seeds = (num_seeds <= 0 or num_seeds > 5)
        invalid_seed_value = not all((idx > 0 and idx <= len(last_played_tracks)) for idx in indexes_list) 

        if (invalid_num_seeds):
            indexes = input("You have entered an invalid number of indexes! Please enter between 1 and 5 indexes to be used as seeds: ")
            continue 

        elif (invalid_seed_value):
            indexes = input(f"You have entered an invalid index! Please enter indexes between 1 and {num_tracks_to_visualise} (inclusive) from the list above: ")
            continue
        
        elif (not invalid_num_seeds and not invalid_seed_value):
            invalid_seeds = False

    seed_tracks = [last_played_tracks[int(index)-1] for index in indexes_list]

    # choosing how many tracks they want recommended in the new playlist
    limit = get_valid_int(input("How many tracks would you like recommended? (Between 1 and 100): "))

    # check the input is valid
    invalid_limit = (limit < 1 or limit > 100)
    while invalid_limit:
        limit = get_valid_int(input("You have entered an invalid number of tracks! Please enter a number between 1 and 100: "))
        invalid_limit = not (limit in range(1, 101))

    # get recommended based off seed tracks
    recommended_tracks = spotify_brain.get_track_recommendations(seed_tracks, limit)

    print("Here are the recommended tracks: ")
    for index, track in enumerate(recommended_tracks, start=1):
        print(f"{index} -  {track}")

    new_playlist = get_playlist_preference(input("Would you like to add recommended tracks to a new or existing playlist? (new/existing): "))

    if new_playlist:
        playlist_name = input("Playlist name: ")
        playlist = spotify_brain.create_playlist(playlist_name)
        print(f"{playlist_name} was created successfully.")
    
    else:
        playlists = spotify_brain.get_existing_playlists()
        print(f"Here are up to 50 of your Playlists: ")
        for index, pl in enumerate(playlists, start=1):
            print(f"{index} -  {pl.name}")
        playlist_idx = get_valid_int(input("Please enter the index of the playlist you wish to add the recommended tracks to: "))
        invalid_idx = not (playlist_idx in range(1, len(playlists)+1))
        while invalid_idx:
            playlist_idx = get_valid_int(input("Please enter a valid index from the list above: " ))
            invalid_idx = not (playlist_idx in range(1, len(playlists)+1))

        playlist = playlists[int(playlist_idx)-1]

    spotify_brain.populate_playlist(playlist, recommended_tracks)
    print(f"{limit} recommended tracks successfully uploaded to Playlist, '{playlist.name}'.")
    

main()
