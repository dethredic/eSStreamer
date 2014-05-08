#!/usr/bin/env python

import sys
import es_shared

def select_item_from_text_list(list):
    for i, list_item in enumerate(list):
        print("[" + str(i) + "]", list_item)

    selection = input("0-" + str(len(list) - 1) + ": ")
    try: selection = int(selection)
    except ValueError:
        print("Please enter a valid option")
        sys.exit()
    if selection < 0 or selection > len(list) - 1:
        print("Invalid selection")
        sys.exit()

    return list[selection]

def main(argv):
    # Apply program arguments
    games, max_streams, quality, livestreamer_cmd, video_player = es_shared.parse_arguments(argv)

    # Get the game
    game = None
    if len(games) > 1:
        print("Select a game:")
        game = select_item_from_text_list(games)
    else:
        game = games[0]

    # Load streams based on the selected game
    print("Loading streams...")
    streams = es_shared.get_twitch_streams(game)
    if len(streams) == 0:
        print("No streams available")  
        sys.exit()

    # Display streams to the user
    print("Select a stream:")
    for i, stream in enumerate(streams):
        print("[" + str(i) + "]", stream.display_name, "  -  Viewers:", stream.viewers)
        if i == max_streams - 1:
            break
    streams = streams[:i+1]

    # Let the user select a stream
    selection = input("0-" + str(len(streams) ) + ": ")
    try: selection = int(selection)
    except ValueError:
        print("Please enter a valid option")
        sys.exit()
    if selection < 0 or selection > len(streams):
        print("Invalid game")
        sys.exit()

    stream = streams[selection]

    url = "twitch.tv/" + stream.name

    # Get a stream quality
    if quality == None:
        print("Loading qualities...")
        qualities = es_shared.parse_livestreamer_qualities(url)

        print("Select a quality:")
        quality = select_item_from_text_list(qualities)

    # Play the stream
    es_shared.play_stream(livestreamer_cmd, url, quality, video_player)

if __name__ == "__main__":
    main(sys.argv[1:])
