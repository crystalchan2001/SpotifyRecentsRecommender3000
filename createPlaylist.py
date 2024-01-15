from spotifyBrain import SpotifyBrain

# The main file that...
# 1. Gets recently played tracks
# 2. Asks the user to choose x seed tracks
# 3. Get y recommended tracks
# 4. Ask the user to choose a playlist name
# 5. Create the playlist and populate with the recommended tracks

def check_valid_int(to_check):
    invalid = True
    while invalid:
        try:
            int(to_check)
        except:
            to_check = input("Please enter numbers only!: ")
        else:
            return int(to_check)
        
def check_valid_int_list(to_check):
    invalid = True
    while invalid:
        try:
            [eval(i) for i in to_check.strip().split()]
        except:
            to_check = input("Please only enter numbers separated by a space: ")
        else:
            return [eval(i) for i in to_check.strip().split()]

def main():
    print("Welcome to the Spotify Recents Recommender 3000!")
    spotify_brain = SpotifyBrain()

    num_tracks_to_visualise = check_valid_int(input("How many of your recently played tracks would you like to choose from? (Between 1 and 50): "))

    # check the input is valid
    invalid_limit = (num_tracks_to_visualise <= 0 or num_tracks_to_visualise > 50)
    while invalid_limit:
        num_tracks_to_visualise = check_valid_int(input("You have entered an invalid number of tracks! Please enter a number between 1 and 50: "))
        if (num_tracks_to_visualise > 0 and num_tracks_to_visualise <= 50):
            invalid_limit = False

    last_played_tracks = spotify_brain.get_last_played_tracks(num_tracks_to_visualise)

    print(f"Here are the last {num_tracks_to_visualise} tracks you listened to on Spotify:")
    for index, track in enumerate(last_played_tracks, start=1):
        print(f"{index} -  {track}")
    
    # choosing which tracks to use as a seed to generate a playlist
    indexes = input("Enter the tracks you want to use as seeds by track id separated by a space (Enter between 1 and 5 indexes): ")

    # check inputted seeds are valid
    invalid_seeds = True
    while invalid_seeds:
        indexes_list = check_valid_int_list(indexes)

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
    limit = check_valid_int(input("How many tracks would you like recommended in your new playlist? (Between 1 and 100):"))

    # check the input is valid
    invalid_limit = (limit < 1 or limit > 100)
    while invalid_limit:
        limit = check_valid_int(input("You have entered an invalid number of tracks! Please enter a number between 1 and 100: "))
        if (limit >= 1 and limit <= 100):
            invalid_limit = False

    # get recommended based off seed tracks
    recommended_tracks = spotify_brain.get_track_recommendations(seed_tracks, limit)

    print("Here are the recommended tracks that will be included in your new playlist: ")
    for index, track in enumerate(recommended_tracks, start=1):
        print(f"{index} -  {track}")

    playlist_name = input("Playlist name: ")
    playlist = spotify_brain.create_playlist(playlist_name)
    print(f"{playlist_name} was created successfully.")

    spotify_brain.populate_playlist(playlist, recommended_tracks)
    print(f"{limit} recommended tracks successfully uploaded to {playlist_name}.")
    

main()
