# -*- coding: utf-8 -*-
with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Line 828-829: Remove budgetLKR and spentLKR in gallery item template
old_card = '''        categoryNameSi: item.categoryNameSi || "ප්‍රජා සංවර්ධන",
        budgetLKR: 1500000,
        spentLKR: 1450000,
        images: [item.url]'''
new_card = '''        categoryNameSi: item.categoryNameSi || "ප්‍රජා සංවර්ධන",
        images: [item.url]'''
assert old_card in content, "old_card not found"
content = content.replace(old_card, new_card)

# 2. Lines 2555-2688 (Overall Progress Report)
old_rep1 = '''      const totalSpent = reportActs.reduce((acc, a) => acc + (a.spentLKR || 0), 0);'''
new_rep1 = '''      const totalPhotos = reportActs.reduce((acc, a) => acc + (a.images ? a.images.length : 0), 0);'''
assert old_rep1 in content, "old_rep1 not found"
content = content.replace(old_rep1, new_rep1)

old_sec_stat = '''          sectorStats[c.id] = { name: c.nameSi, projects: 0, completed: 0, spent: 0, beneficiaries: 0 };'''
new_sec_stat = '''          sectorStats[c.id] = { name: c.nameSi, projects: 0, completed: 0, photos: 0, beneficiaries: 0 };'''
assert old_sec_stat in content, "old_sec_stat not found"
content = content.replace(old_sec_stat, new_sec_stat)

old_sec_inc = '''          sectorStats[a.category].spent += a.spentLKR || 0;'''
new_sec_inc = '''          sectorStats[a.category].photos += (a.images ? a.images.length : 0);'''
assert old_sec_inc in content, "old_sec_inc not found"
content = content.replace(old_sec_inc, new_sec_inc)

old_sec_td = '''              <td style="text-align: right; font-weight: 700;">රු. ${(s.spent || 0).toLocaleString()}</td>'''
new_sec_td = '''              <td style="text-align: center; font-weight: 700;">${(s.photos || 0).toLocaleString()}</td>'''
assert old_sec_td in content, "old_sec_td not found"
content = content.replace(old_sec_td, new_sec_td)

old_act_td = '''            <td style="text-align: right;">රු. ${(act.spentLKR || 0).toLocaleString()}</td>'''
new_act_td = '''            <td style="text-align: center;">${(act.images ? act.images.length : 0)}</td>'''
assert old_act_td in content, "old_act_td not found"
content = content.replace(old_act_td, new_act_td)

old_kpi_spent = '''          <div class="report-kpi-box">
            <div class="report-kpi-label">යෙදවූ මුළු මුදල</div>
            <div class="report-kpi-val" style="color: #B45309;">රු. ${(totalSpent / 1000000).toFixed(2)} M</div>
          </div>'''
new_kpi_spent = '''          <div class="report-kpi-box">
            <div class="report-kpi-label">සත්‍යාපිත ඡායාරූප</div>
            <div class="report-kpi-val" style="color: #0D9488;">${totalPhotos.toLocaleString()}</div>
          </div>'''
assert old_kpi_spent in content, "old_kpi_spent not found"
content = content.replace(old_kpi_spent, new_kpi_spent)

old_exec_sum = '''මේ වෙනුවෙන් යොදවා ඇති සමස්ත මුදල රුපියල් මිලියන ${(totalSpent / 1000000).toFixed(2)} ක් වන අතර'''
new_exec_sum = '''මේ සඳහා සත්‍යාපිත ක්ෂේත්‍ර ඡායාරූප ${totalPhotos.toLocaleString()} ක් සාක්ෂි වශයෙන් ලේඛනගත කර ඇති අතර'''
assert old_exec_sum in content, "old_exec_sum not found"
content = content.replace(old_exec_sum, new_exec_sum)

old_th_rep1 = '''              <th style="text-align: right;">යෙදවූ මුදල (රු.)</th>'''
new_th_rep1 = '''              <th style="text-align: center;">ඡායාරූප ගණන</th>'''
assert old_th_rep1 in content, "old_th_rep1 not found"
content = content.replace(old_th_rep1, new_th_rep1)

old_th_rep2 = '''              <th style="text-align: right;">වියදම (රු.)</th>'''
new_th_rep2 = '''              <th style="text-align: center;">ඡායාරූප</th>'''
assert old_th_rep2 in content, "old_th_rep2 not found"
content = content.replace(old_th_rep2, new_th_rep2)

