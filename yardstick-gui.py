import tkinter as tk
from tkinter import filedialog
import customtkinter, threading
from utility.subghz import yardstick_rx, transmit_signals, transmit_tesla, jammer, parse_import_file
from utility.yardstick import configure_yardstick
from rflib import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.d = RfCat()
        self.d.lowball()

        self.title('Yardstick One Playground')
        self.geometry('1080x460')

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_columnconfigure((0, 2, 3), weight=1)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Options")
        self.scrollable_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # receive switch
        self.switch_receive = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Receive", command=self.toggle_receive)
        self.switch_receive.grid(row=1, column=0, padx=10, pady=(0, 20))
        # transmit switch 
        self.switch_transmit = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Transmit", command=self.toggle_transmit)
        self.switch_transmit.grid(row=2, column=0, padx=10, pady=(0, 20))
    
        # tesla charging port switch
        self.tesla_transmit = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Tesla Port", command=self.toggle_tesla)
        self.tesla_transmit.grid(row=3, column=0, padx=10, pady=(0, 20))
        self.switch_jammer = customtkinter.CTkSwitch(master=self.scrollable_frame, text="Jam", command=self.toggle_jammer)
        self.switch_jammer.grid(row=4, column=0, padx=10, pady=(0, 20))
        # spectrum analyzer
        self.button_spectrum_analyzer = customtkinter.CTkButton(master=self.scrollable_frame, text="Spectrum Analyzer [buggy]", command=self.spectrum_analyzer)
        self.button_spectrum_analyzer.grid(row=5, column=0, padx=20, pady=10)
        # reset button
        # self.button_reset = customtkinter.CTkButton(master=self.scrollable_frame, text="Spectrum Analyzer", command=self.reset_yardstick(d))
        # self.button_reset.grid(row=6, column=0, padx=20, pady=10)
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Configure")
        self.tabview.tab("Configure").grid_columnconfigure(0, weight=1)
        
        # Add the "Advanced" tab
        self.tabview.add("Advanced")
        self.tabview.tab("Advanced").grid_columnconfigure(0, weight=1)

        self.frequencies = ["300Mhz", "315Mhz", "390Mhz", "433.92Mhz", "Custom"]
        self.selected_frequency = tk.StringVar()
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Configure"), values=self.frequencies, command=self.frequency_option_selected)
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        # create textbox for custom frequency
        self.custom_frequency_entry = customtkinter.CTkEntry(self.tabview.tab("Configure"), placeholder_text="Custom Frequency")
        self.custom_frequency_entry.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.custom_frequency_entry.configure(state="disabled")  # Initially disable the textbox
        # dropdown box for modulation selection
        self.selected_modulation = tk.StringVar()
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Configure"), values=['AM270', 'AM650', 'FM238', 'FM476'], command=self.modulation_option_selection)
        self.optionmenu_2.grid(row=2, column=0, padx=20, pady=(20, 10))
        # Configure button
        self.button_configure = customtkinter.CTkButton(self.tabview.tab("Configure"), text="configure", command=self.configure_stick)
        self.button_configure.grid(row=3, column=0, padx=20, pady=10)

        # signals text box
        self.textbox = customtkinter.CTkTextbox(self, width=512)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Scrollable frame for the "Advanced" tab
        self.advanced_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Advanced"))
        self.advanced_scrollable_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")
        self.advanced_scrollable_frame.grid_columnconfigure(0, weight=1)

        # Labels and textboxes for user input in the "Advanced" tab
        self.entry_baudrate = customtkinter.CTkEntry(self.advanced_scrollable_frame, placeholder_text="Custom Baudrate")
        self.entry_baudrate.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.entry_deviation = customtkinter.CTkEntry(self.advanced_scrollable_frame, placeholder_text="Custom Deviation")
        self.entry_deviation.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.label_amp = customtkinter.CTkLabel(self.advanced_scrollable_frame, text="Enable amp")
        self.label_amp.grid(row=2, column=0, padx=20, pady=(20, 0), sticky='w')
 
        self.entry_amp = customtkinter.CTkOptionMenu(self.advanced_scrollable_frame, values=['True', 'False'])
        self.entry_amp.grid(row=3, column=0, padx=20, pady=(0, 10))

        # terminal entry box
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Manually Configure/Utilize Yardstick One")
        self.entry.grid(row=2, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.button_save_file = customtkinter.CTkButton(master=self, text='Save Capture', border_width=2, command=self.save_capture_to_file)
        self.button_save_file.grid(row=2, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # import file
        self.button_import_file = customtkinter.CTkButton(master=self, text='Import Cap File', fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.import_file)
        self.button_import_file.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # progress bar
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.yardstick_receiver = yardstick_rx(self.textbox.insert)

    def configure_stick(self):
        amp = self.entry_amp.get()
        baudrate = int(self.entry_baudrate.get()) if self.entry_baudrate.get() else 0
        deviation = int(self.entry_deviation.get()) if self.entry_deviation.get() else 0


        print(f'Freq: {self.frequency}, Mod: {self.modulation}, Baud: {baudrate}, Dev: {deviation}, Amp: {amp}')
        configure_yardstick(self.d, int(self.frequency), self.modulation, int(baudrate), int(deviation), amp)

    def toggle_receive(self):
        switch = self.switch_receive.get()
        if switch == 1:
            self.start_progress_bar()
            self.start_signal_capture()
        else:
            self.stop_signal_capture()
            self.stop_progress_bar()
            self.d.setModeIDLE()

    def start_signal_capture(self):
        self.d.setModeRX()
        self.yardstick_receiver.reset_capture()
        capture_thread = threading.Thread(target=self.yardstick_receiver.capture_signals, args=(self.d,))
        capture_thread.start()

    def stop_signal_capture(self):
        self.yardstick_receiver.stop_capture()

    def toggle_transmit(self):
        switch = self.switch_transmit.get()
        if switch == 1:
            self.start_progress_bar()
            self.transmit_thread = threading.Thread(target=transmit_signals, args=(self.d, self.yardstick_receiver.signals))
            self.transmit_thread.start()
        elif switch == 0 and hasattr(self, 'transmit_thread') and self.transmit_thread.is_alive():
            self.transmit_thread.join()
        else:
            self.stop_progress_bar()

    def toggle_tesla(self):
        switch = self.tesla_transmit.get()
        if switch == 1:
            self.start_progress_bar()
            telsa_thread = threading.Thread(target=transmit_tesla, args=(self.d,))
            telsa_thread.start()
        else:
            self.stop_progress_bar()
    
    def toggle_jammer(self):
        switch = self.switch_jammer.get()
        if switch == 1:
            self.start_progress_bar()
            jammer_thread = threading.Thread(target=jammer, args=(self.d,))
            jammer_thread.start()
        else:
            self.stop_progress_bar()
            self.d.setModeIDLE()

    def start_progress_bar(self):
        self.progressbar_1.configure(mode="indeterminate")
        self.progressbar_1.start()
    
    def stop_progress_bar(self):
        self.progressbar_1.stop()

    def frequency_option_selected(self, selected_option):
        if selected_option == "Custom":
            self.custom_frequency_entry.configure(state="normal")  # Enable the textbox for custom frequency
        else:
            self.custom_frequency_entry.configure(state="disabled")  # Disable the textbox for preset frequencies
        if selected_option != 'Custom':
            freq = float(selected_option[:-3])
            frequency = int(freq * 1e6)
        else:
            custom_freq_entry = self.custom_frequency_entry.get()
            if len(custom_freq_entry) != 9:
                print(f'[-] Value error for setting frequency at {custom_freq_entry}..\n[*] Configuring to {str(custom_freq_entry)[:3]}Mhz')
                frequency = int(str(custom_freq_entry)[:3] + '000000')
            else:
                frequency = int(custom_freq_entry)
        self.frequency = frequency
        return frequency
        

    def modulation_option_selection(self, selected_option):
        self.modulation = selected_option
    
    def spectrum_analyzer(self):
        try:
            self.d.specan(self.frequency)
        except Exception as e:
            print('error closing specan')
            print(e)
    
    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select a Capture File", filetypes=[("Capture Files", "*.cap"), ("All Files", "*.*"), ("Sub Files", '*.sub')])
        if '.cap' in file_path:
            self.frequency, self.modulation, self.yardstick_receiver.signals = parse_import_file(file_path)
            if str(self.frequency)[:5] == '43392':
                frequency_mhz = '433.92Mhz'
            else:
                frequency_mhz = str(self.frequency[:3]) + 'Mhz'
            self.update_frequency_and_modulation(frequency_mhz, self.modulation)
            self.configure_stick()
            for payload in self.yardstick_receiver.signals:
                formatted_signal = f"Signal: {payload}\nSignal Length: {len(payload)}\n"
                self.textbox.insert(tk.END, formatted_signal)

    def update_frequency_and_modulation(self, frequency, modulation):
        # Update the frequency dropdown or custom entry based on the imported value
        if frequency in self.frequencies:
            self.optionmenu_1.set(frequency)
            self.custom_frequency_entry.configure(state="disabled")
        else:
            self.optionmenu_1.set("Custom")
            self.custom_frequency_entry.configure(state="normal")
            self.custom_frequency_entry.delete(0, tk.END)
            self.custom_frequency_entry.insert(0, str(self.frequency))
        if 'AM650' in modulation or 'AM270' in modulation or 'FM238' in modulation or 'FM476' in modulation:
            self.optionmenu_2.set(modulation)
        else:
            self.optionmenu_2.set('AM650')

    def save_capture_to_file(self):
        file_path = filedialog.asksaveasfilename(title="Save Signals", filetypes=[("Text Files", "*.cap"), ("All Files", "*.*")])
        if file_path:
            print(self.entry_baudrate.get())
            print(self.entry_deviation.get())
            with open(file_path, 'w') as file:
                file.write(f'Frequency: {str(self.frequency)}\n')
                file.write(f'Modulation: {self.modulation}\n')
                if self.entry_baudrate.get() != '':
                    file.write(f'Baudrate: {self.entry_baudrate.get()}\n')
                if self.entry_deviation.get() != '':
                    file.write(f'Deviation: {self.entry_deviation.get()}\n')
                for signal in self.yardstick_receiver.signals:
                    file.write(f'Payload: {signal}\n')

if __name__ == "__main__":
    app = App()
    app.mainloop()