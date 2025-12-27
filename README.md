📱 Contact Manager Pro

A desktop GUI contact management system built with Python and Tkinter. Features intuitive controls, persistent storage, search, filtering, and export capabilities.

Features

📇 Contact Management – Add, edit, delete, and view contacts

🏷️ Category Filtering – Organize by Family, Friends, Work, Business, etc.

🔍 Real-time Search – Filter contacts by name or phone number

💾 Persistent Storage – Automatically saves to contacts.json

📤 CSV Export – Export all contacts to a CSV file

📊 Statistics – View contact distribution by category

🎲 Random Contact Picker – Quick random contact selection

🎨 Clean Interface – Modern GUI with color-coded buttons

Requirements

Python 3.x

tkinter (included with Python)

How to Run

bash
python Contact_Management_System.py
File Structure
Contact_Management_System.py – Main application file

contacts.json – Automatically created/updated contact database

contacts_export_*.csv – Exported CSV files (when using export feature)

Contact Information

Each contact stores:

Name (required)

Phone (required, unique)

Email (optional)

Category (General, Family, Friends, Work, Business, Emergency)

ID (automatically generated unique identifier)

Controls

Button	Function
➕ Add	Add new contact
✏️ Edit	Edit selected contact (double-click row)
🗑️ Delete	Remove selected contact
📋 Export	Export all contacts to CSV
📊 Stats	Show category statistics
🎲 Random	Pick and display random contact
Filtering & Search
Category Buttons – Show All/Family/Friends/Work/Business

Search Box – Real-time filtering by name or phone

Double-click any row to edit the contact

Data Persistence
Contacts are automatically saved to contacts.json

JSON format ensures easy readability and backup

Duplicate phone numbers are prevented

Export Feature
Exports all contacts to a CSV file named contacts_export_##.csv, where ## is the number of contacts. Includes all contact fields.