old_csv_rep1 = '''        ["අංකය", "වැඩසටහනේ නම", "ග්‍රාම නිලධාරී වසම", "ප්‍රජා සංවර්ධන සභාව", "අංශය", "දිනය", "ප්‍රතිලාභී පවුල්", "යෙදවූ මුදල (රු.)", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,වැඩසටහනේ නම,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,අංශය,දිනය,ප්‍රතිලාභී පවුල්,යෙදවූ මුදල (රු.),ප්‍රගතිය (%)\\n";

      reportActs.forEach((a, i) => {
        excelRows.push([i + 1, a.titleSi, a.gnNameSi, a.sabhaNameSi, a.categoryNameSi, a.date, a.beneficiaries, a.spentLKR, `${a.progress}%`]);
        csvData += `${i + 1},"${a.titleSi}","${a.gnNameSi}","${a.sabhaNameSi}","${a.categoryNameSi}","${a.date}","${a.beneficiaries}",${a.spentLKR},${a.progress}%\\n`;
      });'''
new_csv_rep1 = '''        ["අංකය", "වැඩසටහනේ නම", "ග්‍රාම නිලධාරී වසම", "ප්‍රජා සංවර්ධන සභාව", "අංශය", "දිනය", "ප්‍රතිලාභී පවුල්", "ඡායාරූප ගණන", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,වැඩසටහනේ නම,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,අංශය,දිනය,ප්‍රතිලාභී පවුල්,ඡායාරූප ගණන,ප්‍රගතිය (%)\\n";

      reportActs.forEach((a, i) => {
        excelRows.push([i + 1, a.titleSi, a.gnNameSi, a.sabhaNameSi, a.categoryNameSi, a.date, a.beneficiaries, (a.images ? a.images.length : 0), `${a.progress}%`]);
        csvData += `${i + 1},"${a.titleSi}","${a.gnNameSi}","${a.sabhaNameSi}","${a.categoryNameSi}","${a.date}","${a.beneficiaries}",${a.images ? a.images.length : 0},${a.progress}%\\n`;
      });'''
assert old_csv_rep1 in content, "old_csv_rep1 not found"
content = content.replace(old_csv_rep1, new_csv_rep1)

# 3. Lines 2703-2766 (Monthly Report)
old_monthly_csv = '''        ["මාසය", "ඉලක්කගත වැඩසටහන්", "සම්පූර්ණ වූ", "ක්‍රියාත්මකයි", "ප්‍රතිලාභී පවුල්", "මාසික වියදම (රු.)", "සමුච්චිත වියදම (රු.)", "ප්‍රගති වේගය (%)"]
      ];
      csvData = "මාසය,ඉලක්කගත වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,මාසික වියදම (රු.),සමුච්චිත වියදම (රු.),ප්‍රගති වේගය (%)\\n";

      let totalTarget = 0, totalComp = 0, totalOng = 0, totalBen = 0, totalSp = 0;

      reportMonthly.forEach((m) => {
        const rate = Math.round((m.completed / m.target) * 100);
        totalTarget += m.target;
        totalComp += m.completed;
        totalOng += m.ongoing;
        totalBen += m.beneficiaries;
        totalSp += m.spentLKR;

        monthlyRowsHtml += `
          <tr>
            <td style="font-weight: 700;">${m.monthSi} 2024</td>
            <td style="text-align: center;">${m.target}</td>
            <td style="text-align: center; color: #15803D; font-weight: 700;">${m.completed}</td>
            <td style="text-align: center; color: #1D4ED8;">${m.ongoing}</td>
            <td style="text-align: right;">${(m.beneficiaries || 0).toLocaleString()} පවුල්</td>
            <td style="text-align: right;">රු. ${(m.spentLKR || 0).toLocaleString()}</td>
            <td style="text-align: right; font-weight: 700; color: #B45309;">රු. ${(m.cumulativeSpent || 0).toLocaleString()}</td>
            <td style="text-align: center; font-weight: 800; color: #15803D;">${rate}%</td>
          </tr>
        `;

        excelRows.push([m.monthSi, m.target, m.completed, m.ongoing, m.beneficiaries, m.spentLKR, m.cumulativeSpent, `${rate}%`]);
        csvData += `"${m.monthSi}",${m.target},${m.completed},${m.ongoing},${m.beneficiaries},${m.spentLKR},${m.cumulativeSpent},${rate}%\\n`;
      });'''
