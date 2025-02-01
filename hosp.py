import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


def create_connection():                                                           #establish mysql data connection
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='*********', 
            database='hospital'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def add_patient():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, address, phone) VALUES (%s, %s, %s, %s, %s)",
                       (entry_name.get(), entry_age.get(), combo_gender.get(), entry_address.get(), entry_phone.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Patient added successfully!")
        display_patients()
    else:
        messagebox.showerror("Error", "Failed to connect to the database")

def display_patients():                                                           #Displays patients details in the treeview

    for row in treeview.get_children():
        treeview.delete(row)
    
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM patients")
        records = cursor.fetchall()
        for row in records:
            treeview.insert("", "end", values=row)
        connection.close()

def update_patient():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Select Patient", "Please select a patient to update")
        return

    patient_id = treeview.item(selected_item, "values")[0]
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE patients SET name = %s, age = %s, gender = %s, address = %s, phone = %s",
                       (entry_name.get(), entry_age.get(), combo_gender.get(), entry_address.get(), entry_phone.get()))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Patient updated successfully!")
        display_patients()
    else:
        messagebox.showerror("Error", "Failed to connect to the database")

def delete_patient():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Select Patient", "Please select a patient to delete")
        return

    patient_id = treeview.item(selected_item, "values")[0]
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Patient deleted successfully!")
        display_patients()
    else:
        messagebox.showerror("Error", "Failed to connect to the database")

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    combo_gender.set("")
    entry_address.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
   

root = tk.Tk()                                                                      #Creates the main Tkinter window
root.title("HOSPITAL MANAGEMENT SYSTEM")
root.geometry("1000x700")


frame_title = tk.Frame(root, bg="lightblue")
frame_title.pack(fill="x", pady=10)

label_title = tk.Label(frame_title, text="HOSPITAL MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), fg="blue")
label_title.pack()


frame_input = tk.Frame(root, padx=10, pady=10)                                      #adds input field
frame_input.pack(side="left", fill="both", expand=True, padx=20)

# Labels and Entry widgets for left frame
label_name = tk.Label(frame_input, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_name = tk.Entry(frame_input)
entry_name.grid(row=0, column=1, padx=10, pady=5)

label_age = tk.Label(frame_input, text="Age:")
label_age.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_age = tk.Entry(frame_input)
entry_age.grid(row=1, column=1, padx=10, pady=5)

label_gender = tk.Label(frame_input, text="Gender:")
label_gender.grid(row=2, column=0, padx=10, pady=5, sticky="w")
combo_gender = ttk.Combobox(frame_input, values=["Male", "Female", "Other"])
combo_gender.grid(row=2, column=1, padx=10, pady=5)

label_address = tk.Label(frame_input, text="Address:")
label_address.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_address = tk.Entry(frame_input)
entry_address.grid(row=3, column=1, padx=10, pady=5)

label_phone = tk.Label(frame_input, text="Phone:")
label_phone.grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_phone = tk.Entry(frame_input)
entry_phone.grid(row=4, column=1, padx=10, pady=5)


frame_buttons = tk.Frame(root)                                                       #Adds buttons
frame_buttons.pack(fill="x", pady=20)

btn_add = tk.Button(frame_buttons, text="Add Patient", command=add_patient)
btn_add.grid(row=0, column=0, padx=10)

btn_update = tk.Button(frame_buttons, text="Update Patient", command=update_patient)
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(frame_buttons, text="Delete Patient", command=delete_patient)
btn_delete.grid(row=0, column=2, padx=10)

btn_clear = tk.Button(frame_buttons, text="Clear Fields", command=clear_fields)
btn_clear.grid(row=0, column=3, padx=10)



treeview = ttk.Treeview(root, columns=("ID", "Name", "Age", "Gender", "Address", "Phone",), show="headings")   #displays treeview of patients details
treeview.pack(fill="both", padx=20, pady=20)

treeview.heading("ID", text="ID")
treeview.heading("Name", text="Name")
treeview.heading("Age", text="Age")
treeview.heading("Gender", text="Gender")
treeview.heading("Address", text="Address")
treeview.heading("Phone", text="Phone")


display_patients()
root.mainloop()
