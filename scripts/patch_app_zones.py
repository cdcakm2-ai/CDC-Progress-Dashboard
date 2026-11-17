with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '  initActivitiesDivisionShowcase() {'
end_marker = '    // Calculate total photos and unique dates for this division'

p1 = text.find(start_marker)
p2 = text.find(end_marker)

replacement = '''  initActivitiesDivisionShowcase() {
    this.selectedActivitiesGnIndex = 0;
    this.currentGnZone = "all";
    this.gnViewType = "slider"; // "slider" or "grouped"

    // 1. View Mode Toggles (Division Web Article vs Flat List)
    const btnDivMode = document.getElementById("btnActivitiesDivisionMode");
    const btnFlatMode = document.getElementById("btnActivitiesFlatMode");
    const divView = document.getElementById("activitiesDivisionModeView");
    const flatView = document.getElementById("activitiesFlatModeView");

    if (btnDivMode && btnFlatMode) {
      btnDivMode.addEventListener("click", () => {
        this.activitiesViewMode = "division";
        btnDivMode.classList.add("active");
        btnFlatMode.classList.remove("active");
        if (divView) divView.style.display = "block";
        if (flatView) flatView.style.display = "none";
        this.renderDivisionActivitiesShowcase();
      });

      btnFlatMode.addEventListener("click", () => {
        this.activitiesViewMode = "flat";
        btnFlatMode.classList.add("active");
        btnDivMode.classList.remove("active");
        if (divView) divView.style.display = "none";
        if (flatView) flatView.style.display = "block";
        this.renderFlatActivities();
      });
    }

    // 2. Zone Clusters Definitions
    this.gnZones = [
      { id: "all", name: "සියලු කලාප", label: "සියලු කලාප (63)", badge: "63" },
      { id: "109", name: "109 කලාපය", label: "109 කලාපය (වසම් 8)", badge: "8", test: g => g.nameSi.includes("109") },
      { id: "110-113", name: "110-113 කලාපය", label: "110-113 කලාපය (වසම් 12)", badge: "12", test: g => ["110", "111", "112", "113"].some(k => g.nameSi.includes(k)) },
      { id: "118", name: "118 කලාපය", label: "118 කලාපය (වසම් 8)", badge: "8", test: g => g.nameSi.includes("118") },
      { id: "130", name: "130 කලාපය", label: "130 කලාපය (වසම් 6)", badge: "6", test: g => g.nameSi.includes("130") },
      { id: "133", name: "133 කලාපය", label: "133 කලාපය (වසම් 6)", badge: "6", test: g => g.nameSi.includes("133") },
      { id: "134-135", name: "134-135 කලාපය", label: "134-135 කලාපය (වසම් 9)", badge: "9", test: g => ["134", "135"].some(k => g.nameSi.includes(k)) },
      { id: "152", name: "152 කලාපය", label: "152 කලාපය (වසම් 6)", badge: "6", test: g => g.nameSi.includes("152") },
      { id: "155", name: "155 කලාපය", label: "155 කලාපය (වසම් 8)", badge: "8", test: g => g.nameSi.includes("155") },
    ];

    // 3. Render Zone Filter Ribbon
    this.renderGnZoneBar();

    // 4. Slider vs Grouped Toggle Buttons
    const btnSliderToggle = document.getElementById("btnToggleGnSliderView");
    const btnGroupedToggle = document.getElementById("btnToggleGnGroupedView");
    const sliderWrap = document.getElementById("activitiesGnSliderWrap");
    const groupedWrap = document.getElementById("activitiesGnGroupedView");

    if (btnSliderToggle && btnGroupedToggle) {
      btnSliderToggle.addEventListener("click", () => {
        this.gnViewType = "slider";
        btnSliderToggle.classList.add("active");
        btnSliderToggle.style.background = "#3979D6";
        btnSliderToggle.style.color = "#FFF";
        btnGroupedToggle.classList.remove("active");
        btnGroupedToggle.style.background = "transparent";
        btnGroupedToggle.style.color = "#526078";
        if (sliderWrap) sliderWrap.style.display = "block";
        if (groupedWrap) groupedWrap.style.display = "none";
      });

      btnGroupedToggle.addEventListener("click", () => {
        this.gnViewType = "grouped";
        btnGroupedToggle.classList.add("active");
        btnGroupedToggle.style.background = "#3979D6";
        btnGroupedToggle.style.color = "#FFF";
        btnSliderToggle.classList.remove("active");
        btnSliderToggle.style.background = "transparent";
        btnSliderToggle.style.color = "#526078";
        if (sliderWrap) sliderWrap.style.display = "none";
        if (groupedWrap) {
          groupedWrap.style.display = "block";
          this.renderGnGroupedCards();
        }
      });
    }

    // 5. Populate Grouped Dropdown
    this.populateGroupedGnDropdown();

    // 6. Populate GN Nav Pills (Slider track)
    this.renderGnNavPills();

    // 7. GN Quick Search Input
    const gnSearch = document.getElementById("activitiesGnSearchInput");
    if (gnSearch) {
      gnSearch.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase().trim();
        this.filterGnNavPills(q);
      });
    }

    // 8. Interactive Slider Scroll Buttons (Left / Right)
    const btnSliderLeft = document.getElementById("btnSliderScrollLeft");
    const btnSliderRight = document.getElementById("btnSliderScrollRight");
    const sliderTrack = document.getElementById("activitiesGnNavPills");
    if (btnSliderLeft && sliderTrack) {
      btnSliderLeft.addEventListener("click", () => {
        sliderTrack.scrollBy({ left: -320, behavior: "smooth" });
      });
    }
    if (btnSliderRight && sliderTrack) {
      btnSliderRight.addEventListener("click", () => {
        sliderTrack.scrollBy({ left: 320, behavior: "smooth" });
      });
    }

    // 9. Prev / Next GN buttons on banner
    const btnPrev = document.getElementById("btnPrevGnDivision");
    const btnNext = document.getElementById("btnNextGnDivision");
    if (btnPrev) {
      btnPrev.addEventListener("click", () => {
        if (this.selectedActivitiesGnIndex > 0) {
          this.selectGnDivision(this.selectedActivitiesGnIndex - 1);
        }
      });
    }
    if (btnNext) {
      btnNext.addEventListener("click", () => {
        if (this.selectedActivitiesGnIndex < this.data.gnDivisions.length - 1) {
          this.selectGnDivision(this.selectedActivitiesGnIndex + 1);
        }
      });
    }

    // Render the initial showcase
    this.renderDivisionActivitiesShowcase();
  }

  getGnZoneId(gnName) {
    if (gnName.includes("109")) return "109";
    if (["110", "111", "112", "113"].some(k => gnName.includes(k))) return "110-113";
    if (gnName.includes("118")) return "118";
    if (gnName.includes("130")) return "130";
    if (gnName.includes("133")) return "133";
    if (["134", "135"].some(k => gnName.includes(k))) return "134-135";
    if (gnName.includes("152")) return "152";
    if (gnName.includes("155")) return "155";
    return "other";
  }

  renderGnZoneBar() {
    const bar = document.getElementById("activitiesGnZoneBar");
    if (!bar) return;
    bar.innerHTML = "";

    this.gnZones.forEach(zone => {
      const btn = document.createElement("button");
      btn.className = `zone-filter-btn ${zone.id === this.currentGnZone ? "active" : ""}`;
      btn.innerHTML = `<span>${zone.name}</span> <span class="zone-badge">${zone.badge}</span>`;
      btn.addEventListener("click", () => {
        this.currentGnZone = zone.id;
        document.querySelectorAll("#activitiesGnZoneBar .zone-filter-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        
        // Re-render slider pills for this zone
        this.renderGnNavPills();

        // If in grouped view, scroll to zone card
        if (this.gnViewType === "grouped") {
          this.renderGnGroupedCards();
          if (zone.id !== "all") {
            const zCard = document.getElementById(`gnGroupCard-${zone.id}`);
            if (zCard) zCard.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        }
      });
      bar.appendChild(btn);
    });
  }

  populateGroupedGnDropdown() {
    const gnDropdown = document.getElementById("activitiesGnSelectDropdown");
    if (!gnDropdown) return;
    gnDropdown.innerHTML = "";

    const zonesForDropdown = this.gnZones.filter(z => z.id !== "all");
    zonesForDropdown.forEach(zone => {
      const optgroup = document.createElement("optgroup");
      optgroup.label = zone.label;

      this.data.gnDivisions.forEach((gn, idx) => {
        if (zone.test(gn)) {
          const opt = document.createElement("option");
          opt.value = idx;
          const gnActs = this.data.activities.filter(a => a.gnNameSi === gn.nameSi);
          opt.textContent = `${(idx + 1).toString().padStart(2, "0")}. ${gn.nameSi} (${gnActs.length} වැඩසටහන්)`;
          optgroup.appendChild(opt);
        }
      });

      if (optgroup.children.length > 0) {
        gnDropdown.appendChild(optgroup);
      }
    });

    gnDropdown.addEventListener("change", (e) => {
      const idx = parseInt(e.target.value, 10);
      this.selectGnDivision(idx);
    });
  }

  renderGnNavPills() {
    const container = document.getElementById("activitiesGnNavPills");
    if (!container) return;
    container.innerHTML = "";

    this.data.gnDivisions.forEach((gn, idx) => {
      const zId = this.getGnZoneId(gn.nameSi);
      if (this.currentGnZone !== "all" && zId !== this.currentGnZone) {
        return; // filter to current zone
      }

      const gnActs = this.data.activities.filter(a => a.gnNameSi === gn.nameSi);
      const btn = document.createElement("button");
      btn.className = `gn-nav-pill-btn ${idx === this.selectedActivitiesGnIndex ? "active" : ""}`;
      btn.setAttribute("data-gn-idx", idx);
      btn.innerHTML = `
        <span>${gn.nameSi}</span>
        <span class="gn-nav-pill-badge">${gnActs.length}</span>
      `;
      btn.addEventListener("click", () => {
        this.selectGnDivision(idx);
      });
      container.appendChild(btn);
    });

    // Ensure active pill is scrolled into view
    setTimeout(() => {
      const activePill = container.querySelector(".gn-nav-pill-btn.active");
      if (activePill) {
        activePill.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      }
    }, 100);
  }

  renderGnGroupedCards() {
    const container = document.getElementById("activitiesGnGroupedView");
    if (!container) return;
    container.innerHTML = "";

    const zonesToRender = this.currentGnZone === "all" 
      ? this.gnZones.filter(z => z.id !== "all") 
      : this.gnZones.filter(z => z.id === this.currentGnZone);

    zonesToRender.forEach(zone => {
      const gnsInZone = this.data.gnDivisions.map((gn, idx) => ({ gn, idx })).filter(item => zone.test(item.gn));
      if (!gnsInZone.length) return;

      const totalActsInZone = gnsInZone.reduce((acc, item) => {
        return acc + this.data.activities.filter(a => a.gnNameSi === item.gn.nameSi).length;
      }, 0);

      const card = document.createElement("div");
      card.className = "gn-group-card";
      card.id = `gnGroupCard-${zone.id}`;

      let pillsHtml = gnsInZone.map(item => {
        const gnActs = this.data.activities.filter(a => a.gnNameSi === item.gn.nameSi);
        const isActive = (item.idx === this.selectedActivitiesGnIndex);
        return `
          <button class="gn-nav-pill-btn ${isActive ? 'active' : ''}" data-gn-idx="${item.idx}" style="justify-content: space-between; width: 100%;">
            <span>${item.gn.nameSi}</span>
            <span class="gn-nav-pill-badge">${gnActs.length}</span>
          </button>
        `;
      }).join("");

      card.innerHTML = `
        <div class="gn-group-header">
          <span style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="bi bi-collection-fill" style="color: #3979D6;"></i>
            <strong>${zone.label}</strong>
          </span>
          <span class="glass-badge blue" style="font-size: 0.76rem;">${totalActsInZone} වැඩසටහන්</span>
        </div>
        <div class="gn-group-grid">
          ${pillsHtml}
        </div>
      `;

      card.querySelectorAll(".gn-nav-pill-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const idx = parseInt(btn.getAttribute("data-gn-idx"), 10);
          this.selectGnDivision(idx);
        });
      });

      container.appendChild(card);
    });
  }

  selectGnDivision(idx) {
    this.selectedActivitiesGnIndex = idx;
    const gn = this.data.gnDivisions[idx];
    if (gn) {
      const zId = this.getGnZoneId(gn.nameSi);
      // If selected division is outside current zone filter, reset zone to all or switch zone
      if (this.currentGnZone !== "all" && zId !== this.currentGnZone) {
        this.currentGnZone = zId;
        this.renderGnZoneBar();
      }
    }
    this.renderDivisionActivitiesShowcase();
    this.renderGnNavPills();
    if (this.gnViewType === "grouped") {
      this.renderGnGroupedCards();
    }
  }

  filterGnNavPills(q) {
    const pills = document.querySelectorAll("#activitiesGnNavPills .gn-nav-pill-btn");
    pills.forEach(pill => {
      const text = pill.textContent.toLowerCase();
      pill.style.display = text.includes(q) ? "inline-flex" : "none";
    });

    const gnDropdown = document.getElementById("activitiesGnSelectDropdown");
    if (gnDropdown) {
      Array.from(gnDropdown.options).forEach(opt => {
        const matches = opt.textContent.toLowerCase().includes(q);
        opt.hidden = q ? !matches : false;
      });
    }
  }

  renderDivisionActivitiesShowcase() {
    const gn = this.data.gnDivisions[this.selectedActivitiesGnIndex] || this.data.gnDivisions[0];
    if (!gn) return;

    // Update active state in pills
    const pills = document.querySelectorAll("#activitiesGnNavPills .gn-nav-pill-btn");
    pills.forEach((p) => {
      const idx = parseInt(p.getAttribute("data-gn-idx"), 10);
      if (idx === this.selectedActivitiesGnIndex) {
        p.classList.add("active");
        p.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      } else {
        p.classList.remove("active");
      }
    });

    // Update dropdown
    const dropdown = document.getElementById("activitiesGnSelectDropdown");
    if (dropdown) dropdown.value = this.selectedActivitiesGnIndex;

    // Filter activities for this GN division
    const gnActs = this.data.activities.filter(a => a.gnNameSi === gn.nameSi);
    
'''

new_text = text[:p1] + replacement + text[p2:]

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Successfully patched js/app.js with Zone Clusters, Slider, and Grouped Cards logic!")
