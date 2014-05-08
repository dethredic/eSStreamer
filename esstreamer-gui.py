#!/usr/bin/python

from gi.repository import Gtk
from threading import Thread
import sys
import es_shared


class QualitySelecter(Gtk.Window):

    def __init__(self, parent, livestreamer_cmd, url, video_player):
        Gtk.Window.__init__(self, title="Select a stream quality")
        self.set_border_width(5)
        #self.connect("delete-event", self.destroy())

        self.livestreamer_cmd = livestreamer_cmd
        self.url = url
        self.video_player = video_player

        self.main_box = Gtk.VBox()
        self.add(self.main_box)

        self.label = Gtk.Label("Loading qualities...")
        self.loading_spinner = Gtk.Spinner()
        self.loading_spinner.start()
        self.main_box.add(self.label)
        self.main_box.add(self.loading_spinner)

        self.max_qualities = 6
        self.button_list = []
        for i in range(self.max_qualities):
            self.button = Gtk.Button()
            self.button_list.append(self.button)
            self.main_box.add(self.button)

    def play_stream(self, widget, quality):
        es_shared.play_stream(self.livestreamer_cmd, self.url, quality, self.video_player)
        self.destroy()

    def hide_stream_buttoms(self):
        for i in range(self.max_qualities):
            self.button_list[i].hide()

    def load_qualities(self):
        self.hide_stream_buttoms()
        self.qualities = es_shared.parse_livestreamer_qualities(self.url)
        self.label.set_text("Select a quality")
        self.loading_spinner.hide()

        for i, quality in enumerate(self.qualities):
            self.button_list[i].show()
            self.button_list[i].set_label(quality)
            self.button_list[i].connect("clicked", self.play_stream, quality)
            if i > self.max_qualities - 1:
                break

    def get_qualities(self):
        thread = Thread(target = self.load_qualities, args = ())
        thread.start()

class MainWindow(Gtk.Window):

    def __init__(self, argv):
        # Apply program arguments
        self.games, self.max_streams, self.quality, self.livestreamer_cmd, self.video_player = es_shared.parse_arguments(argv)

        Gtk.Window.__init__(self, title="esStreamer")
        self.connect("delete-event", Gtk.main_quit)
        self.set_border_width(5)

        self.table = Gtk.Table(self.max_streams+1, 3, True)
        self.table.set_col_spacing(1, 5)
        self.table.set_row_spacing(0, 5)
        self.add(self.table)

        self.game_selector = Gtk.ComboBoxText()
        for game in self.games:
            self.game_selector.append_text(game)
        self.game_selector.set_active(0)
        self.game_selector.connect("changed", self.refresh_streams, self.max_streams)
        self.table.attach(self.game_selector, 0, 2, 0, 1)

        self.refresh = Gtk.Button(label="Refresh")
        self.refresh.connect("clicked", self.refresh_streams, self.max_streams)
        self.table.attach(self.refresh, 2, 3, 0, 1)

        self.loading_label = Gtk.Label("Loading Streams...")
        self.loading_spinner = Gtk.Spinner()
        self.table.attach(self.loading_label, 0, 3, 2, 3)
        self.table.attach(self.loading_spinner, 0, 3, 4, 5)

        self.button_list = []
        self.button_handle_list = []
        for i in range(self.max_streams):
            self.button = Gtk.Button()
            self.button_list.append(self.button)
            self.button_handle_list.append(1)
            self.table.attach(self.button, 0, 3, i+1, i+2)       

    def hide_stream_buttoms(self):
        for i in range(self.max_streams):
            self.button_list[i].hide()
            if self.button_list[i].handler_is_connected(self.button_handle_list[i]):
                self.button_list[i].disconnect(self.button_handle_list[i])

    def load_streams(self, game):
        self.hide_stream_buttoms()
        self.loading_label.show()
        self.loading_spinner.show()
        self.loading_spinner.start()
        streamList = es_shared.get_twitch_streams(game)
        self.loading_spinner.stop()
        self.loading_label.hide()
        self.loading_spinner.hide()

        for i, stream in enumerate(streamList[:self.max_streams]):
            self.button_list[i].show()
            self.button_list[i].set_label(stream.display_name)
            self.button_handle_list[i] = self.button_list[i].connect("clicked", self.play_stream, stream)

    def play_stream(self, widget, stream):
        url = "twitch.tv/" + stream.name

        if self.quality == None:
            qs = QualitySelecter(self, self.livestreamer_cmd, url, self.video_player)
            qs.show_all()
            qs.get_qualities()
        else:
            es_shared.play_stream(self.livestreamer_cmd, url, quality, self.video_player)

    def refresh_streams(self, widget, max_streams):
        thread = Thread(target = win.load_streams, args = (self.game_selector.get_active_text(), ))
        thread.start()

if __name__ == "__main__":
    win = MainWindow(sys.argv[1:])
    win.show_all()
    win.refresh_streams(win.refresh, win.max_streams)
    Gtk.main()
