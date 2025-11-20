import sqlite3
import csv
import os


def create_database():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "ai_news.csv")
    db_path = os.path.join(base_dir, "ai_news.db")

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            release_date TEXT NOT NULL,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            link TEXT NOT NULL,
            tags TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """
    )

    # Read CSV and insert data
    try:
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            to_db = []
            for row in reader:
                to_db.append(
                    (
                        int(row["id"]),
                        row["release_date"],
                        row["title"],
                        row["source"],
                        row["link"],
                        row["tags"],
                        row["description"],
                    )
                )

        cursor.executemany(
            "INSERT OR REPLACE INTO news (id, release_date, title, source, link, tags, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            to_db,
        )
        conn.commit()
        print(f"Successfully created database at {db_path} with {len(to_db)} records.")
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
