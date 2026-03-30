import streamlit as st
import sqlite3
import pandas as pd
 
def get_connection():
    conn = sqlite3.connect("contacts.db")
    return conn
 
def create_table():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        category TEXT DEFAULT 'Personal'
    )
""")
    conn.commit()
    conn.close()
 
def add_contact(name,phone,email,category):
    conn= get_connection()
    conn.execute("INSERT INTO contacts (name,phone, email, category) VALUES (?,?,?,?)",(name,phone,email,category))
    conn.commit()
    conn.close()
 
def get_all_contacts():
    conn= get_connection()
    df = pd.read_sql_query("SELECT * FROM contacts ORDER BY name", conn)
    conn.close()
    return df
 
def search_contacts(search_term):
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?",
        conn,
        params=(f"%{search_term}%", f"%{search_term}%")
    )
    conn.close()
    return df
 
def delete_contact(contact_id):
    conn = get_connection()
    conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
 
 
create_table()
 
st.title("Contact Book")
st.sidebar.header("Add New Contact")
name = st.sidebar.text_input("Name")
phone = st.sidebar.text_input("Phone")
email = st.sidebar.text_input("Email")
category = st.sidebar.selectbox(
    "Category", ["Personal","Work","Family","Other"]
)
 
if st.sidebar.button("Add Contact"):
    if name and phone:
        add_contact(name,phone,email,category)
        st.sidebar.success(f"Added {name}!")
        st.rerun()
    else:
        st.sidebar.error("Name and Phone are required.")
 
 
 
search = st.text_input("Search contacts...")
if search:
    df = search_contacts(search)
else:
    df = get_all_contacts()
   
st.write(f"Showing {len(df)} contact(s)")
st.dataframe(df,use_container_width=True)
 
if not df.empty:
    st.subheader("Delete a Contact")
    contact_to_delete = st.selectbox(
        "Select contact to delete",
        df["id"].tolist(),
        format_func=lambda x: df[df["id"]== x]["name"].values[0]
    )
 
    if st.button("Delete Selected Contact"):
        delete_contact(contact_to_delete)
        st.success("Contact deleted!")
        st.rerun()
else:
    st.info("No contacts yet. Add one using sidebar!")