import customtkinter as ctk
import pyperclip

import constants as c
from generator import frame_generator

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{c.WIN_W}x{c.WIN_H}")
        self.title("DK Frame Generator")
        self.minsize(c.WIN_W, c.WIN_H)
        self.maxsize(c.WIN_W, c.WIN_H)
        self.iconbitmap("icons/dk.ico")
        self.font = ctk.CTkFont(c.FONT[0], c.FONT[1], c.FONT[2])

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.doc =  ''' The steps slider determines the number of "waves" of numbers to be returned. Each "wave" corresponds to a different interval of numbers in the original sequence.
        For example, if steps is 1, the function will return the first "wave" of numbers, which consists of every 60th number in the sequence.
        If steps is 2, the function will return the first "wave" of numbers (every 60th number), followed by the second "wave" of numbers (every 30th number). In each successive wave the interval will be roughly divided in half (60, 30, 15, 8, 4, 2, 1).
        If the infill frames checkbox is on, the last wave will be followed by all the remaining numbers in the sequence.'''

        self.top_frame = ctk.CTkFrame(master=self)
        self.top_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure((0, 1), weight=1)

        self.sframe_label = ctk.CTkLabel(master=self.top_frame, text="Start Frame", font=self.font)
        self.sframe_label.grid(row=0, column=0, padx=10, pady=5)

        self.sframe_entry = ctk.CTkEntry(master=self.top_frame, width = c.FRAME_ENTRY_W, font=self.font)
        self.sframe_entry.insert(0, "1")
        self.sframe_entry.grid(row=1, column=0, padx=10, pady=5)

        self.endframe_label = ctk.CTkLabel(master=self.top_frame, text="End Frame", font=self.font)
        self.endframe_label.grid(row=0, column=1, padx=10, pady=5)

        self.endframe_entry = ctk.CTkEntry(master=self.top_frame, width = c.FRAME_ENTRY_W, font=self.font)
        self.endframe_entry.insert(0, "100")
        self.endframe_entry.grid(row=1, column=1, padx=10, pady=5)

        self.mid_frame = ctk.CTkFrame(master=self)
        self.mid_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.mid_frame.grid_columnconfigure(0, weight=1)

        self.base_init = 4
        self.base_val = ctk.IntVar()
        self.base_label = ctk.CTkLabel(master=self.mid_frame, text=f"Base {str(c.BASE_VALUES[self.base_init])}", font=self.font)
        self.base_slider = ctk.CTkSlider(master=self.mid_frame, from_=0, to=len(c.BASE_VALUES)-1, number_of_steps=len(c.BASE_VALUES)-2, variable=self.base_val, command=self.base_slider_callback)
        self.base_slider.set(self.base_init)
        self.base_label.grid(row=0, column=0, padx=20, pady=5)
        self.base_slider.grid(row=1, column=0, padx=20, pady=10)
        
        self.step_init = 2
        self.step_val = ctk.IntVar()
        self.step_label = ctk.CTkLabel(master=self.mid_frame, text=str(self.step_init) + " Steps", font=self.font)
        self.step_slider = ctk.CTkSlider(master=self.mid_frame, from_=1, to=8, number_of_steps=7, variable=self.step_val, command=self.step_slider_callback)
        self.step_slider.set(self.step_init)
        self.step_label.grid(row=2, column=0, padx=20, pady=5)
        self.step_slider.grid(row=3, column=0, padx=20, pady=10)

        self.switch_frame = ctk.CTkFrame(master=self)
        self.switch_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.switch_frame.grid_columnconfigure(0, weight=1)

        self.reverse_val = ctk.BooleanVar()
        self.reverse_switch = ctk.CTkCheckBox(master=self.switch_frame, text='Reverse', variable=self.reverse_val, onvalue=True, offvalue=False, font=self.font)
        self.reverse_switch.grid(row=0, column=0, padx=10, pady=10)

        self.infill_val = ctk.BooleanVar()
        self.infill_val.set(True)
        self.infill_switch = ctk.CTkCheckBox(master=self.switch_frame, text='Infill Frames', variable=self.infill_val, onvalue=True, offvalue=False, font=self.font)
        self.infill_switch.grid(row=0, column=1, padx=10, pady=10)

        self.button_generate = ctk.CTkButton(master=self, text="Generate", command=self.button_callback, font=self.font)
        self.button_generate.grid(row=3, column=0, padx=10, pady=10)

        self.textbox = ctk.CTkTextbox(master=self, width=280, wrap='word', font=self.font)
        self.textbox.insert("0.0", self.doc)
        self.textbox.grid(row=4,column=0, padx=10, pady=10, sticky="nsew")

    def base_slider_callback(self, val):
        """Defines a base slider."""
        self.base_label.configure(text=f"Base {str(c.BASE_VALUES[int(val)])}")

    def step_slider_callback(self, val):
        """Defines a step slider."""     
        if val == 1:
            self.step_label.configure(text=str(int(val)) + " Step")
        else:
            self.step_label.configure(text=str(int(val)) + " Steps")

    def button_callback(self):
        """Defines generate button callback."""
        self.textbox.delete("0.0", "end")
        if self.sframe_entry.get() != "" and self.endframe_entry.get() != "":
            formatted_list = frame_generator(int(self.sframe_entry.get()),int(self.endframe_entry.get()),c.BASE_VALUES[int(self.base_val.get())],int(self.step_val.get()),self.infill_val.get(),self.reverse_val.get())
            pyperclip.copy(formatted_list)    
            self.textbox.insert("0.0", formatted_list)
        else:
            self.textbox.insert("0.0", "Please enter a value for both Start and End frame.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
