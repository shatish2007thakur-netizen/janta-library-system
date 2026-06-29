import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class LibrarySystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Janta Library management System")
        self.root.geometry("1000x600")

        # --- Top Title Banner ---
        title_banner = tk.Label(
            self.root,
            text="SHREE JANTA SECONDARY SCHOOL LIBRARY MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#2980b9",
            fg="white",
            height=2,
        )
        title_banner.pack(fill=tk.X)

        # --- Main Workspace Split ---
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Sidebar (Data Entry)
        self.left_frame = tk.Frame(self.main_frame, bg="#1cc5b1", width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.left_frame.pack_propagate(False)

        # Right Area (Controls & Table)
        self.right_frame = tk.Frame(self.main_frame, bg="#db34c5")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Left Sidebar Widgets ---
        self.create_left_widgets()

        # --- Right Area Widgets ---
        self.create_right_widgets()

    def create_left_widgets(self):
        # Universal styling configuration for entries
        label_config = {
            "bg": "#e985d7",
            "fg": "black",
            "font": ("Arial", 12, "bold"),
        }
        entry_config = {"font": ("Arial", 12), "bd": 1, "relief": tk.SOLID}

        # Book Name
        tk.Label(self.left_frame, text="Book Name", **label_config).pack(
            pady=(20, 5)
        )
        self.ent_book_name = tk.Entry(self.left_frame, **entry_config)
        self.ent_book_name.pack(pady=5, ipady=3, padx=20, fill=tk.X)

        # Book ID
        tk.Label(self.left_frame, text="Book ID", **label_config).pack(
            pady=(15, 5)
        )
        self.ent_book_id = tk.Entry(self.left_frame, **entry_config)
        self.ent_book_id.pack(pady=5, ipady=3, padx=20, fill=tk.X)

        # Author Name
        tk.Label(self.left_frame, text="Author Name", **label_config).pack(
            pady=(15, 5)
        )
        self.ent_author = tk.Entry(self.left_frame, **entry_config)
        self.ent_author.pack(pady=5, ipady=3, padx=20, fill=tk.X)

        # Status of the Book
        tk.Label(self.left_frame, text="Status of the Book", **label_config).pack(
            pady=(15, 5)
        )
        self.status_var = tk.StringVar(value="Available")
        self.combo_status = ttk.Combobox(
            self.left_frame,
            textvariable=self.status_var,
            values=["Available", "Issued"],
            state="readonly",
            font=("Arial", 11),
        )
        self.combo_status.pack(pady=5, ipady=3, padx=20, fill=tk.X)

        # Issuer's Card ID
        tk.Label(self.left_frame, text="Issuer's Card ID", **label_config).pack(
            pady=(15, 5)
        )
        self.ent_card_id = tk.Entry(self.left_frame, **entry_config)
        self.ent_card_id.pack(pady=5, ipady=3, padx=20, fill=tk.X)

        # Add New Record Button
        btn_add = tk.Button(
            self.left_frame,
            text="Add new record",
            font=("Arial", 12, "bold"),
            bg="#151fd8",
            fg="white",
            command=self.add_record,
        )
        btn_add.pack(pady=30, padx=40, fill=tk.X, ipady=5)

    def create_right_widgets(self):
        # Top Action Button Bar
        btn_frame = tk.Frame(self.right_frame, bg="#3498db")
        btn_frame.pack(fill=tk.X, pady=20, padx=10)

        # FIXED: Removed 'ipady' from button dictionary settings
        btn_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#2c502f",
            "fg": "white",
            "width": 15,
        }

        # FIXED: Transferred ipady=5 to the .pack() layout configurations
        tk.Button(
            btn_frame, text="Delete record", command=self.delete_record, **btn_style
        ).pack(side=tk.LEFT, padx=10, expand=True, ipady=5)
        tk.Button(
            btn_frame, text="View record", command=self.view_record, **btn_style
        ).pack(side=tk.LEFT, padx=10, expand=True, ipady=5)
        tk.Button(
            btn_frame,
            text="Delete All Records",
            command=self.delete_all,
            **btn_style
        ).pack(side=tk.LEFT, padx=10, expand=True, ipady=5)
        tk.Button(
            btn_frame, text="Clear fields", command=self.clear_fields, **btn_style
        ).pack(side=tk.LEFT, padx=10, expand=True, ipady=5)

        # Table Header Banner
        table_title = tk.Label(
            self.right_frame,
            text="INFORMATION ABOUT ALL THE BOOKS",
            font=("Arial", 14, "bold"),
            bg="#0066cc",
            fg="white",
            pady=8,
        )
        table_title.pack(fill=tk.X, pady=(10, 0))

        # Data Treeview Table Container
        tree_frame = tk.Frame(self.right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("name", "id", "author", "status", "card")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", selectmode="browse"
        )

        # Define Columns
        self.tree.heading("name", text="Book Name")
        self.tree.heading("id", text="Book ID")
        self.tree.heading("author", text="Author")
        self.tree.heading("status", text="Status of the Book")
        self.tree.heading("card", text="Card ID of the Issuer")

        self.tree.column("name", width=200, anchor=tk.W)
        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("author", width=150, anchor=tk.W)
        self.tree.column("status", width=120, anchor=tk.CENTER)
        self.tree.column("card", width=130, anchor=tk.CENTER)

        # Scrollbars
        vsb = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        hsb = ttk.Scrollbar(
            tree_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Inject Dummy Data seen in screenshot
        self.insert_mock_data()

    # --- Logic Operations ---
    def insert_mock_data(self):
        mock_data = [
            ("HP1", "0001", "JK Rowling", "Available", ""),
            ("Harry Potter 2", "0002", "JK Rowling", "Available", ""),
            (
                "Percy Jackson and the Olympians",
                "0103",
                "Rick Riordan",
                "Issued",
                "PG-10981",
            ),
            ("Think Python", "1098", "Allen B. Downey", "Available", ""),
            ("Famous Five 1", "4567", "Enid Blyton", "Issued", "PG-1290"),
            ("Python GUI Programming", "8653", "Allen D. Moore", "Available", ""),
        ]
        for row in mock_data:
            self.tree.insert("", tk.END, values=row)

    def add_record(self):
        name = self.ent_book_name.get()
        bid = self.ent_book_id.get()
        author = self.ent_author.get()
        status = self.status_var.get()
        card = self.ent_card_id.get()

        if not name or not bid:
            messagebox.showerror("Error", "Book Name and ID are mandatory!")
            return

        self.tree.insert("", tk.END, values=(name, bid, author, status, card))
        self.clear_fields()

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        self.tree.delete(selected_item)

    def delete_all(self):
        if messagebox.askyesno("Confirm", "Delete all records?"):
            for item in self.tree.get_children():
                self.tree.delete(item)

    def clear_fields(self):
        self.ent_book_name.delete(0, tk.END)
        self.ent_book_id.delete(0, tk.END)
        self.ent_author.delete(0, tk.END)
        self.status_var.set("Available")
        self.ent_card_id.delete(0, tk.END)

    def view_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to view")
            return
        values = self.tree.item(selected_item, "values")

        self.clear_fields()
        self.ent_book_name.insert(0, values[0])
        self.ent_book_id.insert(0, values[1])
        self.ent_author.insert(0, values[2])
        self.status_var.set(values[3])
        self.ent_card_id.insert(0, values[4])


if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()
