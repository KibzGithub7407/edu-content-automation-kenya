import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Assuming blog content exists, read a snippet for context
try:
    with open("content/blogs/blog1.md", "r") as f:
        blog_snippet = f.read(200) # Read first 200 chars for context
except FileNotFoundError:
    print("Error: Blog content not found. Run generate_content.py first.")
    exit()

caption_prompt = f"""
Based on this blog content snippet: "{blog_snippet}..."
Write a concise and engaging 3-line Facebook caption, a Twitter post (max 280 chars),
and an Instagram caption with 3 relevant hashtags, all for a Kenyan audience.
Focus on KCSE prep tips and invite engagement.
"""

try:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=caption_prompt,
        max_tokens=200, # Sufficient for all three captions
        temperature=0.7
    )

    social_text = response.choices[0].text.strip()
    with open("content/captions/blog1-social.txt", "w") as f:
        f.write(social_text)
    print("Generated social media snippets saved to content/captions/blog1-social.txt")

except openai.error.OpenAIError as e:
    print(f"Error generating social snippets with OpenAI: {e}")
