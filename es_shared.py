import json
from urllib.request import urlopen, URLError
from collections import namedtuple
import sys, subprocess, getopt


def usage():
    print("Program Options:")
    print("-g\t Game(s) to query [REQUIRED]. Game list is comma separated")
    print("-n\t Max number of streams to display [OPTIONAL]")
    print("-q\t Quality of the stream [OPTIONAL]")
    #print("-p\t Video player to play the stream [OPTIONAL]")
    #print("-c\t Livestreamer binary (if it's not in your path) [OPTIONAL]")
    print()
    print("Examples:")
    print("program -g \"Dota 2\" -q source")
    print("program -g \"League of Legends, Dota 2\" -n 5 -q medium")

def parse_arguments(argv):
    # Program options
    games = []
    max_streams = 10
    quality = None
    livestreamer_cmd = "livestreamer"
    video_player = "vlc"

    if len(argv) == 0:
        usage()
        sys.exit()
    else:
        try:
            opts, args = getopt.getopt(argv, "g:n:q:c:p:")
        except getopt.GetoptError as err:
            print(str(err))
            usage()
            sys.exit()
        for opt, arg in opts:
            if opt == "-g":
                games = arg.split(",")
            elif opt == "-n":
                max_streams = int(arg)
            elif opt == "-q":
                quality = arg
            #elif opt == "-c":
                #livestreamer_cmd = arg
            #elif opt == "-p":
                #video_player = arg

        if len(games) < 1:
            print("At least 1 game must be specified")
            usage()
            sys.exit()
        else:
            for i in range(len(games)):
                games[i] = games[i].strip()

    return games, max_streams, quality, livestreamer_cmd, video_player


Stream = namedtuple("Stream", "id name display_name title viewers logo")
def get_twitch_streams(game_name):
    url = "https://api.twitch.tv/kraken/streams?game=" + game_name.strip().replace(" ", "+")
    try: response = urlopen(url)
    except URLError as e:
        print("Could not load Twitch streams")
        return []

    decoded = json.loads(response.readall().decode("utf-8"))

    stream_list = []

    for s in decoded["streams"]:
        stream = Stream(id = s["channel"]["_id"], name = s["channel"]["name"], display_name = s["channel"]["display_name"], 
            title = s["channel"]["status"], viewers =  s["viewers"], logo = s["channel"]["logo"])
        stream_list.append(stream)

    return stream_list

def parse_livestreamer_qualities(url):
    proc = subprocess.Popen(["livestreamer", url], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    out = out.decode("utf-8")
    pos = out.find("Available streams: ")
    out = out[pos:].strip().replace("Available streams: ", "").replace(" ", "").replace("(worst)", "").replace("(best)", "")

    return out.split(",")

def play_stream(livestreamer_cmd, url, quality, video_player):
    #print("Command:", livestreamer_cmd, url, quality, "--player", video_player, "--quiet")
    subprocess.Popen([livestreamer_cmd, url, quality, "--player", video_player, "--quiet"])