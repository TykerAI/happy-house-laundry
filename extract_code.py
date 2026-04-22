import re

with open('generate_en.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the translation dict keys to include loading="lazy" where flagcdn is used
content = content.replace('class="flag">', 'class="flag" loading="lazy">')
content = content.replace('border-radius:2px;">', 'border-radius:2px;" loading="lazy">')

with open('generate_en.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed dictionary matching strings.")