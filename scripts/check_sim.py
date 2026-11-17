from difflib import SequenceMatcher

t1 = "අදිඅවදානම් පවුලක් වන වසන්ත ප්‍රේමලාල් මහතාට රජයේ ද මැදිහත් වීමෙන් නිවසක් සාදාදීම"
t2 = "අදිඅවදානම් පවුලක් වන ජානක තුශාර මහතාට නිවසක් සාදාදීම"
sim = SequenceMatcher(None, t1, t2).ratio()
print(f"Similarity between Vasantha and Janaka: {sim:.3f}")
