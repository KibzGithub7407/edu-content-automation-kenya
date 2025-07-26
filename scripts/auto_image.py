# For illustration — direct Canva AI API not publicly available for direct generation.
# This script uses Pillow for basic image creation.
# For more advanced AI image generation, consider integrating with Stability AI's API (Stable Diffusion)
# or using a service like Hugging Face's inference API (check their free tier limits).

from PIL import Image, ImageDraw, ImageFont
import textwrap # For wrapping long text on the image
import os

def create_blog_cover_image(title, filename="blog1-cover.png"):
    """
    Creates a simple blog cover image with the given title.
    """
    img_width, img_height = 800, 400
    img = Image.new("RGB", (img_width, img_height), color=(255, 240, 230)) # Light, inviting background
    d = ImageDraw.Draw(img)

    # Try to load a font, fall back to default if not found
    try:
        # You might need to specify a full path to a .ttf file if not in system fonts
        font_path = "arial.ttf" # Or 'DejaVuSans-Bold.ttf' on Linux, etc.
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 40)
        else:
            font = ImageFont.load_default()
            print("Warning: arial.ttf not found, using default font.")
    except Exception as e:
        print(f"Error loading font: {e}. Using default font.")
        font = ImageFont.load_default()

    # Wrap text to fit within image
    wrapped_title = textwrap.wrap(title, width=25) # Adjust width as needed
    text_lines = "\n".join(wrapped_title)

    # Calculate text position to center it
    bbox = d.textbbox((0, 0), text_lines, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x_center = (img_width - text_width) / 2
    y_center = (img_height - text_height) / 2

    d.text((x_center, y_center), text_lines, fill=(50, 50, 50), font=font) # Dark grey text

    img.save(f"images/{filename}")
    print(f"Generated cover image saved to images/{filename}")

if __name__ == "__main__":
    # Example usage:
    # You might want to pull the actual blog title from the generated content
    try:
        with open("content/blogs/blog1.md", "r") as f:
            blog_content = f.read()
            # Extract the first line or a specific heading as the title
            title_line = blog_content.split('\n')[0].replace('#', '').strip()
            if title_line:
                create_blog_cover_image(title_line)
            else:
                create_blog_cover_image("Elimuhub Education Insights") # Fallback title
    except FileNotFoundError:
        print("Blog content not found. Generating a default image title.")
        create_blog_cover_image("Elimuhub Education Insights")
