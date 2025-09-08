import sqlite3
import datetime
import csv
import os

DB_NAME = "expenses.db"

def init_db():
    """Initialize SQLite database with an expenses table."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_expense(amount, category):
    """Add a new expense to the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
              (amount, category, datetime.date.today().isoformat()))
    conn.commit()
    conn.close()
    print(f"[+] Added ${amount:.2f} under '{category}'")


def view_expenses():
    """View all expenses in the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, amount, category, date FROM expenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    print("\n--- All Expenses ---")
    for r in rows:
        print(f"#{r[0]} | ${r[1]:.2f} | {r[2]} | {r[3]}")
    print("--------------------\n")


def summary(period="month"):
    """Show summary of expenses by day/week/month."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    today = datetime.date.today()

    if period == "day":
        start_date = today
    elif period == "week":
        start_date = today - datetime.timedelta(days=today.weekday())
    else:  # month
        start_date = today.replace(day=1)

    c.execute("SELECT SUM(amount) FROM expenses WHERE date >= ?", (start_date.isoformat(),))
    total = c.fetchone()[0]
    conn.close()

    total = total if total else 0
    print(f"[Summary] Total {period}ly expenses since {start_date}: ${total:.2f}\n")


def export_csv(filename="expenses.csv"):
    """Export all expenses to a CSV file."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT amount, category, date FROM expenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Amount", "Category", "Date"])
        writer.writerows(rows)

    print(f"[+] Exported expenses to {os.path.abspath(filename)}")


def main():
    init_db()
    while True:
        print("Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Daily Summary")
        print("4. Weekly Summary")
        print("5. Monthly Summary")
        print("6. Export to CSV")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            try:
                amount = float(input("Enter amount: $"))
                category = input("Enter category: ")
                add_expense(amount, category)
            except ValueError:
                print("[!] Invalid input. Try again.")
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary("day")
        elif choice == "4":
            summary("week")
        elif choice == "5":
            summary("month")
        elif choice == "6":
            export_csv()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("[!] Invalid choice, try again.\n")


if __name__ == "__main__":
    main()
