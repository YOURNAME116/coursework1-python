import tkinter as tk
from tkinter import messagebox
import threading
import socket
import concurrent.futures


class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner")
        self.root.geometry("500x500")

        self.host_label = tk.Label(root, text="Host:")
        self.host_label.pack()
        self.host_entry = tk.Entry(root)
        self.host_entry.pack()

        self.scan_type_var = tk.StringVar(value="all")
        self.scan_all_radiobutton = tk.Radiobutton(root, text="Scan All Ports", variable=self.scan_type_var, value="all", command=self.update_scan_type)
        self.scan_all_radiobutton.pack()
        self.scan_specific_radiobutton = tk.Radiobutton(root, text="Scan Specific Ports", variable=self.scan_type_var, value="specific", command=self.update_scan_type)
        self.scan_specific_radiobutton.pack()

        self.port_range_frame = tk.Frame(root)
        self.start_port_label = tk.Label(self.port_range_frame, text="Start Port:")
        self.start_port_label.pack(side=tk.LEFT)
        self.start_port_entry = tk.Entry(self.port_range_frame)
        self.start_port_entry.pack(side=tk.LEFT)
        self.end_port_label = tk.Label(self.port_range_frame, text="End Port:")
        self.end_port_label.pack(side=tk.LEFT)
        self.end_port_entry = tk.Entry(self.port_range_frame)
        self.end_port_entry.pack(side=tk.LEFT)
        self.port_range_frame.pack()

        self.specific_ports_label = tk.Label(root, text="Specific Ports (Comma-separated):")
        self.specific_ports_label.pack()
        self.specific_ports_entry = tk.Entry(root)
        self.specific_ports_entry.pack()

        self.output_label = tk.Label(root, text="Output File:")
        self.output_label.pack()
        self.output_entry = tk.Entry(root)
        self.output_entry.pack()

        self.version_check_var = tk.IntVar()
        self.version_check_button = tk.Checkbutton(root, text="Service Version Detection",
                                                   variable=self.version_check_var)
        self.version_check_button.pack()

        self.scan_button = tk.Button(root, text="Scan", command=self.start_scan)
        self.scan_button.pack()

        self.result_text = tk.Text(root, height=10, width=40)
        self.result_text.pack()

        self.scan_thread = None

    def update_scan_type(self):
        scan_type = self.scan_type_var.get()
        if scan_type == "all":
            self.port_range_frame.pack()
            self.specific_ports_label.pack_forget()
            self.specific_ports_entry.pack_forget()
            
           
            
        elif scan_type == "specific":
            self.port_range_frame.pack_forget()
            self.specific_ports_label.pack()
            self.specific_ports_entry.pack()
            

    def start_scan(self):
        if self.scan_thread and self.scan_thread.is_alive():
            messagebox.showinfo("Scan in Progress", "A scan is already in progress.")
            return

        host = self.host_entry.get()
        scan_type = self.scan_type_var.get()
        if scan_type == "all":
            start_port = int(self.start_port_entry.get())
            end_port = int(self.end_port_entry.get())
            if start_port > end_port:
                messagebox.showerror("Error", "Start port cannot be greater than end port.")
                return
            ports_to_scan = range(start_port, end_port + 1)
        elif scan_type == "specific":
            specific_ports = self.specific_ports_entry.get().split(",")
            specific_ports = [int(port.strip()) for port in specific_ports if port.strip()]
            if not specific_ports:
                messagebox.showerror("Error", "Please provide at least one specific port.")
                return
            ports_to_scan = specific_ports
        else:
            messagebox.showerror("Error", "Invalid scan type.")
            return

        output_file = self.output_entry.get()
        if output_file and not output_file.endswith(".txt"):
            messagebox.showerror("Error", "Invalid output file extension. Please use a .txt file.")
            return

        self.result_text.delete("1.0", tk.END)  # Clear output

        self.scan_thread = threading.Thread(target=self.scan_ports, args=(host, ports_to_scan, output_file))
        self.scan_thread.start()

    def scan_ports(self, host, ports, output_file):
        open_ports = []

        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except socket.error:
                pass

        if open_ports:
            self.result_text.insert(tk.END, "Open Ports:\n")
            for port in open_ports:
                self.result_text.insert(tk.END, f"{port}\n")
        else:
            self.result_text.insert(tk.END, "No open ports found.")

        if self.version_check_var.get() == 1:
            self.result_text.insert(tk.END, "\nPerforming Service Version Detection...\n")
            self.perform_service_version_detection(host, open_ports)

        if output_file:
            self.save_output(output_file)

    def perform_service_version_detection(self, host, open_ports):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_port = {executor.submit(self.detect_service_version, host, port): port for port in open_ports}
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    service_version = future.result()
                    self.result_text.insert(tk.END, f"Port {port}: {service_version}\n")
                except Exception as exc:
                    self.result_text.insert(tk.END, f"Port {port}: Error occurred during service version detection\n")

    def detect_service_version(self, host, port):
        try:
            service_version = "Unknown"
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                sock.connect((host, port))
                sock.sendall(b"GET / HTTP/1.1\r\n\r\n")
                response = sock.recv(1024)
                if response:
                    service_version = response.decode().splitlines()[0]
            return service_version
        except socket.error:
            return "Unknown"

    def save_output(self, filename):
        try:
            if not filename.endswith(".txt"):
                messagebox.showerror("Error", "Invalid output file extension. Please use a .txt file.")
                return

            with open(filename, 'w') as file:
                file.write(self.result_text.get("1.0", tk.END))
            messagebox.showinfo("Success", f"Output saved to {filename}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the output: {str(e)}")


root = tk.Tk()
port_scanner = PortScannerGUI(root)
root.mainloop()
