import tkinter as tk
import qrcode, random
from PIL import ImageTk

# GUI for Command Generation
class CommandGeneratorGUI:
    def __init__(self, root, generator, egpsr_generator):
        self.root = root
        self.root.title("Command Generator")

        # Command Generators
        self.generator = generator
        self.egpsr_generator = egpsr_generator

        # Create a frame to contain the buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # Create command options
        self.user_prompt_label = tk.Label(root, text="Select Command Option:")
        self.user_prompt_label.pack()

        # Arrange buttons side by side using grid
        self.btn_any_command = tk.Button(self.button_frame, text="Any Command", command=self.generate_any_command)
        self.btn_any_command.grid(row=0, column=0, padx=5, pady=5)

        self.btn_no_manipulation = tk.Button(self.button_frame, text="No Manipulation", command=self.generate_no_manipulation_command)
        self.btn_no_manipulation.grid(row=0, column=1, padx=5, pady=5)

        self.btn_with_manipulation = tk.Button(self.button_frame, text="With Manipulation", command=self.generate_with_manipulation_command)
        self.btn_with_manipulation.grid(row=0, column=2, padx=5, pady=5)

        self.btn_batch_commands = tk.Button(self.button_frame, text="Batch of Three", command=self.generate_batch_commands)
        self.btn_batch_commands.grid(row=1, column=0, padx=5, pady=5)

        self.btn_egpsr = tk.Button(self.button_frame, text="EGPSR Setup", command=self.generate_egpsr_setup)
        self.btn_egpsr.grid(row=1, column=1, padx=5, pady=5)

        # Display area for commands
        self.command_display = tk.Text(root, height=10, width=80)
        self.command_display.pack(pady=5)

        # Frame to hold QR codes
        self.qr_frame = tk.Frame(root)
        self.qr_frame.pack(pady=10)

        self.command = ""
        self.command_list = []


    # Method to exit full-screen mode
    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

    def display_command(self, command):
        self.command_display.delete(1.0, tk.END)
        self.command_display.insert(tk.END, command)

        # Automatically generate and display a single QR code
        self.generate_qr_code([command])

    def generate_any_command(self):
        self.command = self.generator.generate_command_start(cmd_category="")
        self.command = self.command[0].upper() + self.command[1:]
        self.display_command(self.command)

    def generate_no_manipulation_command(self):
        self.command = self.generator.generate_command_start(cmd_category="people")
        self.command = self.command[0].upper() + self.command[1:]
        self.display_command(self.command)

    def generate_with_manipulation_command(self):
        self.command = self.generator.generate_command_start(cmd_category="objects")
        self.command = self.command[0].upper() + self.command[1:]
        self.display_command(self.command)

    def generate_batch_commands(self):
        command_one = self.generator.generate_command_start(cmd_category="people")
        command_two = self.generator.generate_command_start(cmd_category="objects")
        command_three = self.generator.generate_command_start(cmd_category="")
        self.command_list = [command_one[0].upper() + command_one[1:], command_two[0].upper() + command_two[1:], command_three[0].upper() + command_three[1:]]
        random.shuffle(self.command_list)

        # Display the batch of commands
        batch_command = "\n".join(self.command_list)
        self.command_display.delete(1.0, tk.END)
        self.command_display.insert(tk.END, batch_command)

        # Generate and display QR codes for the batch
        self.generate_qr_code(self.command_list)

    def generate_egpsr_setup(self):
        self.command = self.egpsr_generator.generate_setup()
        self.display_command(self.command)

    def generate_qr_code(self, command_list):
        # Clear the previous QR codes
        for widget in self.qr_frame.winfo_children():
            widget.destroy()

        # Generate and display QR code for each command in the list
        for command_text in command_list:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=4,
            )
            qr.add_data(command_text)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((300, 300))  # Resize to fit the window

            # Convert the image to PhotoImage for displaying in Tkinter
            img_tk = ImageTk.PhotoImage(img)

            # Create a label to hold each QR code and display it in the grid
            qr_label = tk.Label(self.qr_frame, image=img_tk)
            qr_label.image = img_tk  # Keep a reference to avoid garbage collection
            qr_label.pack(side=tk.LEFT, padx=10)  # Align QR codes horizontally



# class CommandGeneratorGUI:
#     def __init__(self, root, generator, egpsr_generator):
#         self.root = root
#         self.root.title("Command Generator")

