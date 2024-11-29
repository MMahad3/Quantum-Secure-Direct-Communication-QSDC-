import tkinter as tk
import random

class QSDCVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Secure Direct Communication (QSDC) Visualizer")

        # Text box for logs
        self.logs_text = tk.Text(root, height=10, width=80)
        self.logs_text.pack()

        # Entry box for user to input the message
        self.message_entry = tk.Entry(root, width=80)
        self.message_entry.insert(0, "Enter your message here...")
        self.message_entry.bind("<FocusIn>", self.clear_placeholder)  # Clear placeholder on focus
        self.message_entry.pack()

        # Button to start the simulation
        self.start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        # Canvas for visualizing transmission
        self.canvas = tk.Canvas(root, width=700, height=400, bg='white')
        self.canvas.pack()

    def start_simulation(self):
        # Get the user input message and start simulation
        message = self.message_entry.get()
        binary_message = self.convert_to_binary(message)
        self.visualize_qsdc(binary_message)

    def convert_to_binary(self, message):
        """Converts the message into binary."""
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        self.logs_text.insert(tk.END, f"Original binary message: {binary_message}\n")
        return binary_message

    def insert_decoy_bits(self, binary_message, decoy_ratio=0.2):
        """Insert decoy bits into the binary message."""
        decoy_positions = random.sample(range(len(binary_message)), int(len(binary_message) * decoy_ratio))
        decoy_message = list(binary_message)
        for pos in decoy_positions:
            decoy_message.insert(pos, 'd')  # 'd' marks a decoy bit (can be ignored in transmission)
        return ''.join(decoy_message), decoy_positions

    def visualize_qsdc(self, binary_message):
        # Step 1: Show original message
        self.canvas.delete("all")  # Clear previous drawings
        self.canvas.create_text(350, 20, text="Original Message", font=('Helvetica', 14))
        self.canvas.create_text(350, 60, text=binary_message, font=('Courier', 10))

        # Step 2: Add decoy bits and visualize
        binary_with_decoys, decoy_positions = self.insert_decoy_bits(binary_message)
        self.logs_text.insert(tk.END, f"Message with decoy bits: {binary_with_decoys}\n")
        self.canvas.create_text(350, 100, text="Message with Decoy Bits", font=('Helvetica', 14))
        self.canvas.create_text(350, 140, text=binary_with_decoys, font=('Courier', 10))

        # Step 3: Draw participants and transmission line
        alice_x, alice_y = 150, 200
        bob_x, bob_y = 550, 200
        self.canvas.create_oval(alice_x-30, alice_y-30, alice_x+30, alice_y+30, fill="blue", outline="black")
        self.canvas.create_text(alice_x, alice_y, text="Alice", fill="white", font=('Helvetica', 12))
        self.canvas.create_oval(bob_x-30, bob_y-30, bob_x+30, bob_y+30, fill="green", outline="black")
        self.canvas.create_text(bob_x, bob_y, text="Bob", fill="white", font=('Helvetica', 12))
        self.canvas.create_line(alice_x, alice_y, bob_x, bob_y, fill="black", dash=(4, 2))

        # Step 4: Transmission (visualize chunk by chunk)
        total_steps = len(binary_with_decoys)
        self.visualize_transmission_step(binary_with_decoys, 0, total_steps, alice_x, alice_y, bob_x, bob_y)

    def visualize_transmission_step(self, binary_with_decoys, step, total_steps, alice_x, alice_y, bob_x, bob_y):
        """Visualize the transmission of each chunk."""
        if step >= total_steps:
            return  # Stop when all chunks are processed

        # Clear previous chunk visualizations
        self.canvas.delete("chunk")
        self.canvas.create_text(350, 20, text=f"Transmission Step {step + 1}/{total_steps}", font=('Helvetica', 14), tag="chunk")

        # Show each chunk being transmitted
        chunk = binary_with_decoys[step]
        chunk_color = "blue" if chunk != 'd' else "green"  # Decoy bits are green, others are blue
        self.canvas.create_text(350, 60, text=f"Transmitting chunk: {chunk}", font=('Courier', 12), fill=chunk_color, tag="chunk")

        # Simulate interference (randomly for demo)
        intercepted = False
        if random.random() < 0.2 and chunk != 'd':  # 20% chance of interception for non-decoy bits
            intercepted = True
            # Mark interception with a red circle
            interference_x = alice_x + (step / total_steps) * (bob_x - alice_x)
            interference_y = alice_y + (step / total_steps) * (bob_y - alice_y)
            self.canvas.create_oval(interference_x-5, interference_y-5, interference_x+5, interference_y+5, fill="red", tag="chunk")

            # Log interception
            self.logs_text.insert(tk.END, f"Chunk {chunk} was intercepted at step {step + 1}!\n")

        # Step 5: Progress bar
        self.canvas.create_rectangle(50, 100, 650, 120, fill="lightgray", tag="chunk")
        self.canvas.create_rectangle(50, 100, 50 + ((step + 1) / total_steps) * 600, 120, fill="green", tag="chunk")

        # Update transmission in 500ms intervals
        self.canvas.after(500, self.visualize_transmission_step, binary_with_decoys, step + 1, total_steps, alice_x, alice_y, bob_x, bob_y)

    def clear_placeholder(self, event):
        """Clear placeholder text when user starts typing."""
        if self.message_entry.get() == "Enter your message here...":
            self.message_entry.delete(0, tk.END)

# Create the GUI
root = tk.Tk()
app = QSDCVisualizer(root)
root.mainloop()
