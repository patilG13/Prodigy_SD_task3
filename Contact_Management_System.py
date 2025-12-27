import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

class Contact:
    def __init__(self, name, phone, email, category="General"):
        self.name = name
        self.phone = phone
        self.email = email
        self.category = category
        self.id = f"CT{random.randint(1000, 9999)}"
    
    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "category": self.category,
            "id": self.id
        }

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager Pro")
        self.root.geometry("900x600")

        self.colors = {
            "bg": "#f5f5f5",
            "primary": "#2c3e50",
            "secondary": "#3498db",
            "accent": "#e74c3c"
        }
        
        self.file = "contacts.json"
        self.contacts = self.load_contacts()
        self.current_view = "all"
        
        self.setup_gui()
        self.refresh_list()
    
    def load_contacts(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r') as f:
                    data = json.load(f)
                    return [Contact(**item) for item in data]
            except:
                return []
        return []
    
    def save_contacts(self):
        with open(self.file, 'w') as f:
            json.dump([c.to_dict() for c in self.contacts], f, indent=2)
    
    def setup_gui(self):
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        header = tk.Label(main_frame, text="📱 Contact Manager", 
                         font=("Arial", 20, "bold"), 
                         bg=self.colors["primary"], fg="white", pady=10)
        header.pack(fill=tk.X)
        self.stats_label = tk.Label(main_frame, text="", font=("Arial", 10),
                                   bg=self.colors["bg"], fg=self.colors["primary"])
        self.stats_label.pack(pady=5)
        search_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="🔍", bg=self.colors["bg"]).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                                    width=30, font=("Arial", 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        cat_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        cat_frame.pack(fill=tk.X, pady=5)
        
        categories = ["All", "Family", "Friends", "Work", "Business"]
        for cat in categories:
            btn = tk.Button(cat_frame, text=cat, width=10,
                          command=lambda c=cat: self.filter_by_category(c),
                          bg=self.colors["secondary"], fg="white")
            btn.pack(side=tk.LEFT, padx=2)
        tree_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("Name", "Phone", "Email", "Category", "ID")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-Button-1>", self.edit_selected)

        btn_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        btn_frame.pack(fill=tk.X, pady=10)
        
        buttons = [
            ("➕ Add", self.add_contact, "#27ae60"),
            ("✏️ Edit", self.edit_contact, "#f39c12"),
            ("🗑️ Delete", self.delete_contact, "#e74c3c"),
            ("📋 Export", self.export_csv, "#8e44ad"),
            ("📊 Stats", self.show_stats, "#3498db"),
            ("🎲 Random", self.random_contact, "#16a085")
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=cmd, 
                          bg=color, fg="white", font=("Arial", 10, "bold"),
                          width=10, height=2)
            btn.pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(main_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add contacts
        for contact in self.contacts:
            if self.current_view == "all" or contact.category == self.current_view:
                if self.search_var.get().lower() in contact.name.lower() or \
                   self.search_var.get() in contact.phone:
                    self.tree.insert("", tk.END, values=(
                        contact.name, contact.phone, contact.email, 
                        contact.category, contact.id
                    ))
        
        # Update stats
        self.stats_label.config(text=f"📊 Total Contacts: {len(self.contacts)}")
    
    def on_search(self, event):
        self.refresh_list()
    
    def filter_by_category(self, category):
        self.current_view = "all" if category == "All" else category
        self.refresh_list()
        self.status.config(text=f"Showing: {category}")
    
    def add_contact(self):
        dialog = AddEditDialog(self.root, "Add Contact")
        if dialog.result:
            name, phone, email, category = dialog.result
            
            # Check duplicate
            for c in self.contacts:
                if c.phone == phone:
                    messagebox.showerror("Error", "Phone number already exists!")
                    return
            
            contact = Contact(name, phone, email, category)
            self.contacts.append(contact)
            self.save_contacts()
            self.refresh_list()
            self.status.config(text=f"Added: {name}")
    
    def edit_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact to edit")
            return
        
        idx = self.tree.index(selected[0])
        contact = self.contacts[idx]
        
        dialog = AddEditDialog(self.root, "Edit Contact", contact)
        if dialog.result:
            name, phone, email, category = dialog.result
            
            # Update
            contact.name = name
            contact.phone = phone
            contact.email = email
            contact.category = category
            
            self.save_contacts()
            self.refresh_list()
            self.status.config(text=f"Updated: {name}")
    
    def edit_selected(self, event):
        self.edit_contact()
    
    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact to delete")
            return
        
        idx = self.tree.index(selected[0])
        contact = self.contacts[idx]
        
        if messagebox.askyesno("Confirm", f"Delete {contact.name}?"):
            self.contacts.pop(idx)
            self.save_contacts()
            self.refresh_list()
            self.status.config(text=f"Deleted: {contact.name}")
    
    def export_csv(self):
        import csv
        filename = f"contacts_export_{len(self.contacts)}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone", "Email", "Category", "ID"])
            for c in self.contacts:
                writer.writerow([c.name, c.phone, c.email, c.category, c.id])
        
        messagebox.showinfo("Exported", f"Saved to {filename}")
        self.status.config(text=f"Exported {len(self.contacts)} contacts")
    
    def show_stats(self):
        categories = {}
        for c in self.contacts:
            categories[c.category] = categories.get(c.category, 0) + 1
        
        stats = f"📊 Contact Statistics\n\n"
        stats += f"Total: {len(self.contacts)}\n"
        for cat, count in categories.items():
            stats += f"{cat}: {count}\n"
        
        # Show in new window
        stats_win = tk.Toplevel(self.root)
        stats_win.title("Statistics")
        stats_win.geometry("300x200")
        
        text = tk.Text(stats_win, font=("Arial", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, stats)
        text.config(state=tk.DISABLED)
    
    def random_contact(self):
        if self.contacts:
            import random
            contact = random.choice(self.contacts)
            messagebox.showinfo("Random Contact", 
                              f"🎲 Random Pick:\n\nName: {contact.name}\nPhone: {contact.phone}\nEmail: {contact.email}")
        else:
            messagebox.showinfo("No Contacts", "Add some contacts first!")

class AddEditDialog:
    def __init__(self, parent, title, contact=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        self.dialog.geometry(f"+{parent_x+50}+{parent_y+50}")
        
        # Form
        tk.Label(self.dialog, text=title, font=("Arial", 14, "bold")).pack(pady=10)
        
        # Name
        tk.Label(self.dialog, text="Name:").pack(pady=5)
        self.name_var = tk.StringVar(value=contact.name if contact else "")
        tk.Entry(self.dialog, textvariable=self.name_var, width=40).pack()
        
        # Phone
        tk.Label(self.dialog, text="Phone:").pack(pady=5)
        self.phone_var = tk.StringVar(value=contact.phone if contact else "")
        tk.Entry(self.dialog, textvariable=self.phone_var, width=40).pack()
        
        # Email
        tk.Label(self.dialog, text="Email:").pack(pady=5)
        self.email_var = tk.StringVar(value=contact.email if contact else "")
        tk.Entry(self.dialog, textvariable=self.email_var, width=40).pack()
        
        # Category
        tk.Label(self.dialog, text="Category:").pack(pady=5)
        self.category_var = tk.StringVar(value=contact.category if contact else "General")
        categories = ["General", "Family", "Friends", "Work", "Business", "Emergency"]
        ttk.Combobox(self.dialog, textvariable=self.category_var, 
                    values=categories, state="readonly", width=37).pack()
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Save", command=self.on_save, 
                 bg="#27ae60", fg="white", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.on_cancel,
                 bg="#e74c3c", fg="white", width=10).pack(side=tk.LEFT, padx=5)
        
        self.dialog.bind("<Return>", lambda e: self.on_save())
        self.dialog.bind("<Escape>", lambda e: self.on_cancel())
        
        parent.wait_window(self.dialog)
    
    def on_save(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        category = self.category_var.get()
        
        if not name or not phone:
            messagebox.showerror("Error", "Name and phone are required!")
            return
        
        self.result = (name, phone, email, category)
        self.dialog.destroy()
    
    def on_cancel(self):
        self.dialog.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()