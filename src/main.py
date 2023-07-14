import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Enigma
import Config

class EnigmaGUI:
    def __init__(self):
        self.config = Config.Config()
        self.rotor_config = [self.config.rotor_I, self.config.rotor_II, self.config.rotor_III]
        self.rotor_positions = [0, 0, 0]
        self.reflector_config = self.config.reflector_B
        self.plugboard_config = []
        self.enigma = Enigma.EnigmaM3(self.rotor_config, self.rotor_positions, self.reflector_config, self.plugboard_config)
        self.rotor_options = ['Rotor I', 'Rotor II', 'Rotor III']

        self.root = tk.Tk()
        self.root.title("Enigma Machine")

        self.create_widgets()

    def create_widgets(self):
        # Rotor Selection
        rotor_label = ttk.Label(self.root, text="Rotor Configurations")
        rotor_label.pack()

        rotor_frame = ttk.Frame(self.root)
        rotor_frame.pack()

        rotor_names = ['Rotor I', 'Rotor II', 'Rotor III']
        self.rotor_options = [ttk.OptionMenu(rotor_frame, tk.StringVar(), name, *self.rotor_options) for name in rotor_names]
        for i, option in enumerate(self.rotor_options):
            option.grid(row=0, column=i, padx=5, pady=5)

        # Rotor Positions
        position_label = ttk.Label(self.root, text="Rotor Positions")
        position_label.pack()

        position_frame = ttk.Frame(self.root)
        position_frame.pack()

        self.position_entries = [ttk.Entry(position_frame, width=5) for _ in range(3)]
        for i, entry in enumerate(self.position_entries):
            entry.insert(0, chr(self.rotor_positions[i] + 65))
            entry.grid(row=0, column=i, padx=5, pady=5)

        # Plugboard Configuration
        plugboard_label = ttk.Label(self.root, text="Plugboard Configuration")
        plugboard_label.pack()

        plugboard_frame = ttk.Frame(self.root)
        plugboard_frame.pack()

        self.plugboard_entries = []
        for i in range(10):
            label = ttk.Label(plugboard_frame, text=i+1)
            label.grid(row=i, column=0, padx=5, pady=5)

            entry1 = ttk.Entry(plugboard_frame, width=5)
            entry1.grid(row=i, column=1, padx=5, pady=5)

            label2 = ttk.Label(plugboard_frame, text="-")
            label2.grid(row=i, column=2, padx=5, pady=5)

            entry2 = ttk.Entry(plugboard_frame, width=5)
            entry2.grid(row=i, column=3, padx=5, pady=5)

            self.plugboard_entries.append((entry1, entry2))

        # Text Input
        input_label = ttk.Label(self.root, text="Text Input")
        input_label.pack()

        input_entry = ttk.Entry(self.root, width=30)
        input_entry.pack(padx=5, pady=5)

        # Ciphertext Display
        ciphertext_label = ttk.Label(self.root, text="Ciphertext")
        ciphertext_label.pack()

        self.ciphertext_text = tk.Text(self.root, height=4, width=30)
        self.ciphertext_text.pack(padx=5, pady=5)

        # Encryption Button
        encrypt_button = ttk.Button(self.root, text="Encrypt", command=lambda: self.encrypt_text(input_entry.get()))
        encrypt_button.pack(pady=10)

    def encrypt_text(self, plaintext):
        self.update_configuration()
        ciphertext = self.enigma.encrypt(plaintext)
        print("Ciphertext: " + ciphertext)
        self.ciphertext_text.delete('1.0', tk.END)
        self.ciphertext_text.insert(tk.END, ciphertext)

    def update_configuration(self):
        # Update Rotor Configurations
        self.rotor_config = []
        for option in self.rotor_options:
            rotor_name = option.cget('text')
            if rotor_name == 'Rotor I':
                self.rotor_config.append(self.config.rotor_I)
            elif rotor_name == 'Rotor II':
                self.rotor_config.append(self.config.rotor_II)
            elif rotor_name == 'Rotor III':
                self.rotor_config.append(self.config.rotor_III)

        # Update Rotor Positions
        for i, entry in enumerate(self.position_entries):
            position = entry.get().upper()
            self.rotor_positions[i] = ord(position) - 65

        # Update Plugboard Configuration
        self.plugboard_config = []
        for entry1, entry2 in self.plugboard_entries:
            letter1 = entry1.get().upper()
            letter2 = entry2.get().upper()
            for plug in self.plugboard_config:
                if letter1 in plug or letter2 in plug:
                    messagebox.showerror("Error", "There are duplicate letters in the plugboard configuration.")
                    return
            if letter1 and letter2:
                self.plugboard_config.append((letter1, letter2))

        # Update Enigma Machine
        self.enigma = Enigma.EnigmaM3(self.rotor_config, self.rotor_positions, self.reflector_config, self.plugboard_config)

    def run(self):
        self.root.mainloop()

enigma_gui = EnigmaGUI()
enigma_gui.run()
