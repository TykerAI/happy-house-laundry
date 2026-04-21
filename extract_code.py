import os
import re

html_path = 'index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Extract CSS
style_match = re.search(r'<style>(.*?)</style>', html, flags=re.DOTALL)
if style_match:
    css_content = style_match.group(1).strip()
    os.makedirs('css', exist_ok=True)
    with open('css/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    # Replace the huge style block with standard link tags + Preconnects
    replacement = """
    <!-- Performance: Preconnect & Preload -->
    <link rel="preconnect" href="https://cdnjs.cloudflare.com">
    <link rel="preconnect" href="https://flagcdn.com">
    <link rel="stylesheet" href="./css/style.css">
"""
    html = html.replace(style_match.group(0), replacement.strip())

# 2. Extract JS (ignore ld+json)
script_match = re.search(r'<script>(.*?)</script>(?:\s+</body>)', html, flags=re.DOTALL)
if script_match:
    js_content = script_match.group(1).strip()
    os.makedirs('js', exist_ok=True)
    with open('js/main.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    html = html.replace(script_match.group(0), '<script src="./js/main.js" defer></script>')

# 3. Security & Loading Attributes
# Add noopener noreferrer to target="_blank"
html = re.sub(r'(target="_blank"(?![\s>]*rel=))', r'\1 rel="noopener noreferrer"', html)
# Make sure any existing rel gets appended, but it's complex, the above is enough since none currently have rel.

# Lazy loading images (exclude hero if we can, but we know hero uses fetchpriority="high" and doesn't load="lazy")
# Just add loading="lazy" to iframe
html = html.replace('<iframe src="', '<iframe loading="lazy" src="')
# Add loading="lazy" to standard img tags without loading=""
html = re.sub(r'(<img(?!.*loading=)[^>]*?)(/?>)', r'\1 loading="lazy"\2', html)

# 4. Save
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Extraction and optimization completed successfully.")
