import csv

with open('raw_drive_data/sheet1_form_responses_1.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = list(csv.reader(f))

# Let's inspect rows for 109/ ජී ඇටඹගස්මුල්ල
print("=== 109/ ජී ඇටඹගස්මුල්ල ===")
for r_idx in [9, 53]:
    row = reader[r_idx]
    print(f"\nRow {r_idx} | Timestamp: {row[0]} | Officer: {row[1]} | Claimed: {row[3]}")
    for b in range(8):
        d = row[4 + b*4].strip()
        desc = row[5 + b*4].strip()
        p = row[6 + b*4].strip()
        if d or desc:
            print(f"  Block {b+1}: Date: {d} | Desc: {desc[:60]} | HasPhoto: {bool(p)}")

# Let's inspect 155/ ඊ හියාරේ ඉහළ
print("\n=== 155/ ඊ හියාරේ ඉහළ ===")
for r_idx in [10, 58]:
    row = reader[r_idx]
    print(f"\nRow {r_idx} | Timestamp: {row[0]} | Officer: {row[1]} | Claimed: {row[3]}")
    for b in range(8):
        d = row[4 + b*4].strip()
        desc = row[5 + b*4].strip()
        p = row[6 + b*4].strip()
        if d or desc:
            print(f"  Block {b+1}: Date: {d} | Desc: {desc[:60]} | HasPhoto: {bool(p)}")

# Let's inspect 152 /බී තලහිටියාව
print("\n=== 152 /බී තලහිටියාව ===")
for r_idx in [24, 60, 62]:
    row = reader[r_idx]
    print(f"\nRow {r_idx} | Timestamp: {row[0]} | Officer: {row[1]} | Claimed: {row[3]}")
    for b in range(8):
        d = row[4 + b*4].strip()
        desc = row[5 + b*4].strip()
        p = row[6 + b*4].strip()
        if d or desc:
            print(f"  Block {b+1}: Date: {d} | Desc: {desc[:60]} | HasPhoto: {bool(p)}")
