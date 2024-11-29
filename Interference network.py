import tkinter as tk
import random

class QSDCVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Secure Direct Communication (QSDC) Visualizer")

        # Text box for logs
        self.logs_text = tk.Text(root, height=10, width=80)
        self.logs_text.pack()

        # Buttons for different functionalities
        button_frame = tk.Frame(root)
        button_frame.pack()

        # Visualize Photonic Entanglement button
        self.entanglement_button = tk.Button(button_frame, text="Visualize Entanglement", command=self.visualize_entanglement)
        self.entanglement_button.grid(row=0, column=0, padx=5, pady=5)

        # Start Quantum Network Simulation button
        self.network_button = tk.Button(button_frame, text="Simulate Network", command=self.simulate_network)
        self.network_button.grid(row=0, column=1, padx=5, pady=5)

        # Simulate Interference button
        self.interference_button = tk.Button(button_frame, text="Simulate Interference", command=self.simulate_interference)
        self.interference_button.grid(row=0, column=2, padx=5, pady=5)

        # Canvas for visualizing
        self.canvas = tk.Canvas(root, width=700, height=500, bg='white')
        self.canvas.pack()

        # Initialize participants and qubits
        self.participants = {
            "Alice": {"qubits": ["|0⟩", "|1⟩"]},
            "Bob": {"qubits": ["|0⟩", "|1⟩"]},
            "Charlie": {"qubits": ["|0⟩", "|1⟩"]},
            "David": {"qubits": ["|0⟩", "|1⟩"]},
        }
        self.central_x, self.central_y = 350, 200
        self.participant_positions = {
            "Bob": (150, 100),
            "Charlie": (550, 100),
            "David": (350, 350),
        }

    def visualize_entanglement(self):
        """Draw the quantum entanglement network."""
        self.canvas.delete("all")

        # Draw the central trusted user (Alice)
        self.canvas.create_oval(self.central_x-30, self.central_y-30, self.central_x+30, self.central_y+30, fill="blue", outline="black")
        self.canvas.create_text(self.central_x, self.central_y, text="Alice", fill="white", font=('Helvetica', 12))

        # Draw participants and their connections
        for participant, (x, y) in self.participant_positions.items():
            # Draw participant nodes
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="green", outline="black")
            self.canvas.create_text(x, y, text=participant, fill="white", font=('Helvetica', 12))

            # Draw entanglement lines
            self.canvas.create_line(self.central_x, self.central_y, x, y, fill="cyan", width=2)

    def simulate_network(self):
        """Simulate quantum network communication."""
        self.visualize_entanglement()

        # Allow users to select sender and receiver
        def send_message():
            sender = sender_var.get()
            receiver = receiver_var.get()
            if sender == receiver:
                self.logs_text.insert(tk.END, "Sender and receiver cannot be the same.\n")
                return

            self.logs_text.insert(tk.END, f"Message sent from {sender} to {receiver}.\n")
            self.visualize_message_flow(sender, receiver)

        # Dropdown menus for sender and receiver
        sender_var = tk.StringVar(value="Alice")
        receiver_var = tk.StringVar(value="Bob")
        sender_menu = tk.OptionMenu(self.root, sender_var, *self.participants.keys())
        receiver_menu = tk.OptionMenu(self.root, receiver_var, *self.participants.keys())
        sender_menu.pack()
        receiver_menu.pack()

        # Send button
        send_button = tk.Button(self.root, text="Send Message", command=send_message)
        send_button.pack()

    def visualize_message_flow(self, sender, receiver):
        """Overlay the message flow visualization on the existing network."""
        # Keep the network intact
        self.visualize_entanglement()

        # Determine positions of sender and receiver
        sender_x, sender_y = (self.central_x, self.central_y) if sender == "Alice" else self.participant_positions[sender]
        receiver_x, receiver_y = (self.central_x, self.central_y) if receiver == "Alice" else self.participant_positions[receiver]

        # Highlight sender and receiver
        self.canvas.create_oval(sender_x-20, sender_y-20, sender_x+20, sender_y+20, fill="yellow", outline="black")
        self.canvas.create_text(sender_x, sender_y, text=sender, fill="black", font=('Helvetica', 12))

        self.canvas.create_oval(receiver_x-20, receiver_y-20, receiver_x+20, receiver_y+20, fill="orange", outline="black")
        self.canvas.create_text(receiver_x, receiver_y, text=receiver, fill="black", font=('Helvetica', 12))

        # Draw message flow
        self.canvas.create_line(sender_x, sender_y, receiver_x, receiver_y, fill="red", width=3, dash=(5, 2))

        # Show qubits and collapse
        sender_qubit = random.choice(self.participants[sender]["qubits"])
        receiver_qubit = random.choice(self.participants[receiver]["qubits"])

        self.logs_text.insert(tk.END, f"{sender}'s qubit: {sender_qubit}\n")
        self.logs_text.insert(tk.END, f"{receiver}'s qubit before collapse: {receiver_qubit}\n")

        collapsed_qubit = sender_qubit  # Simulate collapse
        self.logs_text.insert(tk.END, f"Receiver's qubit after collapse: {collapsed_qubit}\n")
        self.participants[receiver]["qubits"].remove(receiver_qubit)
        self.participants[receiver]["qubits"].append(collapsed_qubit)

        # Display collapsed qubits
        self.canvas.create_text(350, 450, text=f"{receiver}'s updated qubits: {self.participants[receiver]['qubits']}", font=('Courier', 12), fill="black")

    def simulate_interference(self):
        """Simulate interference on the quantum network."""
        self.logs_text.insert(tk.END, "Interference detected in the network!\n")
        
        # Visualize disrupted entanglement
        self.visualize_entanglement()

        # Highlight interference lines
        for participant, (x, y) in self.participant_positions.items():
            self.canvas.create_line(self.central_x, self.central_y, x, y, fill="magenta", width=2, dash=(3, 3))
            self.logs_text.insert(tk.END, f"Interference on link between Alice and {participant}.\n")


# Create the GUI
root = tk.Tk()
app = QSDCVisualizer(root)
root.mainloop()
