import markdown

with open('wiki.md', 'r') as file:
    markdown_content = file.read()

html_content = markdown.markdown(markdown_content)

with open('templates/wiki_render.html', 'w') as file:
    file.write(html_content)