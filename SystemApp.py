from BaseGUIApp import BaseGUIApp
from shutil import copy2,move,rmtree,copytree
from os import scandir,remove
from time import ctime
from subprocess import PIPE,Popen
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SystemApp(BaseGUIApp):
	def __init__(self):
		BaseGUIApp.__init__(self)
		self.left_path_entry.connect("activate",self.__get_left_list)
		self.right_path_entry.connect("activate",self.__get_right_list)
		self.copy_button.connect("clicked",self.__copy)
		self.move_button.connect("clicked",self.__move)
		self.delete_button.connect("clicked",self.__delete)
		self.left_command_button.connect("clicked",self.__run_left_command)
		self.right_command_button.connect("clicked",self.__run_right_command)
	def __get_list(self,store,tree_view,entry):
		store=Gtk.ListStore(*self.store_type_def)
		tree_view.set_model(store)
		entries=scandir(entry.get_text())
		for i in entries:
			typ="directory" if i.is_dir() else ("file" if i.is_file() else "other")
			st=i.stat()
			store.append([typ,i.name,str(oct(st.st_mode))[-3:],ctime(st.st_mtime),st.st_nlink,st.st_uid,st.st_gid])
	def __get_left_list(self,entry):
		self.__get_list(self.left_store,self.left_tree_view,entry)
	def __get_right_list(self,entry):
		self.__get_list(self.right_store,self.right_tree_view,entry)
	def __copy(self,_):
		l=self.left_path_entry.get_text()
		r=self.right_path_entry.get_text()
		if l[-1]!='/': l+='/'
		if r[-1]!='/': r+='/'
		for file_name in self.__get_selection(self.left_tree_view):
			try:
				copy2(l+file_name,r)
			except IsADirectoryError:
				copytree(l+file_name,r+file_name)
		for file_name in self.__get_selection(self.right_tree_view):
			try:
				copy2(r+file_name,l)
			except IsADirectoryError:
				copytree(r+file_name,l+file_name)
				
		self.__get_list(self.left_store,self.left_tree_view,self.left_path_entry)
		self.__get_list(self.right_store,self.right_tree_view,self.right_path_entry)
	def __move(self,_):
		l=self.left_path_entry.get_text()
		r=self.right_path_entry.get_text()
		if l[-1]!='/': l+='/'
		if r[-1]!='/': r+='/'
		for file_name in self.__get_selection(self.left_tree_view):
			move(l+file_name,r)
		for file_name in self.__get_selection(self.right_tree_view):
			move(r+file_name,l)
		self.__get_list(self.left_store,self.left_tree_view,self.left_path_entry)
		self.__get_list(self.right_store,self.right_tree_view,self.right_path_entry)
	def __delete(self,_):
		l=self.left_path_entry.get_text()
		r=self.right_path_entry.get_text()
		if l[-1]!='/': l+='/'
		if r[-1]!='/': r+='/'
		for file_name in self.__get_selection(self.left_tree_view):
			try:
				remove(l+file_name)
			except OSError:
				rmtree(l+file_name)
		for file_name in self.__get_selection(self.right_tree_view):
			try:
				remove(r+file_name)
			except OSError:
				rmtree(r+file_name)
		self.__get_list(self.left_store,self.left_tree_view,self.left_path_entry)
		self.__get_list(self.right_store,self.right_tree_view,self.right_path_entry)
				
	def __get_selection(self,tree_view):
		model,selection=tree_view.get_selection().get_selected_rows()
		return (model[row][1] for row in selection)

	def __run_left_command(self,_):
		with Popen(['/bin/bash', "-c","(cd "+self.left_path_entry.get_text()+"; "+self.left_command_entry.get_text()+")"],stdout=PIPE) as p:
			self.left_command_view.get_buffer().insert(self.left_command_view.get_buffer().get_end_iter(),p.stdout.read().decode('utf-8'))
	def __run_right_command(self,_):
		with Popen(['/bin/bash', "-c","(cd "+self.right_path_entry.get_text()+"; "+self.right_command_entry.get_text()+")"],stdout=PIPE) as p:
			self.right_command_view.get_buffer().insert(self.right_command_view.get_buffer().get_end_iter(),p.stdout.read().decode('utf-8'))
	
