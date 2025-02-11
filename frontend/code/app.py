import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

# Streamlit UI setup
st.set_page_config(
    page_title="Customer Support Ticket System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Create Ticket", "View Tickets", "Check Ticket Status"])

# Function to create a new ticket
def create_ticket():
    st.title("Create a New Support Ticket")
    with st.form("ticket_form"):
        title = st.text_input("Issue Title", placeholder="Enter a brief title for your issue")
        description = st.text_area("Problem Description", placeholder="Describe your problem in detail")
        submitted = st.form_submit_button("Submit Ticket")
        
        if submitted:
            if not title or not description:
                st.error("Both Title and Description are required!")
            else:
                # Send data to FastAPI backend
                response = requests.post(
                    f"{FASTAPI_URL}/api/tickets",
                    json={"title": title, "description": description}
                )
                if response.status_code == 200:
                    ticket_id = response.json().get("ticket_id")
                    st.success(f"Ticket created successfully! Your Ticket ID: {ticket_id}")
                else:
                    st.error(f"Failed to create ticket: {response.text}")

# Function to view all tickets
def view_tickets():
    st.title("View All Tickets")
    response = requests.get(f"{FASTAPI_URL}/api/tickets")
    
    if response.status_code == 200:
        tickets = response.json()
        if tickets:
            for ticket in tickets:
                with st.expander(f"Ticket #{ticket['id']} - {ticket['title']}"):
                    st.write(f"**Description:** {ticket['description']}")
                    st.write(f"**Status:** {ticket['status']}")
                    st.write(f"**Created At:** {ticket['created_at']}")
        else:
            st.info("No tickets found.")
    else:
        st.error(f"Failed to fetch tickets: {response.text}")

# Function to check the status of a specific ticket
def check_ticket_status():
    st.title("Check Ticket Status")
    ticket_id = st.text_input("Enter Ticket ID", placeholder="e.g., 12345")
    
    if st.button("Check Status"):
        if not ticket_id:
            st.error("Please enter a valid Ticket ID.")
        else:
            response = requests.get(f"{FASTAPI_URL}/api/tickets/{ticket_id}")
            if response.status_code == 200:
                ticket = response.json()
                st.write(f"**Title:** {ticket['title']}")
                st.write(f"**Description:** {ticket['description']}")
                st.write(f"**Status:** {ticket['status']}")
                st.write(f"**Created At:** {ticket['created_at']}")
            else:
                st.error(f"Failed to fetch ticket status: {response.text}")

# Routing based on sidebar navigation
if menu == "Create Ticket":
    create_ticket()
elif menu == "View Tickets":
    view_tickets()
elif menu == "Check Ticket Status":
    check_ticket_status()
