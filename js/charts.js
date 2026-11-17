/**
 * Interactive Charts Engine - Divisional Secretariat Digital Toolkit
 * ප්‍රජා සංවර්ධන සභා මගින් සිදු කරන ලද වැඩසටහන් - අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසය
 * 
 * Premium Multi-Color Visualizations System:
 * - Deep navy, Royal blue, Teal, Emerald, Violet, Indigo, Cyan, Amber & Coral palettes
 * - Smooth canvas gradient fills
 * - Modern dark glass tooltips
 * - Highly responsive, high contrast Sinhala typography
 */

class PssCharts {
  constructor() {
    this.data = (typeof window !== "undefined" && window.PSS_DATA) ? window.PSS_DATA : {};

    // Standard Charts
    this.monthlyChart = null;
    this.categoryChart = null;
    this.gnRankingChart = null;

    // Advanced Progress Analytics Charts (Tab 5)
    this.anCumulativeChart = null;
    this.anMonthlyTrendChart = null;
    this.anTopDivisionsChart = null;
    this.anSectorDoughnutChart = null;
    this.anSectorBarChart = null;
    this.anWeekdayChart = null;
    this.anWeekendChart = null;
    this.anDiversityDistChart = null;
    this.anCompareChart = null;
    this.anDeepdiveFinChart = null;

    this.defaultFont = "'Noto Sans Sinhala', 'Plus Jakarta Sans', sans-serif";

    // Curated Premium Light Palette
    this.palette = [
      "#3979D6", // Primary Blue
      "#159C91", // Teal
      "#36A47A", // Emerald
      "#8B68CC", // Violet
      "#E69B51", // Soft Orange
      "#E16F83", // Coral
      "#243B64", // Deep Navy
      "#0891B2", // Cyan
      "#F59E0B", // Amber
      "#6366F1"  // Indigo
    ];
  }

  // Canvas Gradient Helpers
  getVerticalGrad(ctx, c1, c2, h = 320) {
    if (!ctx) return c1;
    try {
      const g = ctx.createLinearGradient(0, 0, 0, h);
      g.addColorStop(0, c1);
      g.addColorStop(1, c2);
      return g;
    } catch {
      return c1;
    }
  }

  getHorizontalGrad(ctx, c1, c2, w = 450) {
    if (!ctx) return c1;
    try {
      const g = ctx.createLinearGradient(0, 0, w, 0);
      g.addColorStop(0, c1);
      g.addColorStop(1, c2);
      return g;
    } catch {
      return c1;
    }
  }

  getTooltipConfig() {
    return {
      backgroundColor: "rgba(15, 23, 42, 0.94)",
      titleColor: "#FFFFFF",
      bodyColor: "#CBD5E1",
      borderColor: "rgba(255, 255, 255, 0.15)",
      borderWidth: 1,
      padding: 12,
      cornerRadius: 10,
      titleFont: { family: this.defaultFont, size: 12.5, weight: "700" },
      bodyFont: { family: this.defaultFont, size: 12 },
      usePointStyle: true,
      boxPadding: 6
    };
  }

  init(data) {
    this.data = data || ((typeof window !== "undefined" && window.PSS_DATA) ? window.PSS_DATA : {});
    if (typeof Chart === "undefined") {
      console.warn("Chart.js library is not available yet. Charts will initialize when ready.");
      return;
    }
    try {
      this.renderAll();
    } catch (e) {
      console.warn("Chart rendering warning:", e);
    }
  }

  renderAll() {
    if (typeof Chart === "undefined") return;
    try { this.renderMonthlyChart(); } catch (e) { console.warn("Monthly chart error:", e); }
    try { this.renderCategoryChart(); } catch (e) { console.warn("Category chart error:", e); }
    try { this.renderGNRankingChart(); } catch (e) { console.warn("GN ranking chart error:", e); }
    try { this.renderAllAnalyticsCharts(); } catch (e) { console.warn("Analytics charts error:", e); }
  }

