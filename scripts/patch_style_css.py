with open('css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('#FDE68A', '#3979D6')
text = text.replace('#D4AF37', '#3979D6')
text = text.replace('#030816', '#243B64')
text = text.replace('#78350F', '#1E40AF')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replaced all old gold and dark black tokens in style.css!")
