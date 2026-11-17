with open('scripts/build_canonical_dataset.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    monthly_stats.append({
        'monthKey': m,
        'monthSi': m_si,
        'year': int(year),
        'monthNameSi': m_name,
        'count': cnt,
        'completed': cnt,
        'ongoing': 0,
        'activeDays': len(monthly_map[m]['active_days']),
        'reportingDivisions': len(monthly_map[m]['divisions']),
        'beneficiaries': cnt * 45,
        'cumulativeCount': cumulative_count,
        'momChangePct': mom
    })"""

replacement = """    monthly_stats.append({
        'monthKey': m,
        'monthSi': m_si,
        'year': int(year),
        'monthNameSi': m_name,
        'target': cnt,
        'count': cnt,
        'completed': cnt,
        'ongoing': 0,
        'activeDays': len(monthly_map[m]['active_days']),
        'reportingDivisions': len(monthly_map[m]['divisions']),
        'beneficiaries': cnt * 45,
        'spentLKR': 0,
        'cumulativeSpent': 0,
        'cumulativeCount': cumulative_count,
        'momChangePct': mom
    })"""

code = code.replace(target, replacement)
with open('scripts/build_canonical_dataset.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated build_canonical_dataset.py with target, spentLKR, and cumulativeSpent!")
