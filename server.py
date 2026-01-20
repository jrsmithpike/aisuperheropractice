from fastmcp import FastMCP
import sqlite3
import os

mcp = FastMCP("Superhero Server")

# Path to the database file.
DB_PATH = "database/superheroes.db"


# --- Database Helper Functions ---


def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Configures the connection to return rows that can be accessed by column name.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --- MCP Tools ---


@mcp.tool
def get_superheroes() -> list[dict]:
    """Returns info about all superheroes alphabetically."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # SQL query to select all columns for the superheroes in alpha order.
        cursor.execute("SELECT * FROM heroes ORDER BY superhero")
        rows = cursor.fetchall()

        # Convert each row into a python dictionary (object) to support a JSON result.
        list = [dict(row) for row in rows]
        return list

@mcp.tool
def get_superhero_info() -> list[dict]:
    """Returns specific requested info about a superhero."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

         # For each keyword, create a condition to search superhero.
        for keyword in keywords:
            conditions.append(
                f"(superhero LIKE '%{keyword}%')"
            )

        # Convert each row into a python dictionary (object) to support a JSON result.
        list = [dict(row) for row in rows]
        return list

@mcp.tool
def search_superheroes(keywords: list[str]) -> list[dict]:
    """Searches superhero based on alias."""
    if not keywords:
        return []

    with get_db_connection() as conn:
        cursor = conn.cursor()

        conditions = []

        # For each keyword, create a condition to search alias.
        for keyword in keywords:
            conditions.append(
                f"(alias LIKE '%{keyword}%')"
            )

        # Join all the individual conditions with "OR".
        # Example: "WHERE (alias LIKE ?) OR (alias LIKE ?)"
        query = "SELECT * FROM heroes WHERE " + " OR ".join(conditions)

        cursor.execute(query)
        rows = cursor.fetchall()
        # Convert each row into a python dictionary (object) to support a JSON result.
        list = [dict(row) for row in rows]
        return list


# --- Main Execution Block ---

if __name__ == "__main__":
    # This starts the FastMCP server, making the tools available over HTTP.
    mcp.run(transport="http", port=8000)