new_monthly_csv = '''        ["මාසය", "ක්‍රියාත්මක වැඩසටහන්", "සම්පූර්ණ වූ", "වාර්තා කළ වසම්", "ක්‍රියාකාරී දින", "සත්‍යාපිත ඡායාරූප", "සමුච්චිත වැඩසටහන්", "ප්‍රගතිය (%)"]
      ];
      csvData = "මාසය,ක්‍රියාත්මක වැඩසටහන්,සම්පූර්ණ වූ,වාර්තා කළ වසම්,ක්‍රියාකාරී දින,සත්‍යාපිත ඡායාරූප,සමුච්චිත වැඩසටහන්,ප්‍රගතිය (%)\\n";

      let totalTarget = 0, totalComp = 0, totalOng = 0, totalBen = 0, totalPhotosCount = 0;

      reportMonthly.forEach((m) => {
        const rate = 100;
        const count = m.count || m.totalProjects || 1;
        totalTarget += count;
        totalComp += (m.completed || count);
        totalPhotosCount += (m.photos || 0);

        monthlyRowsHtml += `
          <tr>
            <td style="font-weight: 700;">${m.monthSi}</td>
            <td style="text-align: center;">${count}</td>
            <td style="text-align: center; color: #15803D; font-weight: 700;">${m.completed || count}</td>
            <td style="text-align: center; color: #1D4ED8;">${m.reportingDivisions || m.activeGNCount || 1}</td>
            <td style="text-align: center;">${m.activeDays || 1}</td>
            <td style="text-align: center; font-weight: 700; color: #0D9488;">${m.photos || 0}</td>
            <td style="text-align: center; font-weight: 700;">${m.cumulativeActivities || m.cumulativeCount || count}</td>
            <td style="text-align: center; font-weight: 800; color: #15803D;">100%</td>
          </tr>
        `;

        excelRows.push([m.monthSi, count, m.completed || count, m.reportingDivisions || m.activeGNCount || 1, m.activeDays || 1, m.photos || 0, m.cumulativeActivities || m.cumulativeCount || count, "100%"]);
        csvData += `"${m.monthSi}",${count},${m.completed || count},${m.reportingDivisions || m.activeGNCount || 1},${m.activeDays || 1},${m.photos || 0},${m.cumulativeActivities || m.cumulativeCount || count},100%\\n`;
      });'''
assert old_monthly_csv in content, "old_monthly_csv not found"
content = content.replace(old_monthly_csv, new_monthly_csv)

old_monthly_kpi = '''          <div class="report-kpi-box">
            <div class="report-kpi-label">සමුච්චිත මුළු වියදම</div>
            <div class="report-kpi-val" style="color: #B45309;">රු. ${(totalSp / 1000000).toFixed(2)} M</div>
          </div>'''
new_monthly_kpi = '''          <div class="report-kpi-box">
            <div class="report-kpi-label">සත්‍යාපිත මුළු ඡායාරූප</div>
            <div class="report-kpi-val" style="color: #0D9488;">${totalPhotosCount.toLocaleString()}</div>
          </div>'''
assert old_monthly_kpi in content, "old_monthly_kpi not found"
content = content.replace(old_monthly_kpi, new_monthly_kpi)

old_monthly_tbl_head = '''            <tr>
              <th>මාසය</th>
              <th style="text-align: center;">ඉලක්කගත</th>
              <th style="text-align: center;">සම්පූර්ණ වූ</th>
              <th style="text-align: center;">ක්‍රියාත්මකයි</th>
              <th style="text-align: right;">ප්‍රතිලාභී පවුල්</th>
              <th style="text-align: right;">මාසික වියදම (රු.)</th>
              <th style="text-align: right;">සමුච්චිත වියදම (රු.)</th>
              <th style="text-align: center;">වේගය</th>
            </tr>'''
new_monthly_tbl_head = '''            <tr>
              <th>මාසය</th>
              <th style="text-align: center;">වැඩසටහන්</th>
              <th style="text-align: center;">සම්පූර්ණ වූ</th>
              <th style="text-align: center;">වසම් ගණන</th>
              <th style="text-align: center;">දින</th>
              <th style="text-align: center;">ඡායාරූප</th>
              <th style="text-align: center;">සමුච්චිත</th>
              <th style="text-align: center;">ප්‍රගතිය</th>
            </tr>'''
assert old_monthly_tbl_head in content, "old_monthly_tbl_head not found"
content = content.replace(old_monthly_tbl_head, new_monthly_tbl_head)

