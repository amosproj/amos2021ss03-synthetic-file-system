# Python imports
import tkinter as tk
from copy import deepcopy
from threading import Thread
from tkinter import TclError, PhotoImage
from typing import List

# 3rd party imports
import mdh

# Local imports
from sfs.backend import BackendManager
from sfs.paths import ROOT_PATH

_WHITE = "#FFFFFF"
_DARK_GREY = "#363636"
_ORANGE = "#FE7A3A"


class Filter(tk.Frame):

    supported_metadata_tags = ["FileName", "FileSize", "FileType", "MIMEType", "SourceFile"]
    supported_algorithms = ["mirror", "flat"]
    operations_string_map = {"contains": "CONTAINS",
                             "not contains": "NOT_CONTAINS"}
    operations_relations_map = {"equals": "EQUAL",
                                "not equals": "NOT_EQUAL",
                                "is greater": "GREATER",
                                "is smaller": "SMALLER"}

    opt_design = {"bg": _WHITE, "highlightbackground": _WHITE, "activebackground": _DARK_GREY, "activeforeground": _ORANGE}
    opt_menu_design = {"bg": _WHITE, "activebackground": _DARK_GREY, "activeforeground": _ORANGE}
    btn_design = {"bg": _WHITE, "activebackground": _DARK_GREY, "activeforeground": _ORANGE}

    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.configure(bg=_WHITE)
        self.filter_entity_count = 0
        self.filters_config = {}
        self._metadata_tags = deepcopy(self.supported_metadata_tags)

        self._configure_filter()

    @property
    def metadata_tags(self) -> List[str]:
        return self._metadata_tags

    @metadata_tags.setter
    def metadata_tags(self, metadata_tags) -> None:
        """
        Intersect supported metadata tags with mdh core metadata tags
        :return: None
        """
        self._metadata_tags = sorted(list(set(self.supported_metadata_tags) & set(metadata_tags)))

    def _configure_filter(self) -> None:
        """
        Add general configurations for a filter (here: algorithm)
        :return: None
        """
        frm_config = tk.Frame(master=self, bg=_WHITE)
        frm_config.pack()

        tk.Label(
            master=frm_config,
            text="Algorithm:",
            bg=_WHITE
        ).grid(row=0, column=0)

        self.algorithm = tk.StringVar(value=self.supported_algorithms[0])
        opt_algorithm = tk.OptionMenu(frm_config, self.algorithm, *self.supported_algorithms)
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

    def _create_operation(self, metadata_tag, filter_config, frm_filter_entity, row, col) -> None:
        """
        Callback function to adapt the operation choice list in regard to the metadata tag
        :param metadata_tag: to distinguish what tag gets which operation
        :param filter_config: replace the old variable
        :param frm_filter_entity: for accessing the operation slave
        :param row: grid row
        :param col: grid column
        :return: None
        """
        metadata_tag = metadata_tag.get()

        if metadata_tag == "FileSize":
            operations = list(self.operations_relations_map.keys())
        else:
            operations = list(self.operations_string_map.keys()) + list(self.operations_relations_map.keys())[:2]

        frm_filter_entity.grid_slaves(column=col + 1)[0].destroy()

        operation = tk.StringVar(value=operations[0])

        filter_config.pop(2)
        filter_config.insert(2, operation)

        opt_operation = tk.OptionMenu(frm_filter_entity, operation, *operations)
        opt_operation.configure(self.opt_design)
        opt_operation["menu"].configure(self.opt_menu_design)
        opt_operation.grid(row=row, column=col + 1)

    def add_default_filter_entity_widgets(self, is_or=False) -> None:
        """
        Create a filter entity: [(Conditional) | Tag | Operation | Value | AND | OR | X]
        :param is_or: if true, or following filter entities
        :return: None
        """
        frm_filter_entity = tk.Frame(master=self, bg=_WHITE)
        frm_filter_entity_id = id(frm_filter_entity)
        frm_filter_entity.pack()

        filter_config = []

        row, col = 1, 0
        # Label to indicate an "or" or "and" conditional
        if is_or:
            tk.Label(
                master=frm_filter_entity,
                text="or",
                bg=_WHITE
            ).grid(row=row, column=col)
            col = 1
            filter_config.append("or")
        else:
            filter_config.append("and")

        # OptionMenu with operations, e.g. equals, not equals etc.
        operations = list(self.operations_string_map.keys()) + list(self.operations_relations_map.keys())[:2]
        operation = tk.StringVar(value=operations[0])
        opt_conditional = tk.OptionMenu(frm_filter_entity, operation, *operations)
        opt_conditional.configure(self.opt_design)
        opt_conditional["menu"].configure(self.opt_menu_design)
        opt_conditional.grid(row=row, column=col + 1)

        # OptionMenu with metadata tags, e.g. FileName, FileType etc.
        metadata_tag = tk.StringVar(value=self.metadata_tags[0])
        metadata_tag.trace_add(
            "write",
            lambda *args: self._create_operation(metadata_tag, filter_config, frm_filter_entity, row, col))
        opt_metadata_tag = tk.OptionMenu(frm_filter_entity, metadata_tag, *self.metadata_tags)
        opt_metadata_tag.configure(self.opt_design)
        opt_metadata_tag["menu"].configure(self.opt_menu_design)
        opt_metadata_tag.grid(row=row, column=col)

        # Textfield for values
        value = tk.StringVar()
        ent_input = tk.Entry(master=frm_filter_entity, textvariable=value)
        ent_input.grid(row=row, column=col + 2)
        ent_input.bind('<Control-a>', self._ctrl_a_callback)

        filter_config.append(metadata_tag)
        filter_config.append(operation)
        filter_config.append(value)

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
            # Union dictionaries and get mapped operation
            operation = {**self.operations_string_map, **self.operations_relations_map}[filter_entity[2].get()]

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

    btn_run_design = {"bg": _DARK_GREY, "fg": _ORANGE, "activebackground": _WHITE}

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.configure(bg=_WHITE)

        self.partners: List[str] = BackendManager().get_backend_names()
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

    def _switch_filter_frame(self) -> None:
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
            lbl_logo.configure(bg=_WHITE)
            lbl_logo.pack()
        except TclError:
            pass  # Silent ignore

        frm_partner = tk.Frame()
        frm_partner.configure(bg=_WHITE)
        frm_partner.pack()

        self.partner = tk.StringVar(frm_partner, value=self.partners[0])
        self.partner.trace_add("write", lambda *args: self._switch_filter_frame())

        opt_partner = tk.OptionMenu(frm_partner, self.partner, *self.partners)
        opt_partner.configure(Filter.opt_design)
        opt_partner["menu"].configure(Filter.opt_menu_design)
        opt_partner.grid(row=0, column=1)

        tk.Label(
            master=frm_partner,
            text="Partner:",
            bg=_WHITE
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

            # Only get supported metadata tags from core
            backend = BackendManager().get_backend_by_name(partner)
            try:
                metadata_tags_raw = mdh.statistics.get_metadata_tags(backend.core)
                fil.metadata_tags = [metadata_tag['name'] for metadata_tag in metadata_tags_raw]
            except AttributeError:
                pass  # Silent ignore

            fil.add_default_filter_entity_widgets()
            self.filter_frames[partner] = fil

        self.filter_frames[self.partners[0]].master.pack()


class GUIRunner(Thread):

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        root = tk.Tk()
        root.title("Synthetic File System")
        root.configure(bg=_WHITE)
        root.protocol("WM_DELETE_WINDOW", root.destroy)

        GUI(master=root).mainloop()


def run_gui():
    GUIRunner().start()
