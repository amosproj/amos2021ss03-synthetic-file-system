# Python imports
import tkinter as tk
from threading import Thread
from tkinter import TclError, PhotoImage
from typing import List

# Local imports
from sfs.backend import BackendManager
from sfs.paths import ROOT_PATH

WHITE = "white"
DARK_GREY = "#363636"
ORANGE = "#FE7A3A"


class Filter(tk.Frame):

    metadata_tags = ["FileName", "FileType"]
    operations_map = {"equals": "EQUAL",
                      "not equals": "NOT_EQUAL",
                      "contains": "CONTAINS",
                      "not contains": "NOT_CONTAINS"}
    algorithms = ["mirror", "flat"]

    opt_design = {"bg": WHITE, "highlightbackground": WHITE, "activebackground": DARK_GREY, "activeforeground": ORANGE}
    opt_menu_design = {"bg": WHITE, "activebackground": DARK_GREY, "activeforeground": ORANGE}
    btn_design = {"bg": WHITE, "activebackground": DARK_GREY, "activeforeground": ORANGE}

    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.configure(bg=WHITE)
        self.filter_entity_count = 0
        self.filters_config = {}

        self._configure_filter()

    def _configure_filter(self) -> None:
        """
        Add general configurations for a filter (here: algorithm)
        :return: None
        """
        frm_config = tk.Frame(master=self, bg=WHITE)
        frm_config.pack()

        tk.Label(
            master=frm_config,
            text="Algorithm:",
            bg=WHITE
        ).grid(row=0, column=0)

        self.algorithm = tk.StringVar(value=self.algorithms[0])
        opt_algorithm = tk.OptionMenu(frm_config, self.algorithm, *self.algorithms)
        opt_algorithm.configure(self.opt_design)
        opt_algorithm["menu"].configure(self.opt_menu_design)
        opt_algorithm.grid(row=0, column=1)

    def _ctrl_a_callback(self, event) -> str:
        """
        Callback to use ctrl+a for a specific widget
        :param event:
        :return: 'break' to stop whatever following event is breaking the ctrl+a behavior
        """
        event.widget.select_range(0, "end")
        event.widget.icursor("end")
        return "break"

    def _remove_filter(self, frm_filter_entity) -> None:
        """
        Remove a filter entity when button X was clicked
        :param frm_filter_entity:
        :return: None
        """
        if self.filter_entity_count <= 1:
            self.filter_entity_count = 0
            self.add_default_filter_entity_widgets()
        else:
            self.filter_entity_count -= 1

        self.filters_config.pop(id(frm_filter_entity), None)
        frm_filter_entity.pack_forget()

    def add_default_filter_entity_widgets(self, is_or=False) -> None:
        """
        Create a filter entity: [(Conditional) | Tag | Operation | Value | AND | OR | X]
        :param is_or: if true, or following filter entities
        :return: None
        """
        frm_filter_entity = tk.Frame(master=self, bg=WHITE)
        frm_filter_entity_id = id(frm_filter_entity)
        frm_filter_entity.pack()

        filter_config = []

        row, col = 1, 0
        # Label to indicate an "or" or "and" conditional
        if is_or:
            tk.Label(
                master=frm_filter_entity,
                text="or",
                bg=WHITE
            ).grid(row=row, column=col)
            col = 1
            filter_config.append("or")
        else:
            filter_config.append("and")

        # OptionMenu with metadata tags, e.g. FileName, FileType etc.
        metadata_tag = tk.StringVar(value=self.metadata_tags[0])
        filter_config.append(metadata_tag)
        opt_metadata_tag = tk.OptionMenu(frm_filter_entity, metadata_tag, *self.metadata_tags)
        opt_metadata_tag.configure(self.opt_design)
        opt_metadata_tag["menu"].configure(self.opt_menu_design)
        opt_metadata_tag.grid(row=row, column=col)

        # OptionMenu with operations, e.g. equals, not equals etc.
        operations = list(self.operations_map.keys())
        operation = tk.StringVar(value=operations[0])
        filter_config.append(operation)
        opt_conditional = tk.OptionMenu(frm_filter_entity, operation, *operations)
        opt_conditional.configure(self.opt_design)
        opt_conditional["menu"].configure(self.opt_menu_design)
        opt_conditional.grid(row=row, column=col + 1)

        # Textfield for values
        value = tk.StringVar()
        filter_config.append(value)
        ent_input = tk.Entry(master=frm_filter_entity, textvariable=value)
        ent_input.grid(row=row, column=col + 2)
        ent_input.bind('<Control-a>', self._ctrl_a_callback)

        # Button: AND
        tk.Button(
            master=frm_filter_entity,
            text="AND",
            **self.btn_design,
            command=self.add_default_filter_entity_widgets
        ).grid(row=row, column=col + 3)

        # Button: OR
        tk.Button(
            master=frm_filter_entity,
            text="OR",
            **self.btn_design,
            command=lambda: self.add_default_filter_entity_widgets(True)
        ).grid(row=row, column=col + 4)

        # Button: X
        tk.Button(
            master=frm_filter_entity,
            text="X",
            **self.btn_design,
            command=lambda: self._remove_filter(frm_filter_entity)
        ).grid(row=row, column=col + 5)

        self.filters_config[frm_filter_entity_id] = filter_config
        self.filter_entity_count += 1

    def get_filter_entity_list(self) -> List[List[str]]:
        """
        Returns all the filter entities
        :return: List[List[str]]
        """
        filter_entities = []
        for filter_entity in self.filters_config.values():
            value = filter_entity[3].get()
            if not value:
                continue
            conditional = filter_entity[0]
            tag = filter_entity[1].get()
            operation = self.operations_map[filter_entity[2].get()]

            filter_entities.append([conditional, tag, operation, value])

        return filter_entities

    def get_filter_logic_individual(self) -> str:
        """
        Returns the individual filter logic (mdh specific)
        :return: str e.g. "(f0 and f1) or (f2)"
        """

        filter_entities = self.get_filter_entity_list()
        if not filter_entities:
            return ""

        filter_logic = "(f0"
        for i, filter_entity in enumerate(filter_entities[1:], start=1):
            if filter_entity[0] == "or":
                filter_logic += f") or (f{i}"
            else:
                filter_logic += f" and f{i}"
        filter_logic += ")"

        return filter_logic


