import os

def dedent_file(file_path, spaces_to_remove=8):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    prefix = ' ' * spaces_to_remove
    for line in lines:
        if line.startswith(prefix):
            new_lines.append(line[spaces_to_remove:])
        else:
            new_lines.append(line)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Dedented: {file_path}")

def wrap_js_in_domcontentloaded(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "document.addEventListener('DOMContentLoaded'" not in content:
        # indent original content by 4 spaces
        indented_content = '\\n'.join('    ' + line if line.strip() else line for line in content.splitlines())
        wrapped_content = f"document.addEventListener('DOMContentLoaded', () => {{\\n{indented_content}\\n}});\\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(wrapped_content)
        print(f"Wrapped {file_path} in DOMContentLoaded")
    else:
        print(f"{file_path} already wrapped")

if __name__ == "__main__":
    css_path = os.path.join('css', 'style.css')
    js_path = os.path.join('js', 'main.js')

    # Dedent CSS
    dedent_file(css_path, spaces_to_remove=8)
    
    # Dedent JS
    dedent_file(js_path, spaces_to_remove=8)
    
    # Wrap JS
    wrap_js_in_domcontentloaded(js_path)
    print("Formatting complete! You can run python generate_en.py to synchronize.")
