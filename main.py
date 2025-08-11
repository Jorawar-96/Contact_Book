import tkinter as tk
import json
from tkinter import messagebox
import os
from tkinter import ttk

contact_file = "./contact.json"
displayed_indices = []
def load_contact():
    try:
        with open(contact_file,"r") as file:
            return json.load(file)
    except (FileNotFoundError,json.JSONDecodeError):
        return []

def save_contact():
    with open(contact_file,'w') as file:
        return json.dump(contact_storage,file,indent=4)

def add():
    name = name_entry.get()
    number = number_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if not name or not number:
        messagebox.showerror("Error" ," Name and Number is required")
        return
    if number.isdigit() == False:
        messagebox.showwarning("Error ", "Number should be digits only")
        return
    data_list = {"name":name,"number":number,"email":email,"address":address}
    contact_storage.append(data_list)
    save_contact()
    refresh_list()
    clear_fields()

def delete():
    selected = contact_list.selection()
    if not selected:
        messagebox.showwarning("Warning" ," Please select an contact to delete")
        return
    index = int(selected[0])
    real_index = displayed_indices[index]
    if messagebox.askyesno("Confirm Delete", "Are you sure to delete this contact ?"):
        del contact_storage[real_index]
        save_contact()
        refresh_list()
        clear_fields()

def update():
    selected = contact_list.selection()
    if not selected:
        messagebox.showwarning("Warning","Please select an contact to update")
        return
    index = contact_list.index(selected[0])
    real_index = displayed_indices[index]
    contact_storage[real_index] = {
        "name" : name_entry.get(),
        "number":number_entry.get(),
        "email":email_entry.get(),
        "address":address_entry.get()
    }
    save_contact()
    refresh_list()
    clear_fields()

def refresh_list():
    global displayed_indices
    contact_list.delete(*contact_list.get_children())
    displayed_indices = []
    for idx,contact in enumerate(contact_storage):
        contact_list.insert("","end",iid=idx,values=[contact["name"],contact["number"],contact["email"],contact["address"]])
        displayed_indices.append(idx)

def clear_fields():
    name_entry.set("")
    number_entry.set("")
    email_entry.set("")
    address_entry.set("")

def search_list():
    global displayed_indices
    query = search_entry.get().lower()

    if not query:
        refresh_list()
        return

    if not contact_storage:
        messagebox.showinfo("Info", "No contacts available")
        return
    contact_list.delete(*contact_list.get_children())
    displayed_indices=[]
    for idx,contact in enumerate(contact_storage):
        if (query in contact["name"].lower() or
            query in contact["number"] or 
            query in contact["email"].lower() or
            query in contact["address"].lower()):
            contact_list.insert("","end",iid=idx,values = [contact["name"],contact["number"],contact["email"],contact["address"]])
            displayed_indices.append(idx)

def on_select(event):
    selected = contact_list.selection()
    if not selected:
        return
    index = int(selected[0])
    contact = contact_storage[displayed_indices[index]]
    name_entry.set(contact["name"])
    number_entry.set(contact["number"])
    email_entry.set(contact["email"])
    address_entry.set(contact["address"])

root = tk.Tk()
root.title("Contact Book")
root.geometry("700x500")
root.resizable(False,False)

contact_storage = load_contact()

name_entry = tk.StringVar()
number_entry = tk.StringVar()
email_entry = tk.StringVar()
address_entry = tk.StringVar()
search_entry = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame,text="Name").grid(row=0,column=0,padx=10)
tk.Entry(frame,textvariable=name_entry).grid(row=0,column=1,padx=10)

tk.Label(frame,text="Number").grid(row=0,column=2,padx=10)
tk.Entry(frame,textvariable=number_entry).grid(row=0,column=3,padx=10)

tk.Label(frame,text="E-mail").grid(row=1,column=0,padx=10)
tk.Entry(frame,textvariable=email_entry).grid(row=1,column=1,padx=10)

tk.Label(frame,text="Address").grid(row=1,column=2,padx=10)
tk.Entry(frame,textvariable=address_entry).grid(row=1,column=3,padx=10)

btnframe = tk.Frame(root)
btnframe.pack(pady=10)
tk.Button(btnframe,text="Add",command=add,width=12).grid(row=0,column=0,padx=5)
tk.Button(btnframe,text="Edit",command=update,width=12).grid(row=0,column=2,padx=5)
tk.Button(btnframe,text="Delete",command=delete,width=12).grid(row=0,column=3,padx=5)
tk.Button(btnframe,text="Clear",command=clear_fields,width=12).grid(row=0,column=1,padx=5)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)
tk.Label(search_frame,textvariable=search_entry).pack()
tk.Button(search_frame,text="Search",command=search_list).pack()

columns = ("Name","Number","E-mail","Address")
contact_list = ttk.Treeview(root,columns=columns,show="headings",height=15)
for col in columns:
    contact_list.heading(col,text=col)
    contact_list.column(col,width=150)
contact_list.pack(pady=10)
contact_list.bind("<<TreeviewSelect>>",on_select)


refresh_list()

root.mainloop()