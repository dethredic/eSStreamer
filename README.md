eSports Streamer

eSStreamer is a Livestreamer frontend that automatically finds live twitch.tv streams by game. The streams are played with Livestreamer and will appear in your desktop video player like VLC so Flash is avoided.


Required
1) Livestreamer
2) VLC (not really but I have only tested with this)
3) Python 3 with python3-gi

Howto Use
1) Install the above
2) Run either the gui or cli version. Some examples can be seen below:

Shows only Dota 2 streams and prompts for quality
./esstreamer-gui.py -g "Dota 2"

Allows the user to switch between Dota 2 and League of Legends streams. Automatically plays in source quality:
./esstreamer-gui.py -g "Dota 2, League of Legends" -q source

3) Once you have a configuration that works for you save it to a bash script / batch file etc.
