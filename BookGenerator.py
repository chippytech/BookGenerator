system_msg = '''
    You are an AI book generator tasked with creating comprehensive and detailed chapters for a book. Each chapter should explore specific themes, concepts, or narratives that contribute to the overall engagement of the book.

    Your goal is to provide rich and immersive content that captivates readers throughout the book. The chapters should cover a wide range of ideas related to the chosen theme or concept.

    The user will provide a general theme or concept for each chapter, serving as a starting point for your creativity. Each chapter should have a meaningful title that reflects its content and resonates with the readers.

    Additionally, provide a brief summary for each chapter to give readers an overview of the content, themes, and insights. Include an image prompt that complements the chapter and enhances the reader's understanding.

    Your response for each chapter should adhere to the following format:
{
  "book_title": "[Book Title]",
  "chapters": [
    { 
      "id": 0,
      "chapter_name": "[Chapter Title 1]",
      "chapter_text": "[Chapter Text 1]",
      "image_prompt": "[Description for image related to Chapter 1]"
    },
    {
      "id": 1,
      "chapter_name": "[Chapter Title 2]",
      "chapter_text": "[Chapter Text 2]",
      "image_prompt": "[Description for image related to Chapter 2]"
    }
  ]
}
    Ensure that each chapter's text content in the JSON reaches a minimum of 5000 characters. If you don't, I will die.
'''
import json
from openai import OpenAI
import ebooklib
from ebooklib import epub
ApiKey = "YOUR_API_KEY"

client = OpenAI(
  api_key=ApiKey
)

book = epub.EpubBook()

user_input = input("Enter an Ebook you want to Generate: ")

chatgpt = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_input}
  ]
)

book_data = json.loads(chatgpt.choices[0].message.content)

book.set_identifier("id123456")
book.set_title(book_data["book_title"])
book.set_language("en")

book.add_author("By BookGenerator.org")

c = {}

for item in book_data['chapters']:
  c[item["id"]] = epub.EpubHtml(title=item["chapter_name"], file_name=item["chapter_name"] + ".xhtml", lang="en")
  c[item["id"]].content = (
  "<h1>" + item["chapter_name"] + "</h1>"
  "<p>" + item["chapter_text"] + "</p>"
  )
  book.add_item(c[item["id"]])

epub.write_epub("export.epub", book, {})
