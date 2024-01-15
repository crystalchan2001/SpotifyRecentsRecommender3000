from spotifyBrain import SpotifyBrain

# The main file that...
# 1. Gets recently played tracks
# 2. Asks the user to choose x seed tracks
# 3. Get y recommended tracks
# 4. Ask the user to choose a playlist name
# 5. Create the playlist and populate with the recommended tracks

def main():
    print("Welcome to the Spotify Recents Recommender 3000!")
    spotify_brain = SpotifyBrain()

    num_tracks_to_visualise = int(input("How many of your recently played tracks would you like to choose from? (Between 1 and 50): "))

    # check the input is valid
    invalid_limit = (num_tracks_to_visualise <= 0 or num_tracks_to_visualise > 50)
    while invalid_limit:
        num_tracks_to_visualise = int(input("You have entered an invalid number of tracks! Please enter a number between 1 and 50: "))
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
        try:
            indexes_list = [eval(i) for i in indexes.strip().split()]
        except:
            indexes = input("Please only enter indexes separated by a space: ")
            continue

        num_seeds = len(indexes_list)
        print(num_seeds, f"[{indexes_list}]")

        #* ERROR CHECK FOR invalid index value 
        invalid_num_seeds = (num_seeds <= 0 or num_seeds > 5)
        invalid_seed_value = not all((idx > 0 and idx <= len(last_played_tracks)) for idx in indexes_list) 
        print(f"invalid_num_seeds = {invalid_num_seeds}. invalid_seed_value = {invalid_seed_value}. len(last_played_tracks) = {len(last_played_tracks)}")

        if (invalid_num_seeds):
            indexes = input("You have entered an invalid number of indexes! Please enter between 1 and 5 indexes to be used as seeds: ")
            continue 

        elif (invalid_seed_value):
            indexes = input("You have entered an invalid track index! Please enter indexes from the list of tracks above: ")
            continue
        
        elif (not invalid_num_seeds and not invalid_seed_value):
            invalid_seeds = False

    seed_tracks = [last_played_tracks[int(index)-1] for index in indexes_list]

    # choosing how many tracks they want recommended in the new playlist
    limit = int(input("How many tracks would you like recommended in your new playlist? (Between 1 and 100):"))

    # check the input is valid
    invalid_limit = (limit < 1 or limit > 100)
    while invalid_limit:
        limit = int(input("You have entered an invalid number of tracks! Please enter a number between 1 and 100: "))
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