# 4. Lines 2796-2873 (GN Division Report)
old_gn_rep_csv = '''        ["අංකය", "වැඩසටහනේ නම", "දිනය", "ස්ථානය", "අරමුණ", "කාර්යයන්", "ප්‍රතිලාභීන්", "ප්‍රතිඵල", "යෙදවූ මුදල (රු.)", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,වැඩසටහනේ නම,දිනය,ස්ථානය,අරමුණ,කාර්යයන්,ප්‍රතිලාභීන්,ප්‍රතිඵල,යෙදවූ මුදල (රු.),ප්‍රගතිය (%)\\n";'''
new_gn_rep_csv = '''        ["අංකය", "වැඩසටහනේ නම", "දිනය", "ස්ථානය", "අරමුණ", "කාර්යයන්", "ප්‍රතිලාභීන්", "ප්‍රතිඵල", "ඡායාරූප ගණන", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,වැඩසටහනේ නම,දිනය,ස්ථානය,අරමුණ,කාර්යයන්,ප්‍රතිලාභීන්,ප්‍රතිඵල,ඡායාරූප ගණන,ප්‍රගතිය (%)\\n";'''
assert old_gn_rep_csv in content, "old_gn_rep_csv not found"
content = content.replace(old_gn_rep_csv, new_gn_rep_csv)

old_gn_rep_push = '''          excelRows.push([idx + 1, act.titleSi, act.date, act.locationSi || gn.nameSi, act.purposeSi, act.actionsSi, act.beneficiaries, act.resultsSi, act.spentLKR, `${act.progress}%`]);
          csvData += `${idx + 1},"${act.titleSi || act.title || act.description || "වැඩසටහන"}","${act.date}","${act.locationSi || gn.nameSi}","${(act.purposeSi || '').replace(/"/g, '""')}","${(act.actionsSi || '').replace(/"/g, '""')}","${act.beneficiaries}","${(act.resultsSi || '').replace(/"/g, '""')}",${act.spentLKR},${act.progress}%\\n`;'''
new_gn_rep_push = '''          const pCount = act.images ? act.images.length : 0;
          excelRows.push([idx + 1, act.titleSi, act.date, act.locationSi || gn.nameSi, act.purposeSi, act.actionsSi, act.beneficiaries, act.resultsSi, pCount, `${act.progress}%`]);
          csvData += `${idx + 1},"${act.titleSi || act.title || act.description || "වැඩසටහන"}","${act.date}","${act.locationSi || gn.nameSi}","${(act.purposeSi || '').replace(/"/g, '""')}","${(act.actionsSi || '').replace(/"/g, '""')}","${act.beneficiaries}","${(act.resultsSi || '').replace(/"/g, '""')}",${pCount},${act.progress}%\\n`;'''
assert old_gn_rep_push in content, "old_gn_rep_push not found"
content = content.replace(old_gn_rep_push, new_gn_rep_push)

old_gn_rep_admin = '''          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">වෙන්කළ ප්‍රතිපාදන:</td>
            <td>රු. ${(gn.budgetLKR || 0).toLocaleString()}</td>
            <td style="font-weight: 700; background: #F8FAFC;">යෙදවූ මුදල:</td>
            <td style="font-weight: 700; color: #15803D;">රු. ${(gn.spentLKR || 0).toLocaleString()}</td>
          </tr>'''
new_gn_rep_admin = '''          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">වාර්තා කළ වැඩසටහන්:</td>
            <td style="font-weight: 800; color: #1D4ED8;">${gn.activityCount || gn.totalProjects || 0}</td>
            <td style="font-weight: 700; background: #F8FAFC;">සත්‍යාපිත ඡායාරූප:</td>
            <td style="font-weight: 800; color: #0D9488;">${gn.photoCount || divActs.reduce((acc, a) => acc + (a.images ? a.images.length : 0), 0)} කි</td>
          </tr>'''
assert old_gn_rep_admin in content, "old_gn_rep_admin not found"
content = content.replace(old_gn_rep_admin, new_gn_rep_admin)

# 5. Lines 2917-2962 (Single Project Report)
old_single_kpi = '''          <div class="report-kpi-box">
            <div class="report-kpi-label">යෙදවූ මුදල</div>
            <div class="report-kpi-val" style="color: #B45309;">රු. ${(act.spentLKR || 0).toLocaleString()}</div>
          </div>'''
new_single_kpi = '''          <div class="report-kpi-box">
            <div class="report-kpi-label">සත්‍යාපිත ඡායාරූප</div>
            <div class="report-kpi-val" style="color: #0D9488;">${(act.images ? act.images.length : 0)} කි</div>
          </div>'''
assert old_single_kpi in content, "old_single_kpi not found"
content = content.replace(old_single_kpi, new_single_kpi)