#         # Command Generators
#         self.generator = generator
#         self.egpsr_generator = egpsr_generator

#         # Create command options
#         self.user_prompt_label = tk.Label(root, text="Select Command Option:")
#         self.user_prompt_label.pack()

#         # Create a frame to contain the buttons
#         self.button_frame = tk.Frame(root)
#         self.button_frame.pack(pady=10)

#         # Arrange buttons side by side using grid
#         self.btn_any_command = tk.Button(self.button_frame, text="Any Command", command=self.generate_any_command)
#         self.btn_any_command.grid(row=0, column=0, padx=5, pady=5)

#         self.btn_no_manipulation = tk.Button(self.button_frame, text="No Manipulation", command=self.generate_no_manipulation_command)
#         self.btn_no_manipulation.grid(row=0, column=1, padx=5, pady=5)

#         self.btn_with_manipulation = tk.Button(self.button_frame, text="With Manipulation", command=self.generate_with_manipulation_command)
#         self.btn_with_manipulation.grid(row=0, column=2, padx=5, pady=5)

#         self.btn_batch_commands = tk.Button(self.button_frame, text="Batch of Three", command=self.generate_batch_commands)
#         self.btn_batch_commands.grid(row=1, column=0, padx=5, pady=5)

#         self.btn_egpsr = tk.Button(self.button_frame, text="EGPSR Setup", command=self.generate_egpsr_setup)
#         self.btn_egpsr.grid(row=1, column=1, padx=5, pady=5)

#         self.btn_generate_qr = tk.Button(self.button_frame, text="Generate QR Code", command=self.generate_qr_code)
#         self.btn_generate_qr.grid(row=1, column=2, padx=5, pady=5)

#         self.command_display = tk.Text(root, height=10, width=100)
#         self.command_display.pack(pady=5)

#         self.command = ""
#         self.command_list = []

#     def display_command(self, command):
#         self.command_display.delete(1.0, tk.END)
#         self.command_display.insert(tk.END, command)

#     def generate_any_command(self):
#         self.command = self.generator.generate_command_start(cmd_category="")
#         self.command = self.command[0].upper() + self.command[1:]
#         self.display_command(self.command)

#     def generate_no_manipulation_command(self):
#         self.command = self.generator.generate_command_start(cmd_category="people")
#         self.command = self.command[0].upper() + self.command[1:]
#         self.display_command(self.command)

#     def generate_with_manipulation_command(self):
#         self.command = self.generator.generate_command_start(cmd_category="objects")
#         self.command = self.command[0].upper() + self.command[1:]
#         self.display_command(self.command)

#     def generate_batch_commands(self):
#         command_one = self.generator.generate_command_start(cmd_category="people")
#         command_two = self.generator.generate_command_start(cmd_category="objects")
#         command_three = self.generator.generate_command_start(cmd_category="")
#         self.command_list = [command_one[0].upper() + command_one[1:], command_two[0].upper() + command_two[1:], command_three[0].upper() + command_three[1:]]
#         random.shuffle(self.command_list)
#         batch_command = "\n".join(self.command_list)
#         self.display_command(batch_command)

#     def generate_egpsr_setup(self):
#         self.command = self.egpsr_generator.generate_setup()
#         self.display_command(self.command)

#     def generate_qr_code(self):
#         if not self.command and not self.command_list:
#             messagebox.showwarning("Warning", "No command generated yet.")
#             return

#         commands = self.command_list if self.command_list else [self.command]

#         for c in commands:
#             qr = qrcode.QRCode(
#                 version=1,
#                 error_correction=qrcode.constants.ERROR_CORRECT_L,
#                 box_size=10,
#                 border=4,
#             )
#             qr.add_data(c)
#             qr.make(fit=True)
#             img = qr.make_image(fill_color="black", back_color="white")

#             # Convert QR code to ImageTk for display
#             img_tk = ImageTk.PhotoImage(img)

#             # Display QR code in new window
#             qr_window = tk.Toplevel(self.root)
#             qr_window.title("QR Code")

#             # Add QR Code label to window
#             qr_label = tk.Label(qr_window, image=img_tk)
#             qr_label.image = img_tk  # Keep a reference to avoid garbage collection
#             qr_label.pack()

#             # Add the command text under the QR code
#             command_label = tk.Label(qr_window, text=c, wraplength=300)
#             command_label.pack(pady=5)