import tkinter as tk
from tkinter import messagebox
import requests
import json
import os
from src.ingest.spec_parser import parse_endpoints
from src.agent.testcase_gen import generate_testcases
from src.agent.save_csv import save_csv

def load_spec(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        os.makedirs("data", exist_ok=True)
        with open("data/spec.json", "w") as f:
            json.dump(data, f, indent=2)
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load spec: {str(e)}")
        return None

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("API Test Case Generator")
        self.endpoints = []

        tk.Label(root, text="API Doc URL:").pack(pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "https://petstore3.swagger.io/api/v3/openapi.json")

        self.load_btn = tk.Button(root, text="Load and List Endpoints", command=self.load_endpoints)
        self.load_btn.pack(pady=10)

        tk.Label(root, text="Select Endpoints:").pack(pady=5)
        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=80, height=15)
        self.listbox.pack(pady=5)

        self.gen_btn = tk.Button(root, text="Generate Test Cases", command=self.generate_tests, state=tk.DISABLED)
        self.gen_btn.pack(pady=10)

    def load_endpoints(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        spec = load_spec(url)
        if spec:
            self.endpoints = parse_endpoints(spec)
            self.listbox.delete(0, tk.END)
            for ep in self.endpoints:
                self.listbox.insert(tk.END, f"{ep['method']} {ep['path']}")
            self.gen_btn.config(state=tk.NORMAL)
            messagebox.showinfo("Success", f"Loaded {len(self.endpoints)} endpoints")

    def generate_tests(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one endpoint")
            return
        selected_eps = [self.endpoints[i] for i in selected_indices]
        try:
            csv_text = generate_testcases(selected_eps)
            save_csv(csv_text)
            messagebox.showinfo("Success", "Test cases generated and saved to data/testcase_matrix.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate tests: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()