class GUI(tk.Frame):

    btn_run_design = {"bg": DARK_GREY, "fg": ORANGE, "activebackground": WHITE}

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.configure(bg=WHITE)

        self.partners = BackendManager().get_backend_names()
        self.filter_frames = {}

        self._create_partner_widgets()
        self._create_default_filter_widgets()

    def _run(self) -> None:
        """
        Run a filter configuration for a specific partner
        :return: None
        """
        backend_name = self.partner.get()
        backend = BackendManager().get_backend_by_name(backend_name)

        try:
            update_state = getattr(backend, "_update_state")
            query = backend.instance_config["query"]
            query["filterFunctions"] = \
                [filter_entity[1:] for filter_entity in self.filter_frames[backend_name].get_filter_entity_list()]
            query["filterLogicOption"] = "INDIVIDUAL"
            query["filterLogicIndividual"] = self.filter_frames[backend_name].get_filter_logic_individual()

            result_structure = self.filter_frames[backend_name].algorithm.get()
            backend.result_structure = result_structure
            backend.instance_config["resultStructure"] = result_structure

            backend.instance_config["querySource"] = "inline"

            update_state()
        except AttributeError:
            pass  # Silent ignore

    def _switch_filter_frame(self, *args) -> None:
        """
        Switch the filter frame to a different partner
        :param args: ignored
        :return: None
        """
        # FIXME: Remove only the current grid
        for filter_frame in self.filter_frames.values():
            filter_frame.master.pack_forget()
        filter_frame = self.filter_frames[self.partner.get()]
        filter_frame.master.pack()

    def _create_partner_widgets(self) -> None:
        """
        Add an image, partner OptionMenu and run button
        :return: None
        """
        try:
            image = PhotoImage(file=ROOT_PATH / "Deliverables" / "final_logo.png")
            image = image.zoom(25)
            image = image.subsample(125)
            lbl_logo = tk.Label(image=image)
            lbl_logo.image = image
            lbl_logo.configure(bg=WHITE)
            lbl_logo.pack()
        except TclError:
            pass  # Silent ignore

        frm_partner = tk.Frame()
        frm_partner.configure(bg=WHITE)
        frm_partner.pack()

        self.partner = tk.StringVar(frm_partner, value=self.partners[0])
        self.partner.trace_add("write", self._switch_filter_frame)

        opt_partner = tk.OptionMenu(frm_partner, self.partner, *self.partners)
        opt_partner.configure(Filter.opt_design)
        opt_partner["menu"].configure(Filter.opt_menu_design)
        opt_partner.grid(row=0, column=1)

        tk.Label(
            master=frm_partner,
            text="Partner:",
            bg=WHITE
        ).grid(row=0, column=0)

        tk.Button(
            master=frm_partner,
            text="RUN",
            **self.btn_run_design,
            command=self._run
        ).grid(row=0, column=2)

    def _create_default_filter_widgets(self) -> None:
        """
        Create and save all filters and make first partner current
        :return: None
        """
        for partner in self.partners:

            fil = Filter(tk.Frame())
            fil.add_default_filter_entity_widgets()
            self.filter_frames[partner] = fil

        self.filter_frames[self.partners[0]].master.pack()


class GUIRunner(Thread):

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        root = tk.Tk()
        root.title("Synthetic File System")
        root.configure(bg=WHITE)
        root.protocol("WM_DELETE_WINDOW", root.destroy)

        GUI(master=root).mainloop()


def run_gui():
    GUIRunner().start()