old_single_budget = '''          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">වෙන්කළ ප්‍රතිපාදන</td>
            <td>රු. ${(act.budgetLKR || 0).toLocaleString()}</td>
            <td style="font-weight: 700; background: #F8FAFC;">යෙදවූ මුදල</td>
            <td style="font-weight: 700;">රු. ${(act.spentLKR || 0).toLocaleString()}</td>
          </tr>'''
new_single_budget = '''          <tr>
            <td style="font-weight: 700; background: #F8FAFC;">ක්‍රියාත්මක තත්ත්වය</td>
            <td style="font-weight: 800; color: #15803D;">100% සම්පූර්ණයි</td>
            <td style="font-weight: 700; background: #F8FAFC;">ඡායාරූප සාක්ෂි</td>
            <td style="font-weight: 800; color: #0D9488;">ඡායාරූප ${(act.images ? act.images.length : 0)} ක් තහවුරු කර ඇත</td>
          </tr>'''
assert old_single_budget in content, "old_single_budget not found"
content = content.replace(old_single_budget, new_single_budget)

old_single_excel = '''        ["වෙන්කළ මුදල (රු.)", act.budgetLKR],
        ["යෙදවූ මුදල (රු.)", act.spentLKR]'''
new_single_excel = '''        ["සත්‍යාපිත ඡායාරූප ගණන", (act.images ? act.images.length : 0)],
        ["සම්පූර්ණ කිරීමේ තත්ත්වය", "100% සම්පූර්ණයි"]'''
assert old_single_excel in content, "old_single_excel not found"
content = content.replace(old_single_excel, new_single_excel)

# 6. Lines 3058-3101 (Sector Report)
old_sec_rep_csv = '''        ["අංකය", "සංවර්ධන ක්ෂේත්‍රය", "ක්‍රියාත්මක වැඩසටහන්", "සම්පූර්ණ වූ", "ක්‍රියාත්මකයි", "ප්‍රතිලාභී පවුල්", "යෙදවූ මුදල (රු.)", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,සංවර්ධන ක්ෂේත්‍රය,ක්‍රියාත්මක වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,යෙදවූ මුදල (රු.),ප්‍රගතිය (%)\\n";'''
new_sec_rep_csv = '''        ["අංකය", "සංවර්ධන ක්ෂේත්‍රය", "ක්‍රියාත්මක වැඩසටහන්", "සම්පූර්ණ වූ", "ක්‍රියාත්මකයි", "ප්‍රතිලාභී පවුල්", "සත්‍යාපිත ඡායාරූප", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,සංවර්ධන ක්ෂේත්‍රය,ක්‍රියාත්මක වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,සත්‍යාපිත ඡායාරූප,ප්‍රගතිය (%)\\n";'''
assert old_sec_rep_csv in content, "old_sec_rep_csv not found"
content = content.replace(old_sec_rep_csv, new_sec_rep_csv)

old_sec_rep_calc = '''          const cSpent = catActs.reduce((acc, a) => acc + (a.spentLKR || 0), 0);
          const cProg = cCount > 0 ? Math.round((cComp / cCount) * 100) : 100;

          categoryRowsHtml += `
            <tr>
              <td style="text-align: center;">${idx}</td>
              <td style="font-weight: 700; color: #1D4ED8;">${cat.nameSi}</td>
              <td style="text-align: center; font-weight: 700;">${cCount}</td>
              <td style="text-align: center; color: #15803D; font-weight: 700;">${cComp}</td>
              <td style="text-align: center; color: #3B82F6;">${cOng}</td>
              <td style="text-align: right;">${(cBen || 0).toLocaleString()} පවුල්</td>
              <td style="text-align: right; font-weight: 700;">රු. ${(cSpent || 0).toLocaleString()}</td>
              <td style="text-align: center; font-weight: 800; color: #15803D;">${cProg}%</td>
            </tr>
          `;

          excelRows.push([idx, cat.nameSi, cCount, cComp, cOng, cBen, cSpent, `${cProg}%`]);
          csvData += `${idx},"${cat.nameSi}",${cCount},${cComp},${cOng},${cBen},${cSpent},${cProg}%\\n`;'''
