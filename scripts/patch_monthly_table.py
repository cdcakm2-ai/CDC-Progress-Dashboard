with open('js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = """    this.data.monthlyStats.forEach(m => {
      const tr = document.createElement("tr");
      const completionRate = Math.round((m.completed / m.target) * 100);

      tr.innerHTML = `
        <td style="font-weight: 700; color: #FFF;"><i class="bi bi-calendar-event text-gold" style="margin-right: 6px;"></i>${m.monthSi} 2024</td>
        <td style="text-align: center; font-weight: 600;">${m.target}</td>
        <td style="text-align: center; color: #10B981; font-weight: 700;">${m.completed}</td>
        <td style="text-align: center; color: #38BDF8; font-weight: 700;">${m.ongoing}</td>
        <td style="font-weight: 600;">${m.beneficiaries.toLocaleString()} පවුල්</td>
        <td style="font-weight: 600;">රු. ${m.spentLKR.toLocaleString()}</td>
        <td style="font-weight: 600; color: #FDE68A;">රු. ${m.cumulativeSpent.toLocaleString()}</td>"""

replacement = """    (this.data.monthlyStats || []).forEach(m => {
      const tr = document.createElement("tr");
      const targetVal = m.target || m.completed || 1;
      const completionRate = Math.round(((m.completed || 0) / targetVal) * 100);

      tr.innerHTML = `
        <td style="font-weight: 700; color: #FFF;"><i class="bi bi-calendar-event text-gold" style="margin-right: 6px;"></i>${m.monthSi}</td>
        <td style="text-align: center; font-weight: 600;">${m.target || m.completed || 0}</td>
        <td style="text-align: center; color: #10B981; font-weight: 700;">${m.completed || 0}</td>
        <td style="text-align: center; color: #38BDF8; font-weight: 700;">${m.ongoing || 0}</td>
        <td style="font-weight: 600;">${(m.beneficiaries || 0).toLocaleString()} පවුල්</td>
        <td style="font-weight: 600;">${(m.spentLKR || 0) > 0 ? 'රු. ' + m.spentLKR.toLocaleString() : '-'}</td>
        <td style="font-weight: 600; color: #FDE68A;">${(m.cumulativeSpent || 0) > 0 ? 'රු. ' + m.cumulativeSpent.toLocaleString() : '-'}</td>"""

if target in code:
    code = code.replace(target, replacement)
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully patched monthly progress table in js/app.js!")
else:
    print("Target not found in js/app.js")
