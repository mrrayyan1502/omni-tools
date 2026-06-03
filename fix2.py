import os

html_path = 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Split the HTML by tool-card div
parts = html.split('<div class="tool-card')
new_parts = [parts[0]]

for part in parts[1:]:
    # In each part (which starts right after '<div class="tool-card'), 
    # we want to replace the FIRST occurrence of <h3> and </h3> with <h2> and </h2>
    if '<h3>' in part:
        part = part.replace('<h3>', '<h2>', 1).replace('</h3>', '</h2>', 1)
    new_parts.append(part)

final_html = '<div class="tool-card'.join(new_parts)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(final_html)
print("Fixed H3 tags successfully.")
