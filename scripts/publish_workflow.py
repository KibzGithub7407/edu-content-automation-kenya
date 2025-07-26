import os
from datetime import date
import shutil # For robust file operations

# Ensure the blog directory exists
os.makedirs("blog", exist_ok=True)

# 1. Move blog content to /blog/ and convert to HTML
# For robust Markdown to HTML conversion, you might use 'markdown' library
# pip install markdown
try:
    import markdown
    with open("content/blogs/blog1.md", "r") as f:
        blog_md_content = f.read()
    blog_html_content = markdown.markdown(blog_md_content)

    post_filename = f"post-{date.today().strftime('%Y-%m-%d')}.html"
    with open(f"blog/{post_filename}", "w") as f:
        # Basic HTML wrapper for the blog post
        f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elimuhub Blog - {date.today().strftime('%Y-%m-%d')}</title>
    <link rel="stylesheet" href="../styles.css"> </head>
<body>
    <div class="container">
        <h1>New Elimuhub Blog Post</h1>
        {blog_html_content}
        <p><a href="index.html">Back to Blog Home</a></p>
    </div>
</body>
</html>
        """)
    print(f"Blog post converted to HTML and moved to blog/{post_filename}")

    # Optionally, update an index.html for a list of posts
    # This requires more complex logic to append new posts to an existing index
    # For a simple approach, you can just link to the latest post from index.html
    with open("blog/index.html", "w") as f:
        f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elimuhub Education Blog</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="container">
        <h1>Elimuhub Education Blog</h1>
        <p>Welcome to our latest insights and tips for Kenyan education!</p>
        <p><a href="{post_filename}">Read our latest post: {date.today().strftime('%B %d, %Y')}</a></p>
        </div>
</body>
</html>
        """)
    print("blog/index.html updated with link to new post.")

except FileNotFoundError:
    print("Error: Blog content (blog1.md) not found for publishing.")
except ImportError:
    print("Markdown library not installed. Install with 'pip install markdown' for better HTML conversion.")
    # Fallback to simple text copy if markdown not installed
    try:
        with open("content/blogs/blog1.md", "r") as f_md:
            blog_raw_content = f_md.read()
        with open(f"blog/post-{date.today().strftime('%Y-%m-%d')}.html", "w") as f_html:
            f_html.write(f"<html><body><h1>New Blog</h1><pre>{blog_raw_content}</pre></body></html>")
        print("Blog content copied directly as pre-formatted text (no Markdown conversion).")
    except Exception as e:
        print(f"Failed to copy blog content: {e}")


# 2. Optional: Schedule social post using Buffer API
# Replace with your actual Buffer Access Token and Profile IDs
BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN")
BUFFER_PROFILE_IDS = os.getenv("BUFFER_PROFILE_IDS", "").split(',') # Comma-separated list

if BUFFER_ACCESS_TOKEN and BUFFER_PROFILE_IDS:
    import requests
    buffer_url = "https://api.bufferapp.com/1/updates/create.json"
    try:
        with open("content/captions/blog1-social.txt", "r") as f:
            social_caption_full = f.read()

        # Assuming the social_caption_full contains all three (FB, Twitter, IG)
        # You'd parse this more intelligently in a real app, e.g., using markers
        # For this example, we'll just use the full text for simplicity.
        text_to_post = social_caption_full.split("\n\n")[0] # Use the first paragraph/section

        data = {
            "text": text_to_post,
            "media[link]": "https://kibzgithub7407.github.io/edu-content-automation-kenya/blog/",
            "profile_ids[]": BUFFER_PROFILE_IDS,
            "access_token": BUFFER_ACCESS_TOKEN # For API requests
        }

        # Removed the 'auth' parameter as Buffer API usually uses access_token in data/URL
        res = requests.post(buffer_url, data=data)
        res.raise_for_status()
        print("Social post scheduled successfully via Buffer!")

    except FileNotFoundError:
        print("Social captions file (blog1-social.txt) not found. Skipping Buffer scheduling.")
    except requests.exceptions.RequestException as e:
        print(f"Error scheduling social post with Buffer: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during Buffer scheduling: {e}")
else:
    print("Buffer API keys or profile IDs not configured. Skipping social scheduling.")

