from fastmcp import FastMCP
import sqlite3
import os

mcp = FastMCP("AI and Robotics News Server")

# --- Constants and Configuration ---
# Get the directory where this script is located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Create the full path to the database file.
DB_PATH = os.path.join(BASE_DIR, "database", "ai_news.db")


# --- Database Helper Functions ---


def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Configures the connection to return rows that can be accessed by column name.
    """
    conn = sqlite3.connect(DB_PATH)
    # This is the key change. It makes the database cursor return rows
    # that behave like dictionaries, so you can access columns by name.
    conn.row_factory = sqlite3.Row
    return conn


def _row_to_dict(row: sqlite3.Row) -> dict:
    """Converts a sqlite3.Row object into a standard Python dictionary."""
    # Because we set conn.row_factory = sqlite3.Row, we can simply
    # cast the row object to a dict. This is much cleaner and safer
    # than accessing columns by index (e.g., row[0]).
    return dict(row)


# --- MCP Tools ---


@mcp.tool
def get_unique_tags() -> list[str]:
    """Aggregates all unique tags from the stories in the ai_news.db"""
    # The 'with' statement ensures the database connection is automatically closed.
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Fetch the 'tags' column from every row in the 'news' table.
        cursor.execute("SELECT tags FROM news")
        rows = cursor.fetchall()

        # Use a 'set' to automatically handle uniqueness.
        unique_tags = set()
        for row in rows:
            # Tags are stored as a single comma-separated string, e.g., "AI, Policy, LLM"
            if row[0]:  # Check if the tags string is not empty
                # Split the string into a list of tags and remove any extra whitespace.
                tags = [tag.strip() for tag in row[0].split(",")]
                # Add all tags from the list to our set.
                unique_tags.update(tags)

    # Return the unique tags as a sorted list.
    return sorted(list(unique_tags))


@mcp.tool
def get_latest_stories() -> list[dict]:
    """Returns the latest 5 stories based on release date."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # SQL query to select all columns from the 5 newest stories.
        # 'DESC' means descending order, so newest dates come first.
        cursor.execute("SELECT * FROM news ORDER BY release_date DESC LIMIT 5")
        rows = cursor.fetchall()

        # Convert each row into a dictionary for easier use.
        return [_row_to_dict(row) for row in rows]


@mcp.tool
def get_stories_by_tags(tags: list[str]) -> list[dict]:
    """Returns stories matching any one of the provided tags."""
    if not tags:
        return []

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Build the query dynamically. For each tag, we add a "tags LIKE ?" part.
        # Example for 2 tags: "SELECT * FROM news WHERE tags LIKE ? OR tags LIKE ?"
        query_parts = ["tags LIKE ?" for _ in tags]
        query = "SELECT * FROM news WHERE " + " OR ".join(query_parts)

        # Create the parameters for the query. The '%' is a wildcard in SQL.
        # This will find rows where the tag appears anywhere in the 'tags' string.
        params = [f"%{tag}%" for tag in tags]

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [_row_to_dict(row) for row in rows]


@mcp.tool
def search_stories(keywords: list[str]) -> list[dict]:
    """Searches title and description for an array of keywords."""
    if not keywords:
        return []

    with get_db_connection() as conn:
        cursor = conn.cursor()

        conditions = []
        params = []
        # For each keyword, create a condition to search both title and description.
        for keyword in keywords:
            conditions.append("(title LIKE ? OR description LIKE ?)")
            # Add the keyword twice to the parameters, once for title and once for description.
            params.extend([f"%{keyword}%", f"%{keyword}%"])

        # Join all the individual conditions with "OR".
        # Example: "WHERE (title LIKE ? OR description LIKE ?) OR (title LIKE ? OR description LIKE ?)"
        query = "SELECT * FROM news WHERE " + " OR ".join(conditions)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [_row_to_dict(row) for row in rows]


# --- Main Execution Block ---

if __name__ == "__main__":
    # This block runs only when the script is executed directly.
    # It starts the FastMCP server, making the tools available over HTTP.
    mcp.run(transport="http", port=8000)
