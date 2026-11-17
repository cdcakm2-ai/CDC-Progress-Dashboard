import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'<[^>]*id=["\']view-status["\'][^>]*>', text)
if match:
    print('Found tag:', match.group(0), 'at index', match.start())
    # find closing section
    end_tag = text.find('</section>', match.start())
    print('Closing tag at:', end_tag)
    print(text[match.start():match.start()+100])
