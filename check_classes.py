import re
from collections import Counter

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

bg_classes = re.findall(r'bg-[a-zA-Z]+-[0-9]+', text)
print(Counter(bg_classes).most_common(20))
