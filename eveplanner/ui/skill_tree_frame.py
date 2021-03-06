from tkinter import *
from tkinter import ttk
from eveplanner.eveapi_wrapper.character_wrapper import CharacterWrapper
from eveplanner.ui.read_only_text import ReadOnlyText

__author__ = 'apodoprigora'


class SkillTreeFrame(ttk.Frame):
    def __init__(self, char_wrapper, master=None, cnf={}, **kw):
        super().__init__(master=master, **kw)
        if not isinstance(char_wrapper, CharacterWrapper):
            raise RuntimeError("There should be a character wrapper")
        self._char_wrapper = char_wrapper
        self._skill_name_list = StringVar()
        self._skill_description = StringVar(value="Please select a skill")
        self._skill_list = []
        self._refresh_data()
        self._initialize_widgets()
        self._initialize_self()

    def _initialize_skill_frame(self):
        skill_frame = ttk.Frame(master=self, padding=(3, 3, 3, 3))
        skill_frame.grid(row=0, column=0, sticky="nswe")
        skill_frame.rowconfigure(0, weight=1)
        skill_frame.columnconfigure(0, weight=1, minsize=150)
        skill_frame.columnconfigure(2, weight=1)
        return skill_frame

    def _init_skill_listbox(self, skill_frame):
        self.__list_box = Listbox(master=skill_frame, height=10, listvariable=self._skill_name_list)
        self.__list_box.grid(row=0, column=0, sticky="nswe")
        scrollbar = ttk.Scrollbar(master=skill_frame, orient=VERTICAL, command=self.__list_box.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.__list_box.configure(yscrollcommand=scrollbar.set)
        self.__list_box.bind('<<ListboxSelect>>', self._showPopulation)

    def _init_text_label(self, skill_frame):
        self.__text_label = ReadOnlyText(master=skill_frame)
        self.__text_label.grid(row=0, column=2, sticky="nswe")

    def _init_refresh_button(self):
        ttk.Button(master=self, text="Refresh", command=self._refresh_data).grid(row=1, column=0, columnspan=2, sticky=S)

    def _initialize_widgets(self):
        skill_frame = self._initialize_skill_frame()
        self._init_skill_listbox(skill_frame)
        self._init_text_label(skill_frame)
        self._init_refresh_button()
        self._showPopulation(None, selected_index=0)


    def _refresh_data(self):
        self._skill_list = self._char_wrapper.get_training_queue(update_cache=True)

        def get_skill_list_element(skill):
            return "%d. %s" % (skill.position, skill.tree_skill.name)

        self._skill_name_list.set(tuple([get_skill_list_element(skill) for skill in self._skill_list]))

    def _initialize_self(self):
        self.grid(row=0, column=0, sticky="nswe")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _set_text_element(self, selected_index):
        if not self._skill_list:
            return None
        self.__text_label.delete("1.0", END)
        self.__text_label.insert("0.0", self._skill_list[selected_index])

    def _showPopulation(self, event, selected_index=None):
        if selected_index is not None and 0 <= selected_index:
            self._set_text_element(selected_index)
        else:
            selection = self.__list_box.curselection()
            selected_pos = int(selection[0])
            if selected_pos >= 0:
                self._set_text_element(selected_pos)
