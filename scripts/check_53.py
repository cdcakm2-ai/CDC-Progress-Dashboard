import re
from exact_counts import by_gn

# Let's inspect the 53 GN names
sheet_gns = sorted(list(by_gn.keys()))
print(f"53 GN names from sheets:")
for i, g in enumerate(sheet_gns, 1):
    print(f"  {i}. {g}")