  resizeAll() {
    setTimeout(() => {
      const charts = [
        this.monthlyChart, this.categoryChart, this.gnRankingChart,
        this.anCumulativeChart, this.anMonthlyTrendChart, this.anTopDivisionsChart,
        this.anSectorDoughnutChart, this.anSectorBarChart, this.anWeekdayChart,
        this.anWeekendChart, this.anDiversityDistChart, this.anCompareChart,
        this.anDeepdiveFinChart
      ];
      charts.forEach(c => {
        if (c && typeof c.resize === "function") c.resize();
      });
    }, 100);
  }

  /**
   * 1. Tab 1 & 2: Monthly Progress Bar & Line Chart
   * Royal Blue / Cyan Gradient Bars + Emerald Line
   */
  renderMonthlyChart() {
    const canvas = document.getElementById("monthlyProgressChart");
    if (!canvas) return;
    if (this.monthlyChart) this.monthlyChart.destroy();

    const ctx = canvas.getContext("2d");
    const stats = this.data?.monthlyStats || this.data?.monthlySummary || [];
    if (!stats.length) return;

    const labels = stats.map(m => m.nameSi ? m.nameSi.replace(" මාසික වාර්තාව", "") : (m.monthSi || m.month));
    const completedData = stats.map(m => m.count || m.totalProjects || 0);
    const activeDaysData = stats.map(m => m.activeDays || 0);

    const barGrad = this.getVerticalGrad(ctx, "rgba(37, 99, 235, 0.95)", "rgba(8, 145, 178, 0.75)", 340);
    const lineFillGrad = this.getVerticalGrad(ctx, "rgba(5, 150, 105, 0.28)", "rgba(5, 150, 105, 0.0)", 340);

    this.monthlyChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "සිදුකළ වැඩසටහන් සංඛ්‍යාව",
            data: completedData,
            backgroundColor: barGrad,
            borderColor: "#60A5FA",
            borderWidth: 1.5,
            borderRadius: 8,
            hoverBackgroundColor: "#38BDF8",
            yAxisID: "y"
          },
          {
            label: "සක්‍රිය දින ගණන",
            data: activeDaysData,
            type: "line",
            yAxisID: "y1",
            borderColor: "#10B981",
            backgroundColor: lineFillGrad,
            borderWidth: 3,
            pointBackgroundColor: "#34D399",
            pointBorderColor: "#FFFFFF",
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 8,
            tension: 0.38,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: {
            position: "top",
            labels: {
              color: "#CBD5E1",
              font: { family: this.defaultFont, size: 12, weight: "600" },
              usePointStyle: true,
              boxWidth: 8,
              padding: 16
            }
          },
          tooltip: this.getTooltipConfig()
        },
        scales: {
          x: {
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            ticks: { color: "#94A3B8", font: { family: this.defaultFont, size: 11 } }
          },
          y: {
            title: { display: true, text: "වැඩසටහන් ගණන", color: "#60A5FA", font: { family: this.defaultFont, size: 11, weight: "600" } },
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            ticks: { color: "#94A3B8" }
          },
          y1: {
            type: "linear",
            display: true,
            position: "right",
            title: { display: true, text: "සක්‍රිය දින", color: "#34D399", font: { family: this.defaultFont, size: 11, weight: "600" } },
            grid: { drawOnChartArea: false },
            ticks: { color: "#34D399" }
          }
        }
      }
    });
  }

  /**
   * 2. Tab 1: Category Breakdown Doughnut Chart
   * 10-Color Multi-Palette with Cutout Depth
   */
  renderCategoryChart() {
    const canvas = document.getElementById("categoryBreakdownChart");
    if (!canvas) return;
    if (this.categoryChart) this.categoryChart.destroy();

    const cats = this.data?.categories || this.data?.analyticalCategories || [];
    if (!cats.length) return;

    const labels = cats.map(c => c.nameSi);
    const dataValues = cats.map(c => c.count);
    const colors = cats.map((c, i) => c.color || this.palette[i % this.palette.length]);

    this.categoryChart = new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [{
          data: dataValues,
          backgroundColor: colors,
          borderColor: "#FFFFFF",
          borderWidth: 2.5,
          hoverOffset: 12
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "66%",
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: "#CBD5E1",
              font: { family: this.defaultFont, size: 10.5 },
              usePointStyle: true,
              padding: 10
            }
          },
          tooltip: {
            ...this.getTooltipConfig(),
            callbacks: {
              label: (ctx) => {
                const val = ctx.raw || 0;
                const total = ctx.chart._metasets[ctx.datasetIndex].total || 1;
                const pct = ((val / total) * 100).toFixed(1);
                return ` ${ctx.label}: ${val} (${pct}%)`;
              }
            }
          }
        }
      }
    });
  }

  /**
   * 3. Tab 1: Top 8 GN Divisions Ranking Horizontal Bar Chart
   * Violet to Royal Blue Gradient
   */
  renderGNRankingChart() {
    const canvas = document.getElementById("gnProgressChart");
    if (!canvas) return;
    if (this.gnRankingChart) this.gnRankingChart.destroy();

    const ctx = canvas.getContext("2d");
    const rawDivs = this.data?.gnDivisions || [];
    if (!rawDivs.length) return;

    const sorted = [...rawDivs].sort((a, b) => b.totalProjects - a.totalProjects).slice(0, 8);
    const labels = sorted.map(g => g.nameSi);
    const projects = sorted.map(g => g.totalProjects);

    const grad = this.getHorizontalGrad(ctx, "rgba(124, 58, 237, 0.95)", "rgba(37, 99, 235, 0.85)", 400);

    this.gnRankingChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "ක්‍රියාත්මක කළ මුළු වැඩසටහන්",
            data: projects,
            backgroundColor: grad,
            borderColor: "#C084FC",
            borderWidth: 1,
            borderRadius: 6,
            hoverBackgroundColor: "#38BDF8"
          }
        ]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
            labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" }, usePointStyle: true }
          },
          tooltip: this.getTooltipConfig()
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#94A3B8" } },
          y: {
            grid: { display: false },
            ticks: { color: "#FFFFFF", font: { family: this.defaultFont, size: 11.5, weight: "500" } }
          }
        }
      }
    });
  }

  // =========================================================================
  // ADVANCED PROGRESS ANALYTICS CHARTS (TAB 5)
  // =========================================================================

  renderAllAnalyticsCharts() {
    this.renderAnCumulativeChart();
    this.renderAnMonthlyTrendChart();
    this.renderAnTopDivisionsChart();
    this.renderAnSectorCharts();
    this.renderAnTimelineCharts();
    this.renderAnDiversityChart();
    this.renderAnDeepdiveFinChart();
  }

  /**
   * 4. Analytics: Cumulative Growth Curve
   * Royal Blue Bars + Glowing Amber/Gold Cumulative Area Curve
   */
  renderAnCumulativeChart(monthlyData) {
    const canvas = document.getElementById("anCumulativeChart");
    if (!canvas) return;
    if (this.anCumulativeChart) this.anCumulativeChart.destroy();

    const ctx = canvas.getContext("2d");
    const data = monthlyData || this.data?.monthlyStats || this.data?.monthlySummary || [];
    if (!data.length) return;

    const labels = data.map(m => m.nameSi ? m.nameSi.replace(" මාසික වාර්තාව", "") : (m.monthSi || m.month));
    const monthlyCounts = data.map(m => m.count || m.totalProjects || 0);
    const cumulativeCounts = data.map(m => m.cumulativeCount || m.cumulativeTotal || 0);

    const barGrad = this.getVerticalGrad(ctx, "rgba(79, 70, 229, 0.85)", "rgba(37, 99, 235, 0.5)", 340);
    const lineGrad = this.getVerticalGrad(ctx, "rgba(217, 119, 6, 0.35)", "rgba(217, 119, 6, 0.02)", 340);

    this.anCumulativeChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "මාසික වැඩසටහන් සංඛ්‍යාව",
            data: monthlyCounts,
            backgroundColor: barGrad,
            borderColor: "#818CF8",
            borderWidth: 1.5,
            borderRadius: 7,
            yAxisID: "y"
          },
          {
            label: "සමුච්චිත ප්‍රගති වක්‍රය (මුළු එකතුව)",
            data: cumulativeCounts,
            type: "line",
            yAxisID: "y1",
            borderColor: "#F59E0B",
            backgroundColor: lineGrad,
            borderWidth: 3,
            pointBackgroundColor: "#FDE68A",
            pointBorderColor: "#FFFFFF",
            pointBorderWidth: 2,
            pointRadius: 5.5,
            pointHoverRadius: 8,
            tension: 0.35,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: {
            position: "top",
            labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" }, usePointStyle: true }
          },
          tooltip: this.getTooltipConfig()
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#94A3B8", font: { family: this.defaultFont, size: 10.5 } } },
          y: {
            title: { display: true, text: "මාසික වැඩසටහන්", color: "#818CF8", font: { family: this.defaultFont, size: 11, weight: "600" } },
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            ticks: { color: "#94A3B8" }
          },
          y1: {
            position: "right",
            title: { display: true, text: "සමුච්චිත එකතුව", color: "#F59E0B", font: { family: this.defaultFont, size: 11, weight: "600" } },
            grid: { drawOnChartArea: false },
            ticks: { color: "#FDE68A" }
          }
        }
      }
    });
  }

  /**
   * 5. Analytics: Monthly Trend & MoM Change % Chart
   * Cyan/Teal Bars + Coral Trend Line
   */
  renderAnMonthlyTrendChart(monthlyData) {
    const canvas = document.getElementById("anMonthlyTrendChart");
    if (!canvas) return;
    if (this.anMonthlyTrendChart) this.anMonthlyTrendChart.destroy();

    const ctx = canvas.getContext("2d");
    const data = monthlyData || this.data?.monthlyStats || this.data?.monthlySummary || [];
    if (!data.length) return;

    const labels = data.map(m => m.nameSi ? m.nameSi.replace(" මාසික වාර්තාව", "") : (m.monthSi || m.month));
    const counts = data.map(m => m.count || m.totalProjects || 0);

    // Calculate real MoM pct
    const momPcts = [];
    for (let i = 0; i < counts.length; i++) {
      if (i === 0 || counts[i - 1] === 0) {
        momPcts.push(0);
      } else {
        const pct = Math.round(((counts[i] - counts[i - 1]) / counts[i - 1]) * 100);
        momPcts.push(pct);
      }
    }

    const tealGrad = this.getVerticalGrad(ctx, "rgba(13, 148, 136, 0.9)", "rgba(8, 145, 178, 0.65)", 340);

    this.anMonthlyTrendChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "වැඩසටහන් සංඛ්‍යාව",
            data: counts,
            backgroundColor: tealGrad,
            borderColor: "#2DD4BF",
            borderWidth: 1.5,
            borderRadius: 7,
            yAxisID: "y"
          },
          {
            label: "MoM වර්ධනය / අඩුවීම (%)",
            data: momPcts,
            type: "line",
            yAxisID: "y1",
            borderColor: "#EA580C",
            backgroundColor: "rgba(234, 88, 12, 0.15)",
            borderWidth: 2.8,
            pointBackgroundColor: momPcts.map(p => p < 0 ? "#EF4444" : "#10B981"),
            pointBorderColor: "#FFFFFF",
            pointRadius: 5.5,
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: {
            position: "top",
            labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" }, usePointStyle: true }
          },
          tooltip: this.getTooltipConfig()
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#94A3B8" } },
          y: {
            title: { display: true, text: "වැඩසටහන් සංඛ්‍යාව", color: "#2DD4BF", font: { family: this.defaultFont, size: 11, weight: "600" } },
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            ticks: { color: "#94A3B8" }
          },
          y1: {
            position: "right",
            title: { display: true, text: "MoM වෙනස (%)", color: "#EA580C", font: { family: this.defaultFont, size: 11, weight: "600" } },
            grid: { drawOnChartArea: false },
            ticks: {
              color: "#FB923C",
              callback: (v) => v + "%"
            }
          }
        }
      }
    });
  }

  /**
   * 6. Analytics: Top 15 GN Divisions Horizontal Bar Chart
   * Rank-based Palette (Gold, Blue, Violet tiers)
   */
  renderAnTopDivisionsChart(divisionsData) {
    const canvas = document.getElementById("anTopDivisionsChart");
    if (!canvas) return;
    if (this.anTopDivisionsChart) this.anTopDivisionsChart.destroy();

    const data = divisionsData || this.data?.gnDivisions || [];
    if (!data.length) return;

    const sorted = [...data].sort((a, b) => b.totalProjects - a.totalProjects).slice(0, 15);
    const labels = sorted.map(d => d.nameSi);
    const completed = sorted.map(d => d.totalProjects);

    const colors = sorted.map((d, idx) => {
      if (idx < 3) return "#D97706"; // Top 3 in Amber/Gold
      if (idx < 8) return "#2563EB"; // 4-8 in Royal Blue
      return "#7C3AED";            // 9-15 in Violet
    });

    this.anTopDivisionsChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "සම්පූර්ණ වූ වැඩසටහන්",
            data: completed,
            backgroundColor: colors,
            borderRadius: 6
          }
        ]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
            labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" }, usePointStyle: true }
          },
          tooltip: this.getTooltipConfig()
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#94A3B8" } },
          y: {
            grid: { display: false },
            ticks: { color: "#FFFFFF", font: { family: this.defaultFont, size: 11.5, weight: "500" } }
          }
        }
      }
    });
  }

  /**
   * 7. Analytics: 10 Sectors Charts (Doughnut & Horizontal Bar)
   */
  renderAnSectorCharts(categoriesData) {
    const cats = categoriesData || this.data?.categories || this.data?.analyticalCategories || [];
    if (!cats.length) return;

    // Doughnut
    const dCanvas = document.getElementById("anSectorDoughnutChart");
    if (dCanvas) {
      if (this.anSectorDoughnutChart) this.anSectorDoughnutChart.destroy();
      this.anSectorDoughnutChart = new Chart(dCanvas, {
        type: "doughnut",
        data: {
          labels: cats.map(c => c.nameSi),
          datasets: [{
            data: cats.map(c => c.count),
            backgroundColor: cats.map((c, i) => c.color || this.palette[i % this.palette.length]),
            borderColor: "#FFFFFF",
            borderWidth: 2.5,
            hoverOffset: 10
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "62%",
          plugins: {
            legend: {
              position: "bottom",
              labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 9.5 }, usePointStyle: true, padding: 8 }
            },
            tooltip: {
              ...this.getTooltipConfig(),
              callbacks: {
                label: (ctx) => {
                  const val = ctx.raw || 0;
                  const total = ctx.chart._metasets[ctx.datasetIndex].total || 1;
                  const pct = ((val / total) * 100).toFixed(1);
                  return ` ${ctx.label}: ${val} (${pct}%)`;
                }
              }
            }
          }
        }
      });
    }

    // Horizontal Bar
    const bCanvas = document.getElementById("anSectorBarChart");
    if (bCanvas) {
      if (this.anSectorBarChart) this.anSectorBarChart.destroy();
      const sorted = [...cats].sort((a, b) => b.count - a.count);
      this.anSectorBarChart = new Chart(bCanvas, {
        type: "bar",
        data: {
          labels: sorted.map(c => c.nameSi),
          datasets: [{
            label: "වැඩසටහන් ගණන",
            data: sorted.map(c => c.count),
            backgroundColor: sorted.map((c, i) => c.color || this.palette[i % this.palette.length]),
            borderRadius: 6
          }]
        },
        options: {
          indexAxis: "y",
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: this.getTooltipConfig()
          },
          scales: {
            x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#94A3B8" } },
            y: {
              grid: { display: false },
              ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 10.5 } }
            }
          }
        }
      });
    }
  }

  /**
   * 8. Analytics: Weekday & Weekend Analysis Charts
   */
  renderAnTimelineCharts() {
    const rawActs = this.data?.activities || [];
    const weekdayMap = {
      0: { daySi: "ඉරිදා", count: 0, isWeekend: true, color: "#EA580C" },
      1: { daySi: "සඳුදා", count: 0, isWeekend: false, color: "#2563EB" },
      2: { daySi: "අඟහරුවාදා", count: 0, isWeekend: false, color: "#0891B2" },
      3: { daySi: "බදාදා", count: 0, isWeekend: false, color: "#0D9488" },
      4: { daySi: "බ්‍රහස්පතින්දා", count: 0, isWeekend: false, color: "#059669" },
      5: { daySi: "සිකුරාදා", count: 0, isWeekend: false, color: "#7C3AED" },
      6: { daySi: "සෙනසුරාදා", count: 0, isWeekend: true, color: "#D97706" }
    };

    rawActs.forEach(a => {
      try {
        const d = new Date(a.date);
        const dayIdx = d.getDay();
        if (weekdayMap[dayIdx]) weekdayMap[dayIdx].count++;
      } catch {}
    });

    const daysList = [weekdayMap[1], weekdayMap[2], weekdayMap[3], weekdayMap[4], weekdayMap[5], weekdayMap[6], weekdayMap[0]];
    const weekdaysTotal = daysList.filter(d => !d.isWeekend).reduce((acc, d) => acc + d.count, 0);
    const weekendsTotal = daysList.filter(d => d.isWeekend).reduce((acc, d) => acc + d.count, 0);
    const grandTotal = Math.max(1, weekdaysTotal + weekendsTotal);

    // Weekday Bar Chart
    const wCanvas = document.getElementById("anWeekdayChart");
    if (wCanvas) {
      if (this.anWeekdayChart) this.anWeekdayChart.destroy();
      this.anWeekdayChart = new Chart(wCanvas, {
        type: "bar",
        data: {
          labels: daysList.map(d => d.daySi),
          datasets: [{
            label: "වැඩසටහන් ගණන",
            data: daysList.map(d => d.count),
            backgroundColor: daysList.map(d => d.color),
            borderRadius: 7
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              ...this.getTooltipConfig(),
              callbacks: {
                label: (ctx) => ` ${ctx.raw} වැඩසටහන් (${((ctx.raw / grandTotal) * 100).toFixed(1)}%)`
              }
            }
          },
          scales: {
            x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" } } },
            y: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#94A3B8" } }
          }
        }
      });
    }

    // Weekend vs Weekday Doughnut
    const eCanvas = document.getElementById("anWeekendChart");
    if (eCanvas) {
      if (this.anWeekendChart) this.anWeekendChart.destroy();
      const wDayPct = ((weekdaysTotal / grandTotal) * 100).toFixed(1);
      const wEndPct = ((weekendsTotal / grandTotal) * 100).toFixed(1);

      this.anWeekendChart = new Chart(eCanvas, {
        type: "doughnut",
        data: {
          labels: [`සතියේ වැඩ කරන දින (${wDayPct}%)`, `සති අන්ත දින (${wEndPct}%)`],
          datasets: [{
            data: [weekdaysTotal, weekendsTotal],
            backgroundColor: ["#2563EB", "#EA580C"],
            borderColor: "#FFFFFF",
            borderWidth: 3,
            hoverOffset: 10
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "64%",
          plugins: {
            legend: {
              position: "bottom",
              labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11, weight: "600" }, usePointStyle: true, padding: 12 }
            },
            tooltip: this.getTooltipConfig()
          }
        }
      });
    }
  }

  /**
   * 9. Analytics: Diversity Distribution Histogram Chart
   * 4-Tier Colorful Breakdown
   */
  renderAnDiversityChart(divisionsData) {
    const canvas = document.getElementById("anDiversityDistChart");
    if (!canvas) return;
    if (this.anDiversityDistChart) this.anDiversityDistChart.destroy();

    const data = divisionsData || this.data?.gnDivisions || [];
    if (!data.length) return;

    const tiers = {
      "7+ ක්ෂේත්‍ර (ඉහළම)": 0,
      "5 - 6 ක්ෂේත්‍ර (මධ්‍යස්ථ)": 0,
      "3 - 4 ක්ෂේත්‍ර (සාමාන්‍ය)": 0,
      "1 - 2 ක්ෂේත්‍ර (අවධානය)": 0
    };

    data.forEach(d => {
      const v = d.diversity || 4;
      if (v >= 7) tiers["7+ ක්ෂේත්‍ර (ඉහළම)"]++;
      else if (v >= 5) tiers["5 - 6 ක්ෂේත්‍ර (මධ්‍යස්ථ)"]++;
      else if (v >= 3) tiers["3 - 4 ක්ෂේත්‍ර (සාමාන්‍ය)"]++;
      else tiers["1 - 2 ක්ෂේත්‍ර (අවධානය)"]++;
    });

    this.anDiversityDistChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: Object.keys(tiers),
        datasets: [{
          label: "වසම් සංඛ්‍යාව",
          data: Object.values(tiers),
          backgroundColor: ["#059669", "#2563EB", "#D97706", "#EA580C"],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            ...this.getTooltipConfig(),
            callbacks: {
              label: (ctx) => ` වසම් ${ctx.raw} ක් (${((ctx.raw / 63) * 100).toFixed(1)}%)`
            }
          }
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" } } },
          y: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#94A3B8", stepSize: 5 } }
        }
      }
    });
  }

  /**
   * 10. Analytics: Dual Entity Head-to-Head Comparison Chart
   * Royal Blue vs Amber Dual Bars
   */
  renderAnCompareChart(itemA, itemB, mode) {
    const canvas = document.getElementById("anCompareChart");
    if (!canvas || !itemA || !itemB) return;
    if (this.anCompareChart) this.anCompareChart.destroy();

    let labels = [];
    let dataA = [];
    let dataB = [];

    if (mode === "division") {
      labels = ["මුළු වැඩසටහන්", "සක්‍රිය දින", "සත්‍ය ඡායාරූප"];
      dataA = [itemA.totalProjects || 0, itemA.activeDays || 0, itemA.totalPhotos || 0];
      dataB = [itemB.totalProjects || 0, itemB.activeDays || 0, itemB.totalPhotos || 0];
    } else if (mode === "month") {
      labels = ["වැඩසටහන්", "සක්‍රිය දින", "වාර්තා කළ වසම්", "ඡායාරූප"];
      dataA = [itemA.count || 0, itemA.activeDays || 0, itemA.reportingDivisions || 0, itemA.photos || 0];
      dataB = [itemB.count || 0, itemB.activeDays || 0, itemB.reportingDivisions || 0, itemB.photos || 0];
    } else {
      labels = ["වැඩසටහන් ගණන"];
      dataA = [itemA.count || 0];
      dataB = [itemB.count || 0];
    }

    this.anCompareChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: itemA.nameSi || itemA.monthSi || "පළමු ඒකකය",
            data: dataA,
            backgroundColor: "rgba(37, 99, 235, 0.9)",
            borderColor: "#60A5FA",
            borderWidth: 1.5,
            borderRadius: 7
          },
          {
            label: itemB.nameSi || itemB.monthSi || "දෙවන ඒකකය",
            data: dataB,
            backgroundColor: "rgba(217, 119, 6, 0.9)",
            borderColor: "#FBBF24",
            borderWidth: 1.5,
            borderRadius: 7
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
            labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 12, weight: "bold" }, usePointStyle: true }
          },
          tooltip: this.getTooltipConfig()
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11 } } },
          y: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#94A3B8" } }
        }
      }
    });
  }

  /**
   * 11. Analytics Deep Dive: Top Divisions Activity & Active Days
   * Royal Blue & Teal Grouped Bars
   */
  renderAnDeepdiveFinChart(divisionsData) {
    const canvas = document.getElementById("anDeepdiveFinChart");
    if (!canvas) return;
    if (this.anDeepdiveFinChart) this.anDeepdiveFinChart.destroy();

    const data = divisionsData || this.data?.gnDivisions || [];
    if (!data.length) return;

    const sorted = [...data].sort((a, b) => b.totalProjects - a.totalProjects).slice(0, 10);
    const labels = sorted.map(d => d.nameSi);
    const projects = sorted.map(d => d.totalProjects);
    const activeDays = sorted.map(d => d.activeDays || 0);

    this.anDeepdiveFinChart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "ක්‍රියාත්මක කළ වැඩසටහන්",
            data: projects,
            backgroundColor: "rgba(37, 99, 235, 0.9)",
            borderColor: "#60A5FA",
            borderWidth: 1.5,
            borderRadius: 6
          },
          {
            label: "සක්‍රිය දින ගණන",
            data: activeDays,
            backgroundColor: "rgba(13, 148, 136, 0.9)",
            borderColor: "#2DD4BF",
            borderWidth: 1.5,
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" }, usePointStyle: true } },
          tooltip: this.getTooltipConfig()
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.08)" }, ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 10.5 } } },
          y: {
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            ticks: { color: "#94A3B8" }
          }
        }
      }
    });
  }
}

window.pssCharts = new PssCharts();
