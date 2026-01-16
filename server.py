from fastmcp import FastMCP
import sqlite3
import os

mcp = FastMCP("AI and Robotics News Server")

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
def get_latest_stories() -> list[dict]:
    """Returns info about 5 superheroes alphabetically."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # SQL query to select all columns for 5 superheroes in alpha order.
        cursor.execute("SELECT * FROM heroes ORDER BY superhero DESC LIMIT 5")
        rows = cursor.fetchall()

        # Convert each row into a python dictionary (object) to support a JSON result.
        list = [dict(row) for row in rows]
        return list


@mcp.tool
def search_stories(keywords: list[str]) -> list[dict]:
    """Searches title and description for an array of keywords."""
    if not keywords:
        return []

    with get_db_connection() as conn:
        cursor = conn.cursor()

        conditions = []

        # For each keyword, create a condition to search both title and description.
        for keyword in keywords:
            conditions.append(
                f"(title LIKE '%{keyword}%' OR description LIKE '%{keyword}%')"
            )

        # Join all the individual conditions with "OR".
        # Example: "WHERE (title LIKE ? OR description LIKE ?) OR (title LIKE ? OR description LIKE ?)"
        query = "SELECT * FROM news WHERE " + " OR ".join(conditions)

        cursor.execute(query)
        rows = cursor.fetchall()
        # Convert each row into a python dictionary (object) to support a JSON result.
        list = [dict(row) for row in rows]
        return list


# --- Main Execution Block ---

if __name__ == "__main__":
    # This starts the FastMCP server, making the tools available over HTTP.
    mcp.run(transport="http", port=8000)