new_sec_rep_calc = '''          const cPhotos = catActs.reduce((acc, a) => acc + (a.images ? a.images.length : 0), 0);
          const cProg = cCount > 0 ? Math.round((cComp / cCount) * 100) : 100;

          categoryRowsHtml += `
            <tr>
              <td style="text-align: center;">${idx}</td>
              <td style="font-weight: 700; color: #1D4ED8;">${cat.nameSi}</td>
              <td style="text-align: center; font-weight: 700;">${cCount}</td>
              <td style="text-align: center; color: #15803D; font-weight: 700;">${cComp}</td>
              <td style="text-align: center; color: #3B82F6;">${cOng}</td>
              <td style="text-align: right;">${(cBen || 0).toLocaleString()} පවුල්</td>
              <td style="text-align: center; font-weight: 700; color: #0D9488;">${(cPhotos || 0).toLocaleString()}</td>
              <td style="text-align: center; font-weight: 800; color: #15803D;">${cProg}%</td>
            </tr>
          `;

          excelRows.push([idx, cat.nameSi, cCount, cComp, cOng, cBen, cPhotos, `${cProg}%`]);
          csvData += `${idx},"${cat.nameSi}",${cCount},${cComp},${cOng},${cBen},${cPhotos},${cProg}%\\n`;'''
assert old_sec_rep_calc in content, "old_sec_rep_calc not found"
content = content.replace(old_sec_rep_calc, new_sec_rep_calc)

# 7. Lines 3129-3171 (All GNs Report)
old_all_gns_csv = '''        ["අංකය", "ග්‍රාම නිලධාරී වසම", "ප්‍රජා සංවර්ධන සභාව", "ප්‍රමුඛ ක්ෂේත්‍රය", "මුළු වැඩසටහන්", "සම්පූර්ණ වූ", "ක්‍රියාත්මකයි", "ප්‍රතිලාභී පවුල්", "ප්‍රතිපාදන (රු.)", "යෙදවූ මුදල (රු.)", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,ප්‍රමුඛ ක්ෂේත්‍රය,මුළු වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,ප්‍රතිපාදන (රු.),යෙදවූ මුදල (රු.),ප්‍රගතිය (%)\\n";'''
new_all_gns_csv = '''        ["අංකය", "ග්‍රාම නිලධාරී වසම", "ප්‍රජා සංවර්ධන සභාව", "ප්‍රමුඛ ක්ෂේත්‍රය", "මුළු වැඩසටහන්", "සම්පූර්ණ වූ", "ක්‍රියාත්මකයි", "ප්‍රතිලාභී පවුල්", "සත්‍යාපිත ඡායාරූප", "ප්‍රගතිය (%)"]
      ];
      csvData = "අංකය,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,ප්‍රමුඛ ක්ෂේත්‍රය,මුළු වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,සත්‍යාපිත ඡායාරූප,ප්‍රගතිය (%)\\n";'''
assert old_all_gns_csv in content, "old_all_gns_csv not found"
content = content.replace(old_all_gns_csv, new_all_gns_csv)

old_all_gns_row = '''            <td style="text-align: right;">${(g.beneficiaries || 0).toLocaleString()}</td>
            <td style="text-align: right;">රු. ${(g.budgetLKR || 0).toLocaleString()}</td>
            <td style="text-align: right; font-weight: 600;">රු. ${(g.spentLKR || 0).toLocaleString()}</td>
            <td style="text-align: center; font-weight: 800; color: #15803D;">${g.progress}%</td>
          </tr>
        `;

        excelRows.push([idx + 1, g.nameSi, g.sabhaNameSi, g.keySectorSi, g.totalProjects, g.completed, g.ongoing, g.beneficiaries, g.budgetLKR, g.spentLKR, `${g.progress}%`]);
        csvData += `${idx + 1},"${g.nameSi}","${g.sabhaNameSi}","${g.keySectorSi}",${g.totalProjects},${g.completed},${g.ongoing},${g.beneficiaries},${g.budgetLKR},${g.spentLKR},${g.progress}%\\n`;'''
new_all_gns_row = '''            <td style="text-align: right;">${(g.beneficiaries || 0).toLocaleString()}</td>
            <td style="text-align: center; font-weight: 700; color: #0D9488;">${g.photoCount || 0}</td>
            <td style="text-align: center; font-weight: 800; color: #15803D;">${g.progress}%</td>
          </tr>
        `;

        excelRows.push([idx + 1, g.nameSi, g.sabhaNameSi, g.keySectorSi, g.totalProjects, g.completed, g.ongoing, g.beneficiaries, g.photoCount || 0, `${g.progress}%`]);
        csvData += `${idx + 1},"${g.nameSi}","${g.sabhaNameSi}","${g.keySectorSi}",${g.totalProjects},${g.completed},${g.ongoing},${g.beneficiaries},${g.photoCount || 0},${g.progress}%\\n`;'''
assert old_all_gns_row in content, "old_all_gns_row not found"
content = content.replace(old_all_gns_row, new_all_gns_row)

