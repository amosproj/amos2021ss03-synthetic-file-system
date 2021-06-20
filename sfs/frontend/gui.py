# Python imports
import tkinter as tk


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

    def add_default_filter_entity_widgets(self, is_or=False):
        frm_filter_entity = tk.Frame(master=self)
        frm_filter_entity.pack()

        row, col = 1, 0
        if is_or:
            lbl_or = tk.Label(master=frm_filter_entity, text="or")
            lbl_or.grid(row=row, column=col)
            col = 1

        metadata_tag = tk.StringVar(value=self.metadata_tags[0])
        opt_metadata_tag = tk.OptionMenu(frm_filter_entity, metadata_tag, *self.metadata_tags)
        opt_metadata_tag.grid(row=row, column=col)

        conditional = tk.StringVar(value=self.conditionals[0])
        opt_conditional = tk.OptionMenu(frm_filter_entity, conditional, *self.conditionals)
        opt_conditional.grid(row=row, column=col + 1)

        ent_input = tk.Entry(master=frm_filter_entity)
        ent_input.grid(row=row, column=col + 2)
        ent_input.bind('<Control-a>', self._ctrl_a_callback)

        btn_and = tk.Button(master=frm_filter_entity, text="AND", command=self.add_default_filter_entity_widgets)
        btn_and.grid(row=row, column=col + 3)

        btn_or = tk.Button(
            master=frm_filter_entity, text="OR", command=lambda: self.add_default_filter_entity_widgets(True)
        )
        btn_or.grid(row=row, column=col + 4)

        btn_x = tk.Button(master=frm_filter_entity, text="X", command=frm_filter_entity.pack_forget)
        btn_x.grid(row=row, column=col + 5)


class GUI(tk.Frame):

    partners = ["mdh-core-1", "mdh-core-2", "passthrough"]  # TODO: Get names by backend manager

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.filter_frames = {}

        self._create_partner_widgets()
        self._create_default_filter_widgets()

    def _switch_filter_frame(self, *args):
        for filter_frame in self.filter_frames.values():
            filter_frame.grid_remove()
        filter_frame = self.filter_frames[self.partner.get()]
        filter_frame.grid()

    def _create_partner_widgets(self):
        frm_partner = tk.Frame(master=self)
        frm_partner.grid()

        self.partner = tk.StringVar(frm_partner, value=self.partners[0])
        self.partner.trace_add("write", self._switch_filter_frame)

        opt_partner = tk.OptionMenu(frm_partner, self.partner, *self.partners)
        opt_partner.pack()

    def _create_default_filter_widgets(self):
        for partner in self.partners:
            frm_filter = tk.Frame(master=self)

            self.filter_frames[partner] = frm_filter

            Filter(frm_filter).add_default_filter_entity_widgets()

        self.filter_frames[self.partners[0]].grid()


root = tk.Tk()
root.title("Synthetic File System")
app = GUI(master=root)
app.mainloop()
