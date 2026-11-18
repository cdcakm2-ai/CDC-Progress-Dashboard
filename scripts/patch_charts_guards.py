import re

def patch_charts():
    with open('js/charts.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Functions to guard
    func_names = [
        'renderAll',
        'renderMonthlyChart',
        'renderCategoryChart',
        'renderGNRankingChart',
        'renderAllAnalyticsCharts',
        'renderAnCumulativeChart',
        'renderAnMonthlyTrendChart',
        'renderAnTopDivisionsChart',
        'renderAnSectorCharts',
        'renderAnTimelineCharts',
        'renderAnDiversityChart',
        'renderAnCompareChart',
        'renderAnDeepdiveFinChart'
    ]

    for fn in func_names:
        # Match function definition
        pattern = rf'({fn}\s*\([^)]*\)\s*\{{)'
        replacement = r'\1\n    if (typeof Chart === "undefined") { console.warn("Chart.js not loaded. Skipping ' + fn + r'"); return; }'
        content = re.sub(pattern, replacement, content)

    with open('js/charts.js', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Patched js/charts.js with defensive Chart guards.")

if __name__ == '__main__':
    patch_charts()