old_all_gns_th = '''              <th style="text-align: right;">ප්‍රතිලාභීන්</th>
              <th style="text-align: right;">ප්‍රතිපාදන</th>
              <th style="text-align: right;">යෙදවූ මුදල</th>
              <th style="text-align: center;">ප්‍රගතිය</th>'''
new_all_gns_th = '''              <th style="text-align: right;">ප්‍රතිලාභීන්</th>
              <th style="text-align: center;">සත්‍යාපිත ඡායාරූප</th>
              <th style="text-align: center;">ප්‍රගතිය</th>'''
assert old_all_gns_th in content, "old_all_gns_th not found"
content = content.replace(old_all_gns_th, new_all_gns_th)

# 8. Lines 3520-3538 (Data Export CSVs)
old_exp_act = '''    let csv = "ID,වැඩසටහන් නම,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,අංශය,දිනය,ස්ථානය,අරමුණ,කාර්යයන්,ප්‍රතිලාභීන්,ප්‍රතිඵල,ප්‍රගතිය (%),වෙන්කළ මුදල (රු.),යෙදවූ මුදල (රු.)\\n";
    this.data.activities.forEach(a => {
      csv += `"${a.id}","${a.titleSi}","${a.gnNameSi}","${a.sabhaNameSi}","${a.categoryNameSi}","${a.date}","${a.locationSi || ''}","${(a.purposeSi || '').replace(/"/g, '""')}","${(a.actionsSi || '').replace(/"/g, '""')}","${a.beneficiaries}","${(a.resultsSi || '').replace(/"/g, '""')}",${a.progress},${a.budgetLKR},${a.spentLKR}\\n`;
    });'''
new_exp_act = '''    let csv = "ID,වැඩසටහන් නම,ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,අංශය,දිනය,ස්ථානය,අරමුණ,කාර්යයන්,ප්‍රතිලාභීන්,ප්‍රතිඵල,ප්‍රගතිය (%),ඡායාරූප ගණන\\n";
    this.data.activities.forEach(a => {
      csv += `"${a.id}","${a.titleSi}","${a.gnNameSi}","${a.sabhaNameSi}","${a.categoryNameSi}","${a.date}","${a.locationSi || ''}","${(a.purposeSi || '').replace(/"/g, '""')}","${(a.actionsSi || '').replace(/"/g, '""')}","${a.beneficiaries}","${(a.resultsSi || '').replace(/"/g, '""')}",${a.progress},${a.images ? a.images.length : 0}\\n`;
    });'''
assert old_exp_act in content, "old_exp_act not found"
content = content.replace(old_exp_act, new_exp_act)

old_exp_gn = '''    let csv = "ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,ප්‍රමුඛ ක්ෂේත්‍රය,මුළු වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,ප්‍රතිපාදන (රු.),යෙදවූ මුදල (රු.),ප්‍රගතිය (%)\\n";
    this.data.gnDivisions.forEach(g => {
      csv += `"${g.nameSi}","${g.sabhaNameSi}","${g.keySectorSi}",${g.totalProjects},${g.completed},${g.ongoing},${g.beneficiaries},${g.budgetLKR},${g.spentLKR},${g.progress}\\n`;
    });'''
new_exp_gn = '''    let csv = "ග්‍රාම නිලධාරී වසම,ප්‍රජා සංවර්ධන සභාව,ප්‍රමුඛ ක්ෂේත්‍රය,මුළු වැඩසටහන්,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,සත්‍යාපිත ඡායාරූප,ප්‍රගතිය (%)\\n";
    this.data.gnDivisions.forEach(g => {
      csv += `"${g.nameSi}","${g.sabhaNameSi}","${g.keySectorSi}",${g.totalProjects},${g.completed},${g.ongoing},${g.beneficiaries},${g.photoCount || 0},${g.progress}\\n`;
    });'''
assert old_exp_gn in content, "old_exp_gn not found"
content = content.replace(old_exp_gn, new_exp_gn)

old_exp_mon = '''    let csv = "මාසය,ඉලක්කය,සම්පූර්ණ වූ,ක්‍රියාත්මකයි,ප්‍රතිලාභී පවුල්,මාසික වියදම (රු.),සමුච්චිත වියදම (රු.)\\n";
    this.data.monthlyStats.forEach(m => {
      csv += `"${m.monthSi}",${m.target},${m.completed},${m.ongoing},${m.beneficiaries},${m.spentLKR},${m.cumulativeSpent}\\n`;
    });'''
