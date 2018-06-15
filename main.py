import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from SystemApp import SystemApp

def main():
	main_app=SystemApp()
	main_app.main_window.show_all()
	Gtk.main()
main()
