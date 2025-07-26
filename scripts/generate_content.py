import openai, json
import os # For securely getting API key from environment variables

# Ensure your OpenAI API key is set as an environment variable or in a secrets.py file
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

try:
    data = json.load(open("data/keyword_trends.json"))
except FileNotFoundError:
    print("Error: data/keyword_trends.json not found. Run fetch_keywords.py first.")
    exit()

# Refine the prompt for specific Kenyan education content
keyword_string = ', '.join(data[:5]) # Use top 5 keywords for focus
prompt = f"""
Write a comprehensive, 500-word SEO-optimized blog post for Kenyan parents and students.
The topic should primarily focus on: {keyword_string}.

Ensure the content is:
- **Highly relevant** to the Kenyan education system (e.g., mention specific exams like KCPE/KCSE, local school terms).
- **Informative and helpful**, offering practical advice or insights.
- **Engaging** and easy to understand.
- **Optimized for SEO** with natural keyword integration.
- Include a call to action related to Elimuhub's services (e.g., tutoring, consultation).
"""

try:
    response = openai.Completion.create(
        engine="text-davinci-003", # Or 'gpt-3.5-turbo' with chat completion API
        prompt=prompt,
        max_tokens=1000, # Allows for a longer, more detailed response
        temperature=0.7 # Adjust for creativity (higher = more creative)
    )

    blog_content = response.choices[0].text.strip()
    blog_filename = "blog1.md" # Consider dynamic naming for multiple blogs
    with open(f"content/blogs/{blog_filename}", "w") as f:
        f.write(blog_content)
    print(f"Generated blog post saved to content/blogs/{blog_filename}")

except openai.error.OpenAIError as e:
    print(f"Error generating content with OpenAI: {e}")