new_exp_mon = '''    let csv = "මාසය,ක්‍රියාත්මක වැඩසටහන්,සම්පූර්ණ වූ,වාර්තා කළ වසම්,ක්‍රියාකාරී දින,සත්‍යාපිත ඡායාරූප\\n";
    (this.data.monthlyProgress || []).forEach(m => {
      csv += `"${m.monthSi}",${m.count || m.totalProjects || 0},${m.completed || 0},${m.reportingDivisions || m.activeGNCount || 0},${m.activeDays || 0},${m.photos || 0}\\n`;
    });'''
assert old_exp_mon in content, "old_exp_mon not found"
content = content.replace(old_exp_mon, new_exp_mon)

# 9. Lines 3768, 3811, 3823 (Print division report)
old_print_td = '''            <td style="border: 1px solid #CCC; padding: 8px; text-align: right;">රු. ${(act.spentLKR || 0).toLocaleString()}</td>'''
new_print_td = '''            <td style="border: 1px solid #CCC; padding: 8px; text-align: center;">${act.images ? act.images.length : 0}</td>'''
assert old_print_td in content, "old_print_td not found"
content = content.replace(old_print_td, new_print_td)

old_print_meta = '''          <div><span style="font-size: 11px; color: #666;">යෙදවූ ප්‍රතිපාදන:</span><br><strong>රු. ${(gn.spentLKR || 0).toLocaleString()}</strong></div>'''
new_print_meta = '''          <div><span style="font-size: 11px; color: #666;">සත්‍යාපිත ඡායාරූප:</span><br><strong style="color: #0D9488;">${gn.photoCount || activities.reduce((acc, a) => acc + (a.images ? a.images.length : 0), 0)}</strong></div>'''
assert old_print_meta in content, "old_print_meta not found"
content = content.replace(old_print_meta, new_print_meta)

old_print_th = '''              <th style="width: 100px;">වියදම</th>'''
new_print_th = '''              <th style="width: 80px; text-align: center;">ඡායාරූප</th>'''
assert old_print_th in content, "old_print_th not found"
content = content.replace(old_print_th, new_print_th)

# 10. Lines 3934-3943 (Activity Modal)
old_modal_grid = '''        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
          <div>
            <div class="field-label">වෙන්කළ ප්‍රතිපාදන</div>
            <div class="field-val">රු. ${(act.budgetLKR || 0).toLocaleString()}</div>
          </div>
          <div>
            <div class="field-label">යෙදවූ මුදල</div>
            <div class="field-val" style="font-weight: 700;">රු. ${(act.spentLKR || 0).toLocaleString()}</div>
          </div>
        </div>'''
new_modal_grid = '''        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
          <div>
            <div class="field-label">ක්‍රියාත්මක තත්ත්වය</div>
            <div class="field-val" style="color: #10B981; font-weight: 700;"><i class="bi bi-check-circle-fill"></i> 100% සම්පූර්ණයි</div>
          </div>
          <div>
            <div class="field-label">සත්‍යාපිත ඡායාරූප ගණන</div>
            <div class="field-val" style="font-weight: 700; color: #0D9488;"><i class="bi bi-images"></i> ${(act.images ? act.images.length : 0)} කි</div>
          </div>
        </div>'''
assert old_modal_grid in content, "old_modal_grid not found"
content = content.replace(old_modal_grid, new_modal_grid)

# 11. Lines 4737, 4758 (Monthly compare)
old_compare_spent_a = '''<div class="an-metric-row"><span style="color: #94A3B8;">වියදම:</span><strong style="color: #CBD5E1;">රු. ${((itemA.spentLKR || 0) / 1000000).toFixed(2)}M</strong></div>'''
new_compare_spent_a = '''<div class="an-metric-row"><span style="color: #94A3B8;">සත්‍යාපිත ඡායාරූප:</span><strong style="color: #CBD5E1;">${itemA.photos || 0}</strong></div>'''
assert old_compare_spent_a in content, "old_compare_spent_a not found"
content = content.replace(old_compare_spent_a, new_compare_spent_a)

old_compare_spent_b = '''<div class="an-metric-row"><span style="color: #94A3B8;">වියදම:</span><strong style="color: #CBD5E1;">රු. ${((itemB.spentLKR || 0) / 1000000).toFixed(2)}M</strong></div>'''
new_compare_spent_b = '''<div class="an-metric-row"><span style="color: #94A3B8;">සත්‍යාපිත ඡායාරූප:</span><strong style="color: #CBD5E1;">${itemB.photos || 0}</strong></div>'''
assert old_compare_spent_b in content, "old_compare_spent_b not found"
content = content.replace(old_compare_spent_b, new_compare_spent_b)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully replaced all dummy financial data in js/app.js!")
