# Example for scripts/sheets_manager.py
import gspread
import os # For service account key path

def init_sheet():
    """Authenticates and returns the Google Sheet."""
    # Ensure your service account key file path is set as an environment variable
    # For GitHub Actions, you'd store the JSON content as a secret and write to file
    gc = gspread.service_account(filename=os.getenv("GOOGLE_SHEETS_KEY_PATH"))
    # Open your spreadsheet by name
    spreadsheet = gc.open("Elimuhub Content Calendar")
    return spreadsheet.worksheet("Content Log") # Assuming a sheet named "Content Log"

def log_content_status(title, status="Generated", url="", notes=""):
    """Logs or updates content status in Google Sheet."""
    worksheet = init_sheet()
    # Find next empty row or update existing row based on title
    # For simplicity, let's just append for now
    row = [title, status, url, notes, str(datetime.now())]
    worksheet.append_row(row)
    print(f"Logged content '{title}' to Google Sheet.")

# Example Usage (e.g., in publish_workflow.py after publishing):
# log_content_status(
#     "KCSE 2025 Revision Guide",
#     "Published",
#     "https://kibzgithub7407.github.io/edu-content-automation-kenya/blog/post-YYYY-MM-DD.html",
#     "Automatically generated blog post"
# )
