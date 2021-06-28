# Python imports
import tkinter as tk
from threading import Thread
from tkinter import TclError, PhotoImage

# Local imports
from sfs.paths import ROOT_PATH
from sfs.backend import BackendManager

COLOR = "white"

# Naming conventions:
# Label lbl
# Button btn
# Entry ent
# Text txt
# Frame frm
# OptionMenu opt
class Filter(tk.Frame):

    metadata_tags = ["FileName", "FileType"]
    conditionals = ["Equals", "Contains"]
    algorithms = ["default", "flat"]

    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.configure(background=COLOR)
        self.filter_entity_num = 0
        self.filters_config = {}

        self._configure_filter()

    def _configure_filter(self):
        frm_config = tk.Frame(master=self)
        frm_config.pack()
        lbl_algorithm = tk.Label(master=frm_config, text="Algorithm:")
        lbl_algorithm.grid(row=0, column=0)
        algorithm = tk.StringVar(value=self.algorithms[0])
        opt_algorithm = tk.OptionMenu(frm_config, algorithm, *self.algorithms)
        opt_algorithm.grid(row=0, column=1)

    def _ctrl_a_callback(self, event):
        event.widget.select_range(0, 'end')
        event.widget.icursor('end')
        return 'break'

    def _remove_filter(self, frm_filter_entity):
        if self.filter_entity_num <= 1:
            self.add_default_filter_entity_widgets()
            self.filter_entity_num = 1
        else:
            self.filter_entity_num -= 1

        self.filters_config.pop(id(frm_filter_entity), None)
        frm_filter_entity.pack_forget()

    def get_filter_entity_list(self):
        filter_entities = []
        for filter_entity in self.filters_config.values():
            value = filter_entity[3].get()
            if not value:
                continue
            conditional = filter_entity[0]
            tag = filter_entity[1].get()
            operation = filter_entity[2].get()

            filter_entities.append([conditional, tag, operation, value])

        return filter_entities

    def get_filter_logic_individual(self) -> str:
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

    def add_default_filter_entity_widgets(self, is_or=False):
        frm_filter_entity = tk.Frame(master=self)
        frm_filter_entity_id = id(frm_filter_entity)
        frm_filter_entity.pack()

        filter_config = []

        row, col = 1, 0
        if is_or:
            lbl_or = tk.Label(master=frm_filter_entity, text="or")
            lbl_or.grid(row=row, column=col)
            col = 1
            filter_config.append("or")
        else:
            filter_config.append("and")

        metadata_tag = tk.StringVar(value=self.metadata_tags[0])
        filter_config.append(metadata_tag)
        opt_metadata_tag = tk.OptionMenu(frm_filter_entity, metadata_tag, *self.metadata_tags)
        opt_metadata_tag.grid(row=row, column=col)

        conditional = tk.StringVar(value=self.conditionals[0])
        filter_config.append(conditional)
        opt_conditional = tk.OptionMenu(frm_filter_entity, conditional, *self.conditionals)
        opt_conditional.grid(row=row, column=col + 1)

        value = tk.StringVar()
        filter_config.append(value)
        ent_input = tk.Entry(master=frm_filter_entity, textvariable=value)
        ent_input.grid(row=row, column=col + 2)
        ent_input.bind('<Control-a>', self._ctrl_a_callback)

        btn_and = tk.Button(master=frm_filter_entity, text="AND", command=self.add_default_filter_entity_widgets)
        btn_and.grid(row=row, column=col + 3)

        btn_or = tk.Button(
            master=frm_filter_entity, text="OR", command=lambda: self.add_default_filter_entity_widgets(True)
        )
        btn_or.grid(row=row, column=col + 4)

        btn_x = tk.Button(master=frm_filter_entity, text="X", command=lambda: self._remove_filter(frm_filter_entity))
        btn_x.grid(row=row, column=col + 5)

        self.filters_config[frm_filter_entity_id] = filter_config
        self.filter_entity_num += 1


class GUI(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.configure(background=COLOR)

        self.partners = BackendManager().get_backend_names()
        self.filter_frames = {}

        self._create_partner_widgets()
        self._create_default_filter_widgets()

    def _run(self):
        backend_name = self.partner.get()
        backend = BackendManager().get_backend_by_name(backend_name)

        try:
            update_state = getattr(backend, "_update_state")
            # TODO configure instance_config -> query
            query = backend.instance_config["query"]
            #print(self.filter_frames[backend_name].get_filter_entity_list())
            print(self.filter_frames[backend_name].get_filter_logic_individual())
            #query["filterLogicOption"] = "INDIVIDUAL"
            #query["filterFunctions"]
            #query["filterLogicIndividual"]
        except AttributeError:
            print("ERROR")
            pass  # Silent ignore

    def _switch_filter_frame(self, *args):
        # FIXME: Remove only the current grid
        for filter_frame in self.filter_frames.values():
            filter_frame.master.grid_remove()
        filter_frame = self.filter_frames[self.partner.get()]
        filter_frame.master.grid()

    def _create_partner_widgets(self):
        try:
            image = PhotoImage(file=ROOT_PATH / "Deliverables" / "final_logo.png")
            image = image.zoom(25)
            image = image.subsample(125)
            lbl_logo = tk.Label(master=self, image=image)
            lbl_logo.image = image
            lbl_logo.configure(background=COLOR)
            lbl_logo.grid(row=0, column=0)
        except TclError:
            pass  # Silent ignore

        frm_partner = tk.Frame(master=self)
        frm_partner.configure(background=COLOR)
        frm_partner.grid(row=1, column=0)

        self.partner = tk.StringVar(frm_partner, value=self.partners[0])
        self.partner.trace_add("write", self._switch_filter_frame)

        opt_partner = tk.OptionMenu(frm_partner, self.partner, *self.partners)
        opt_partner.grid(row=0, column=1)

        lbl_partner = tk.Label(master=frm_partner, text="Partner:")
        lbl_partner.grid(row=0, column=0)

        btn_run = tk.Button(master=frm_partner, text="RUN", command=self._run)
        btn_run.grid(row=0, column=2)

    def _create_default_filter_widgets(self):
        for partner in self.partners:

            fil = Filter(tk.Frame(master=self))
            fil.add_default_filter_entity_widgets()

            self.filter_frames[partner] = fil

        self.filter_frames[self.partners[0]].master.grid()


class GUIRunner(Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        root = tk.Tk()
        root.title("Synthetic File System")
        root.configure(background=COLOR)
        root.protocol("WM_DELETE_WINDOW", root.destroy)

        GUI(master=root).mainloop()


def run_gui():
    GUIRunner().start()



