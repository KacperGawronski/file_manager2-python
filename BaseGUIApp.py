import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class BaseGUIApp:
	def __init__(self):
		self.__builder = Gtk.Builder()
		self.__builder.add_from_file("GUI/main.glade")
		self.store_type_def=(str,str,str,str,int,int,int)
		self.column_names=["Type","Name","Permissions","Modification","nlink","uid","gid"]
		
		self.main_window=self.__builder.get_object("main_window")
		self.left_path_entry=self.__builder.get_object("left_path_entry")
		self.right_path_entry=self.__builder.get_object("right_path_entry")
		
		self.left_store = Gtk.ListStore(*self.store_type_def)
		self.left_tree_view=self.__builder.get_object("left_tree_view")
		self.left_tree_view.set_model(self.left_store)
		self.left_tree_view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		for i in range(len(self.store_type_def)):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(self.column_names[i], renderer, text=i)
			self.left_tree_view.append_column(column)
		
		self.right_store = Gtk.ListStore(str,str,str,str,int,int,int)
		self.right_tree_view=self.__builder.get_object("right_tree_view")
		self.right_tree_view.set_model(self.right_store)
		self.right_tree_view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		for i in range(len(self.store_type_def)):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(self.column_names[i], renderer, text=i)
			self.right_tree_view.append_column(column)
		
		self.copy_button=self.__builder.get_object("copy_button")
		self.move_button=self.__builder.get_object("move_button")
		self.delete_button=self.__builder.get_object("delete_button")
		self.left_command_button=self.__builder.get_object("left_command_button")
		self.right_command_button=self.__builder.get_object("right_command_button")
		self.left_command_view=self.__builder.get_object("left_command_view")
		self.right_command_view=self.__builder.get_object("right_command_view")
		self.left_command_entry=self.__builder.get_object("left_command_entry")
		self.right_command_entry=self.__builder.get_object("right_command_entry")
