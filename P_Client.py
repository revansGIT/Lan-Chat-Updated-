import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
from tkinter import PhotoImage

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Synthwave LAN Chat")
        self.master.geometry("500x600")
        self.master.config(bg='#2C003E')  # Background color for synthwave

        # Set font and colors for synthwave theme
        self.font = ("Helvetica", 14, "bold")
        self.fg_color = "#39FF14"  # Neon green
        self.bg_color = "#2C003E"  # Dark purple
        self.entry_bg_color = "#8A2BE2"  # Blue violet
        self.button_bg_color = "#FF1493"  # Deep pink
        self.button_fg_color = "#FFFFFF"  # White

        self.username = None

        # Login Screen
        self.login_screen()

    def login_screen(self):
        self.login_frame = tk.Frame(self.master, bg=self.bg_color)
        self.login_frame.pack(pady=20)

        # Load the logo image
        try:
            self.logo = PhotoImage(file="logo.png")  # Change this to the path of your logo
        except Exception as e:
            messagebox.showerror("Image Error", f"Error loading logo image: {e}")
            self.logo = None

        if self.logo:
            self.logo_label = tk.Label(self.login_frame, image=self.logo, bg=self.bg_color)
            self.logo_label.pack(pady=10)

        self.username_label = tk.Label(self.login_frame, text="Enter your username:", font=self.font, fg=self.fg_color, bg=self.bg_color)
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(self.login_frame, font=self.font, fg=self.fg_color, bg=self.entry_bg_color, insertbackground=self.fg_color)
        self.username_entry.pack(pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", font=self.font, fg=self.button_fg_color, bg=self.button_bg_color, command=self.connect_to_server)
        self.login_button.pack(pady=10)

    def connect_to_server(self):
        self.username = self.username_entry.get()
        if not self.username:
            messagebox.showerror("Username Error", "Username cannot be empty!")
            return

        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set server IP address (adjust as necessary)
        self.server_ip = '127.0.0.1'  # Change this to the server's IP address if on a different machine
        self.port = 12345  # The same port as used by the server

        try:
            self.client_socket.connect((self.server_ip, self.port))
            self.client_socket.send(self.username.encode('utf-8'))
            self.login_frame.destroy()
            self.chat_screen()
            threading.Thread(target=self.receive_messages).start()
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Connection to the server failed. Ensure the server is running and reachable.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"An error occurred: {e}")
            self.client_socket.close()

    def chat_screen(self):
        self.chat_frame = tk.Frame(self.master, bg=self.bg_color)
        self.chat_frame.pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, font=self.font, fg=self.fg_color, bg=self.bg_color, insertbackground=self.fg_color)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(self.chat_frame, font=self.font, fg=self.fg_color, bg=self.entry_bg_color, insertbackground=self.fg_color, width=50)
        self.message_entry.pack(pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.chat_frame, text="Send", font=self.font, fg=self.button_fg_color, bg=self.button_bg_color, command=self.send_message)
        self.send_button.pack(pady=5)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, message + "\n")
                    self.chat_area.yview(tk.END)
                    self.chat_area.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Connection Error", f"An error occurred while receiving messages: {e}")
                self.client_socket.close()
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            try:
                if message.startswith('/'):
                    self.client_socket.send(message.encode('utf-8'))
                else:
                    self.client_socket.send(message.encode('utf-8'))
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, f"You: {message}\n")
                    self.chat_area.yview(tk.END)
                    self.chat_area.config(state=tk.DISABLED)
                    self.message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Send Error", f"An error occurred while sending message: {e}")
                self.client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
