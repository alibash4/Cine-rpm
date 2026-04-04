import os
import gi
from .utils import LAST_PLAYLIST_FILE

gi.require_version("GLib", "2.0")
from gi.repository import GLib


def save_last_playlist_file(win_mpv):
    """Saves the current playlist to a m3u8 file."""

    if win_mpv.playlist_count == 0 and os.path.exists(LAST_PLAYLIST_FILE):
        os.remove(LAST_PLAYLIST_FILE)
        return

    try:
        win_mpv["save-position-on-quit"] = True
        with open(LAST_PLAYLIST_FILE, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for item in win_mpv.playlist:
                filename = item.get("filename")
                f.write(f"{filename}\n")
    except Exception as e:
        print(f"Error saving last playlist file: {e}")


def restore_last_playlist(window, app, win_mpv):
    """Restore the last playlist if its the first window."""

    if len(app.get_windows()) > 1:
        return

    if os.path.exists(LAST_PLAYLIST_FILE):
        window.start_page.set_sensitive(False)
        GLib.idle_add(win_mpv.loadfile, LAST_PLAYLIST_FILE, "replace")
