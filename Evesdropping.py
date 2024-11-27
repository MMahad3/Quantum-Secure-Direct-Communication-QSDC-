from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import random
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk  


class QSDCSimulationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quantum Secure Direct Communication")
        self.create_gui()

    def create_gui(self):
        tk.Label(self.root, text="Enter your message:").pack(pady=10)
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.pack(pady=5)
        tk.Button(self.root, text="Simulate QSDC", command=self.start_simulation).pack(pady=20)
        self.result_text = tk.Text(self.root, height=15, width=60, wrap=tk.WORD)
        self.result_text.pack(pady=10)
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

    def start_simulation(self):
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Input Error", "Please enter a message.")
            return

        # Ask the user if they want to simulate eavesdropping
        user_choice = messagebox.askyesno("Eavesdropping", "Do you want to simulate eavesdropping?")
        eavesdropping = user_choice  # True if the user clicks 'Yes'

        # Convert the message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Original binary message: {binary_message}\n")
        self.simulate_qsdc(binary_message, eavesdropping)

    def simulate_qsdc(self, binary_message, eavesdropping):
        binary_chunks = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        received_message = ""
        error_positions = []  # To store error positions if any

        for chunk in binary_chunks:
            # Create a quantum circuit for this chunk
            qc = QuantumCircuit(len(chunk), len(chunk))

            # Encode the message chunk
            for i, bit in enumerate(chunk):
                if bit == '1':
                    qc.x(i)  # Apply X gate to encode as |1>
                qc.h(i)  # Apply Hadamard gate

            # Simulate eavesdropping if applicable
            eavesdrop_msg = "No eavesdropping occurred."
            if eavesdropping:
                num_qubits_to_eavesdrop = random.randint(1, len(chunk))
                eavesdropped_indices = random.sample(range(len(chunk)), num_qubits_to_eavesdrop)
                for index in eavesdropped_indices:
                    qc.measure(index, index)
                eavesdrop_msg = f"Eavesdropped qubits: {eavesdropped_indices}"

            # Measure all qubits after encoding
            qc.measure_all()

            # Run the simulation
            simulator = AerSimulator()
            job = simulator.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts(qc)

            # Decode the measured results
            measured_result = list(counts.keys())[0]  # Take the first result
            measured_result = measured_result[::-1]  # Reverse to match qubit order
            received_message += measured_result

            # Display results
            self.result_text.insert(tk.END, f"\nChunk: {chunk}\n")
            self.result_text.insert(tk.END, f"Measurement results: {measured_result}\n")
            self.result_text.insert(tk.END, eavesdrop_msg + "\n")

            # Display the quantum circuit for this chunk
            circuit_image = circuit_drawer(qc, output='mpl')
            plt.close()  # Close the plot to prevent display issues
            circuit_image.savefig("circuit.png")

            # Load and display the image in Tkinter
            img = Image.open("circuit.png")
            img = img.resize((400, 400), Image.Resampling.LANCZOS)  # Corrected resizing
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

        # Error detection: Compare sent and received binary message
        if eavesdropping:  # Error detection only when eavesdropping is simulated
            errors = [i for i, (sent, received) in enumerate(zip(binary_message, received_message)) if sent != received]
            if errors:
                self.result_text.insert(tk.END, f"\nErrors detected at positions: {errors}\n")
            else:
                self.result_text.insert(tk.END, "\nNo errors detected in the message.\n")

        messagebox.showinfo("Simulation Complete", "The QSDC simulation has completed.")

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = QSDCSimulationApp()
    app.run()
