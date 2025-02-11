from fastapi import FastAPI, HTTPException
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from models.models import TicketCreate,TicketResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/ticket_system")

# Initialize FastAPI app
app = FastAPI()

# Database connection setup
try:
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connected successfully!")
except Exception as e:
    print("Database connection failed!")
    raise e


# Endpoint to create a new ticket
@app.post("/api/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):
    try:
        cursor.execute(
            """
            INSERT INTO tickets (title, description, status, created_at)
            VALUES (%s, %s, %s, %s) RETURNING *;
            """,
            (ticket.title, ticket.description, "open", datetime.now())
        )
        new_ticket = cursor.fetchone()
        conn.commit()
        return new_ticket
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating ticket: {str(e)}")

# Endpoint to get all tickets
@app.get("/api/tickets", response_model=List[TicketResponse])
def get_all_tickets():
    try:
        cursor.execute("SELECT * FROM tickets;")
        tickets = cursor.fetchall()
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tickets: {str(e)}")

# Endpoint to get a specific ticket by ID
@app.get("/api/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    try:
        cursor.execute("SELECT * FROM tickets WHERE id = %s;", (ticket_id,))
        ticket = cursor.fetchone()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ticket: {str(e)}")
