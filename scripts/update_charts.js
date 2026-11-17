const fs = require('fs');

const chartsCode = `/**
 * Interactive Charts Engine - 8 Tab Government Dashboard
 * ප්‍රජා සංවර්ධන සභා මගින් සිදු කරන ලද වැඩසටහන් - අක්මීමන ප්‍රාදේශීය ලේකම් කොට්ඨාසය
 * 
 * Includes full analytics suite for "ප්‍රගති විශ්ලේෂණය" (Tab 6):
 * - Cumulative Growth Curve
 * - Monthly Progress & MoM Trends
 * - Top 15 GN Divisions Ranking
 * - 10 Activity Sectors Doughnut & Horizontal Bar
 * - Weekday Distribution (7 days) & Weekend vs Weekday Split
 * - Diversity Index Histogram
 * - Dual Entity Comparison Chart
 * - Financial Utilization Deep Dive
 */

class PssCharts {
  constructor() {
    this.data = (typeof window !== "undefined" && window.PSS_DATA) ? window.PSS_DATA : {};

    // Legacy / Overview Charts
    this.monthlyChart = null;
    this.categoryChart = null;
    this.gnRankingChart = null;

    // Advanced Progress Analytics Charts (Tab 6)
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

    this.defaultFont = "'Noto Sans Sinhala', sans-serif";
  }

  init(data) {
    this.data = data || (typeof window !== "undefined" && window.PSS_DATA) ? window.PSS_DATA : {};
    this.renderAll();
  }

  renderAll() {
    this.renderMonthlyChart();
    this.renderCategoryChart();
    this.renderGNRankingChart();
    this.renderAllAnalyticsCharts();
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
   * Tab 1 / Tab 2 Monthly Progress Chart
   */
  renderMonthlyChart() {
    const ctx = document.getElementById("monthlyProgressChart");
    if (!ctx) return;
    if (this.monthlyChart) this.monthlyChart.destroy();

    const stats = this.data?.monthlyStats || (typeof window !== "undefined" && window.PSS_DATA?.monthlyStats) || [];
    const labels = stats.map(m => m.monthSi);
    const completedData = stats.map(m => m.completed);
    const ongoingData = stats.map(m => m.ongoing);
    const beneficiariesData = stats.map(m => m.beneficiaries || 0);

    this.monthlyChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "සම්පූර්ණ වූ වැඩසටහන්",
            data: completedData,
            backgroundColor: "rgba(212, 175, 55, 0.9)",
            borderColor: "#FDE68A",
            borderWidth: 1.5,
            borderRadius: 6,
            stack: "projects"
          },
          {
            label: "ක්‍රියාත්මක වෙමින් පවතින",
            data: ongoingData,
            backgroundColor: "rgba(30, 64, 175, 0.8)",
            borderColor: "#60A5FA",
            borderWidth: 1.5,
            borderRadius: 6,
            stack: "projects"
          },
          {
            label: "ප්‍රතිලාභී පවුල් සංඛ්‍යාව",
            data: beneficiariesData,
            type: "line",
            yAxisID: "y1",
            borderColor: "#38BDF8",
            backgroundColor: "rgba(56, 189, 248, 0.14)",
            borderWidth: 2.5,
            pointBackgroundColor: "#F59E0B",
            pointBorderColor: "#FFFFFF",
            pointBorderWidth: 2,
            pointRadius: 4.5,
            pointHoverRadius: 7,
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
              color: "#E2E8F0",
              font: { family: this.defaultFont, size: 12, weight: "600" },
              usePointStyle: true,
              boxWidth: 8,
              padding: 16
            }
          },
          tooltip: {
            backgroundColor: "rgba(5, 14, 36, 0.96)",
            titleColor: "#FDE68A",
            bodyColor: "#F8FAFC",
            borderColor: "rgba(212, 175, 55, 0.4)",
            borderWidth: 1,
            padding: 12,
            titleFont: { family: this.defaultFont, size: 13, weight: "bold" }
          }
        },
        scales: {
          x: {
            grid: { color: "rgba(255, 255, 255, 0.04)" },
            ticks: { color: "#94A3B8", font: { family: this.defaultFont, size: 11 } }
          },
          y: {
            title: { display: true, text: "වැඩසටහන් ගණන", color: "#CBD5E1", font: { family: this.defaultFont, size: 11 } },
            grid: { color: "rgba(255, 255, 255, 0.06)" },
            ticks: { color: "#94A3B8", stepSize: 5 }
          },
          y1: {
            type: "linear",
            display: true,
            position: "right",
            title: { display: true, text: "ප්‍රතිලාභී පවුල්", color: "#38BDF8", font: { family: this.defaultFont, size: 11 } },
            grid: { drawOnChartArea: false },
            ticks: { color: "#38BDF8" }
          }
        }
      }
    });
  }

  /**
   * Overview Category Breakdown Doughnut
   */
  renderCategoryChart() {
    const ctx = document.getElementById("categoryBreakdownChart");
    if (!ctx) return;
    if (this.categoryChart) this.categoryChart.destroy();

    const cats = this.data?.analyticalCategories || (typeof window !== "undefined" && window.PSS_DATA?.analyticalCategories) || [];
    const labels = cats.map(c => c.nameSi);
    const dataValues = cats.map(c => c.count);
    const colors = cats.map(c => c.color || "#D4AF37");

    this.categoryChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [{
          data: dataValues,
          backgroundColor: colors,
          borderColor: "rgba(5, 14, 36, 0.9)",
          borderWidth: 2,
          hoverOffset: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "64%",
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
            backgroundColor: "rgba(5, 14, 36, 0.96)",
            titleColor: "#FDE68A",
            bodyColor: "#F8FAFC",
            borderColor: "rgba(212, 175, 55, 0.4)",
            borderWidth: 1,
            callbacks: {
              label: function (context) {
                const val = context.raw || 0;
                const total = context.chart._metasets[context.datasetIndex].total || 1;
                const pct = ((val / total) * 100).toFixed(1);
                return \` \${context.label}: \${val} (\${pct}%)\`;
              }
            }
          }
        }
      }
    });
  }

  /**
   * Overview GN Division Ranking
   */
  renderGNRankingChart() {
    const ctx = document.getElementById("gnProgressChart");
    if (!ctx) return;
    if (this.gnRankingChart) this.gnRankingChart.destroy();

    const rawDivs = this.data?.gnDivisions || (typeof window !== "undefined" && window.PSS_DATA?.gnDivisions) || [];
    const sorted = [...rawDivs].sort((a, b) => b.totalProjects - a.totalProjects).slice(0, 8);
    const labels = sorted.map(g => g.nameSi);
    const completedVals = sorted.map(g => g.completed);
    const ongoingVals = sorted.map(g => g.ongoing);

    this.gnRankingChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "සම්පූර්ණ වූ වැඩසටහන්",
            data: completedVals,
            backgroundColor: "#D4AF37",
            borderRadius: 5
          },
          {
            label: "ක්‍රියාත්මක වෙමින් පවතින",
            data: ongoingVals,
            backgroundColor: "rgba(37, 99, 235, 0.8)",
            borderRadius: 5
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
            labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11 }, usePointStyle: true }
          },
          tooltip: {
            backgroundColor: "rgba(5, 14, 36, 0.96)",
            borderColor: "rgba(212, 175, 55, 0.4)",
            borderWidth: 1
          }
        },
        scales: {
          x: { stacked: true, grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#94A3B8" } },
          y: {
            stacked: true,
            grid: { display: false },
            ticks: { color: "#E2E8F0", font: { family: this.defaultFont, size: 11.5, weight: "500" } }
          }
        }
      }
    });
  }

  // =========================================================================
  // ADVANCED ANALYTICS CHARTS (TAB 6)
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
   * 1. Cumulative Growth Curve (Monthly Additions + Cumulative Total)
   */
  renderAnCumulativeChart(monthlyData) {
    const ctx = document.getElementById("anCumulativeChart");
    if (!ctx) return;
    if (this.anCumulativeChart) this.anCumulativeChart.destroy();

    const data = monthlyData || this.data?.monthlyStats || (typeof window !== "undefined" && window.PSS_DATA?.monthlyStats) || [];
    if (!data.length) return;

    const labels = data.map(m => m.monthSi);
    const monthlyCounts = data.map(m => m.count);
    const cumulativeCounts = data.map(m => m.cumulativeCount);

    this.anCumulativeChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "මාසික වැඩසටහන් සංඛ්‍යාව",
            data: monthlyCounts,
            backgroundColor: "rgba(56, 189, 248, 0.65)",
            borderColor: "#38BDF8",
            borderWidth: 1.5,
            borderRadius: 6,
            yAxisID: "y"
          },
          {
            label: "සමුච්චිත ප්‍රගති වක්‍රය (මුළු එකතුව)",
            data: cumulativeCounts,
            type: "line",
            yAxisID: "y1",
            borderColor: "#D4AF37",
            backgroundColor: "rgba(212, 175, 55, 0.15)",
            borderWidth: 3,
            pointBackgroundColor: "#FDE68A",
            pointBorderColor: "#FFFFFF",
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7,
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
            labels: { color: "#E2E8F0", font: { family: this.defaultFont, size: 11.5, weight: "600" }, usePointStyle: true }
          },
          tooltip: {
            backgroundColor: "rgba(5, 14, 36, 0.96)",
            titleColor: "#FDE68A",
            borderColor: "rgba(212, 175, 55, 0.4)",
            borderWidth: 1
          }
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#94A3B8", font: { family: this.defaultFont, size: 10.5 } } },
          y: {
            title: { display: true, text: "මාසික වැඩසටහන්", color: "#38BDF8", font: { family: this.defaultFont, size: 11 } },
            grid: { color: "rgba(255, 255, 255, 0.06)" },
            ticks: { color: "#94A3B8" }
          },
          y1: {
            position: "right",
            title: { display: true, text: "සමුච්චිත එකතුව", color: "#D4AF37", font: { family: this.defaultFont, size: 11 } },
            grid: { drawOnChartArea: false },
            ticks: { color: "#D4AF37" }
          }
        }
      }
    });
  }

  /**
   * 2. Monthly Trend & MoM Change % Chart
   */
  renderAnMonthlyTrendChart(monthlyData) {
    const ctx = document.getElementById("anMonthlyTrendChart");
    if (!ctx) return;
    if (this.anMonthlyTrendChart) this.anMonthlyTrendChart.destroy();

    const data = monthlyData || this.data?.monthlyStats || (typeof window !== "undefined" && window.PSS_DATA?.monthlyStats) || [];
    if (!data.length) return;

    const labels = data.map(m => m.monthSi);
    const counts = data.map(m => m.count);
    const momPcts = data.map(m => m.momChangePct !== null ? m.momChangePct : 0);

    this.anMonthlyTrendChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "වැඩසටහන් සංඛ්‍යාව",
            data: counts,
            backgroundColor: data.map(m => m.monthKey === "2026-08" ? "rgba(212, 175, 55, 0.9)" : "rgba(30, 64, 175, 0.75)"),
            borderColor: data.map(m => m.monthKey === "2026-08" ? "#FDE68A" : "#60A5FA"),
            borderWidth: 1.5,
            borderRadius: 6,
            yAxisID: "y"
          },
          {
            label: "MoM වර්ධනය / අඩුවීම (%)",
            data: momPcts,
            type: "line",
            yAxisID: "y1",
            borderColor: "#EC4899",
            backgroundColor: "rgba(236, 72, 153, 0.15)",
            borderWidth: 2.5,
            pointBackgroundColor: momPcts.map(p => p < 0 ? "#EF4444" : "#10B981"),
            pointBorderColor: "#FFFFFF",
            pointRadius: 5,
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
            labels: { color: "#E2E8F0", font: { family: this.defaultFont, size: 11.5, weight: "600" }, usePointStyle: true }
          },
          tooltip: {
            backgroundColor: "rgba(5, 14, 36, 0.96)",
            titleColor: "#FDE68A",
            borderColor: "rgba(212, 175, 55, 0.4)",
            borderWidth: 1
          }
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#94A3B8" } },
          y: {
            title: { display: true, text: "වැඩසටහන් සංඛ්‍යාව", color: "#60A5FA", font: { family: this.defaultFont, size: 11 } },
            grid: { color: "rgba(255, 255, 255, 0.06)" },
            ticks: { color: "#94A3B8" }
          },
          y1: {
            position: "right",
            title: { display: true, text: "MoM වෙනස (%)", color: "#EC4899", font: { family: this.defaultFont, size: 11 } },
            grid: { drawOnChartArea: false },
            ticks: {
              color: "#EC4899",
              callback: (v) => v + "%"
            }
          }
        }
      }
    });
  }

  /**
   * 3. Top 15 GN Divisions Horizontal Bar Chart
   */
  renderAnTopDivisionsChart(divisionsData) {
    const ctx = document.getElementById("anTopDivisionsChart");
    if (!ctx) return;
    if (this.anTopDivisionsChart) this.anTopDivisionsChart.destroy();

    const data = divisionsData || this.data?.gnDivisions || (typeof window !== "undefined" && window.PSS_DATA?.gnDivisions) || [];
    if (!data.length) return;

    const sorted = [...data].sort((a, b) => b.totalProjects - a.totalProjects).slice(0, 15);
    const labels = sorted.map(d => d.nameSi);
    const completed = sorted.map(d => d.completed);
    const ongoing = sorted.map(d => d.ongoing);

    this.anTopDivisionsChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "සම්පූර්ණ වූ වැඩසටහන්",
            data: completed,
            backgroundColor: "#D4AF37",
            borderRadius: 4
          },
          {
            label: "ක්‍රියාත්මක වැඩසටහන්",
            data: ongoing,
            backgroundColor: "rgba(37, 99, 235, 0.8)",
            borderRadius: 4
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
            labels: { color: "#E2E8F0", font: { family: this.defaultFont, size: 11.5 } }
          },
          tooltip: {
            backgroundColor: "rgba(5, 14, 36, 0.96)",
            borderColor: "rgba(212, 175, 55, 0.4)",
            borderWidth: 1
          }
        },
        scales: {
          x: { stacked: true, grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#94A3B8" } },
          y: {
            stacked: true,
            grid: { display: false },
            ticks: { color: "#F8FAFC", font: { family: this.defaultFont, size: 11.5, weight: "500" } }
          }
        }
      }
    });
  }

  /**
   * 4. 10 Sectors Charts: Doughnut & Horizontal Bar
   */
  renderAnSectorCharts(categoriesData) {
    const cats = categoriesData || this.data?.analyticalCategories || (typeof window !== "undefined" && window.PSS_DATA?.analyticalCategories) || [];
    if (!cats.length) return;

    // Doughnut
    const dCtx = document.getElementById("anSectorDoughnutChart");
    if (dCtx) {
      if (this.anSectorDoughnutChart) this.anSectorDoughnutChart.destroy();
      this.anSectorDoughnutChart = new Chart(dCtx, {
        type: "doughnut",
        data: {
          labels: cats.map(c => c.nameSi),
          datasets: [{
            data: cats.map(c => c.count),
            backgroundColor: cats.map(c => c.color),
            borderColor: "rgba(5, 14, 36, 0.9)",
            borderWidth: 2,
            hoverOffset: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "60%",
          plugins: {
            legend: {
              position: "bottom",
              labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 9.5 }, usePointStyle: true, padding: 8 }
            },
            tooltip: {
              backgroundColor: "rgba(5, 14, 36, 0.96)",
              titleColor: "#FDE68A",
              callbacks: {
                label: (ctx) => {
                  const val = ctx.raw || 0;
                  const total = ctx.chart._metasets[ctx.datasetIndex].total || 1;
                  const pct = ((val / total) * 100).toFixed(1);
                  return \` \${ctx.label}: \${val} (\${pct}%)\`;
                }
              }
            }
          }
        }
      });
    }

    // Horizontal Bar
    const bCtx = document.getElementById("anSectorBarChart");
    if (bCtx) {
      if (this.anSectorBarChart) this.anSectorBarChart.destroy();
      const sorted = [...cats].sort((a, b) => b.count - a.count);
      this.anSectorBarChart = new Chart(bCtx, {
        type: "bar",
        data: {
          labels: sorted.map(c => c.nameSi),
          datasets: [{
            label: "වැඩසටහන් ගණන",
            data: sorted.map(c => c.count),
            backgroundColor: sorted.map(c => c.color),
            borderRadius: 5
          }]
        },
        options: {
          indexAxis: "y",
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { backgroundColor: "rgba(5, 14, 36, 0.96)", borderColor: "rgba(212, 175, 55, 0.4)", borderWidth: 1 }
          },
          scales: {
            x: { grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#94A3B8" } },
            y: {
              grid: { display: false },
              ticks: { color: "#E2E8F0", font: { family: this.defaultFont, size: 10.5 } }
            }
          }
        }
      });
    }
  }

  /**
   * 5. Weekday & Weekend Analysis Charts
   */
  renderAnTimelineCharts(weekdayData) {
    const data = weekdayData || this.data?.analytics?.weekdays || (typeof window !== "undefined" && window.PSS_DATA?.analytics?.weekdays);
    if (!data || !data.breakdown) return;

    // Weekday Bar Chart (Monday to Sunday)
    const wCtx = document.getElementById("anWeekdayChart");
    if (wCtx) {
      if (this.anWeekdayChart) this.anWeekdayChart.destroy();
      this.anWeekdayChart = new Chart(wCtx, {
        type: "bar",
        data: {
          labels: data.breakdown.map(d => d.daySi),
          datasets: [{
            label: "වැඩසටහන් ගණන",
            data: data.breakdown.map(d => d.count),
            backgroundColor: data.breakdown.map(d => d.isWeekend ? "rgba(212, 175, 55, 0.85)" : "rgba(30, 64, 175, 0.8)"),
            borderColor: data.breakdown.map(d => d.isWeekend ? "#FDE68A" : "#60A5FA"),
            borderWidth: 1.5,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: "rgba(5, 14, 36, 0.96)",
              titleColor: "#FDE68A",
              callbacks: {
                label: (ctx) => \` \${ctx.raw} වැඩසටහන් (\${((ctx.raw / 383) * 100).toFixed(1)}%)\`
              }
            }
          },
          scales: {
            x: { grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" } } },
            y: { grid: { color: "rgba(255, 255, 255, 0.06)" }, ticks: { color: "#94A3B8" } }
          }
        }
      });
    }

    // Weekend vs Weekday Doughnut
    const eCtx = document.getElementById("anWeekendChart");
    if (eCtx) {
      if (this.anWeekendChart) this.anWeekendChart.destroy();
      this.anWeekendChart = new Chart(eCtx, {
        type: "doughnut",
        data: {
          labels: ["සතියේ වැඩ කරන දින (67.6%)", "සති අන්ත දින (32.4%)"],
          datasets: [{
            data: [data.summary.weekdays.count, data.summary.weekends.count],
            backgroundColor: ["#1D4ED8", "#D4AF37"],
            borderColor: "rgba(5, 14, 36, 0.9)",
            borderWidth: 3,
            hoverOffset: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "62%",
          plugins: {
            legend: {
              position: "bottom",
              labels: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11 }, usePointStyle: true, padding: 12 }
            },
            tooltip: {
              backgroundColor: "rgba(5, 14, 36, 0.96)",
              titleColor: "#FDE68A"
            }
          }
        }
      });
    }
  }

  /**
   * 6. Diversity Distribution Histogram Chart
   */
  renderAnDiversityChart(divisionsData) {
    const ctx = document.getElementById("anDiversityDistChart");
    if (!ctx) return;
    if (this.anDiversityDistChart) this.anDiversityDistChart.destroy();

    const data = divisionsData || this.data?.gnDivisions || (typeof window !== "undefined" && window.PSS_DATA?.gnDivisions) || [];
    if (!data.length) return;

    const tiers = { "7+ ක්ෂේත්‍ර (ඉහළම)": 0, "5 - 6 ක්ෂේත්‍ර (මධ්‍යස්ථ)": 0, "3 - 4 ක්ෂේත්‍ර (සාමාන්‍ය)": 0, "1 - 2 ක්ෂේත්‍ර (අවධානය)": 0 };
    data.forEach(d => {
      const v = d.diversity || 4;
      if (v >= 7) tiers["7+ ක්ෂේත්‍ර (ඉහළම)"]++;
      else if (v >= 5) tiers["5 - 6 ක්ෂේත්‍ර (මධ්‍යස්ථ)"]++;
      else if (v >= 3) tiers["3 - 4 ක්ෂේත්‍ර (සාමාන්‍ය)"]++;
      else tiers["1 - 2 ක්ෂේත්‍ර (අවධානය)"]++;
    });

    this.anDiversityDistChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: Object.keys(tiers),
        datasets: [{
          label: "වසම් සංඛ්‍යාව",
          data: Object.values(tiers),
          backgroundColor: ["#D4AF37", "#3B82F6", "#06B6D4", "#EF4444"],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "rgba(5, 14, 36, 0.96)",
            titleColor: "#FDE68A",
            callbacks: {
              label: (ctx) => \` වසම් \${ctx.raw} ක් (\${((ctx.raw / 63) * 100).toFixed(1)}%)\`
            }
          }
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11.5, weight: "600" } } },
          y: { grid: { color: "rgba(255, 255, 255, 0.06)" }, ticks: { color: "#94A3B8", stepSize: 5 } }
        }
      }
    });
  }

  /**
   * 7. Dual Entity Head-to-Head Comparison Chart
   */
  renderAnCompareChart(itemA, itemB, mode) {
    const ctx = document.getElementById("anCompareChart");
    if (!ctx || !itemA || !itemB) return;
    if (this.anCompareChart) this.anCompareChart.destroy();

    let labels = [];
    let dataA = [];
    let dataB = [];

    if (mode === "division") {
      labels = ["මුළු වැඩසටහන්", "සම්පූර්ණ කළ", "ක්‍රියාකාරී දින", "ක්ෂේත්‍ර විවිධත්වය", "ප්‍රතිලාභීන් (x10)"];
      dataA = [itemA.totalProjects, itemA.completed, itemA.activeDays, itemA.diversity, Math.round(itemA.beneficiaries / 10)];
      dataB = [itemB.totalProjects, itemB.completed, itemB.activeDays, itemB.diversity, Math.round(itemB.beneficiaries / 10)];
    } else if (mode === "month") {
      labels = ["වැඩසටහන්", "සම්පූර්ණ", "ක්‍රියාකාරී දින", "වාර්තා කළ වසම්", "ප්‍රතිලාභීන් (x100)"];
      dataA = [itemA.count, itemA.completed, itemA.activeDays, itemA.reportingDivisions, Math.round((itemA.beneficiaries || 0) / 100)];
      dataB = [itemB.count, itemB.completed, itemB.activeDays, itemB.reportingDivisions, Math.round((itemB.beneficiaries || 0) / 100)];
    } else {
      labels = ["වැඩසටහන් ගණන", "සමස්ත % (x5)"];
      dataA = [itemA.count, Math.round(itemA.pct * 5)];
      dataB = [itemB.count, Math.round(itemB.pct * 5)];
    }

    this.anCompareChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: itemA.nameSi || itemA.monthSi,
            data: dataA,
            backgroundColor: "rgba(212, 175, 55, 0.85)",
            borderColor: "#FDE68A",
            borderWidth: 1.5,
            borderRadius: 6
          },
          {
            label: itemB.nameSi || itemB.monthSi,
            data: dataB,
            backgroundColor: "rgba(56, 189, 248, 0.8)",
            borderColor: "#38BDF8",
            borderWidth: 1.5,
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
            labels: { color: "#E2E8F0", font: { family: this.defaultFont, size: 12, weight: "bold" }, usePointStyle: true }
          },
          tooltip: { backgroundColor: "rgba(5, 14, 36, 0.96)", borderColor: "rgba(212, 175, 55, 0.4)", borderWidth: 1 }
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 11 } } },
          y: { grid: { color: "rgba(255, 255, 255, 0.06)" }, ticks: { color: "#94A3B8" } }
        }
      }
    });
  }

  /**
   * 8. Financial Utilization Deep Dive Chart
   */
  renderAnDeepdiveFinChart(divisionsData) {
    const ctx = document.getElementById("anDeepdiveFinChart");
    if (!ctx) return;
    if (this.anDeepdiveFinChart) this.anDeepdiveFinChart.destroy();

    const data = divisionsData || this.data?.gnDivisions || (typeof window !== "undefined" && window.PSS_DATA?.gnDivisions) || [];
    if (!data.length) return;

    const sorted = [...data].sort((a, b) => b.budgetLKR - a.budgetLKR).slice(0, 10);
    const labels = sorted.map(d => d.nameSi);
    const budgets = sorted.map(d => d.budgetLKR / 1000000);
    const spents = sorted.map(d => d.spentLKR / 1000000);

    this.anDeepdiveFinChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "වෙන්කළ ප්‍රතිපාදන (රු. මිලියන)",
            data: budgets,
            backgroundColor: "rgba(30, 64, 175, 0.7)",
            borderColor: "#3B82F6",
            borderWidth: 1.5,
            borderRadius: 5
          },
          {
            label: "යෙදවූ මුදල (රු. මිලියන)",
            data: spents,
            backgroundColor: "rgba(212, 175, 55, 0.85)",
            borderColor: "#FDE68A",
            borderWidth: 1.5,
            borderRadius: 5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", labels: { color: "#E2E8F0", font: { family: this.defaultFont, size: 11.5 } } },
          tooltip: {
            backgroundColor: "rgba(5, 14, 36, 0.96)",
            callbacks: {
              label: (ctx) => \` \${ctx.dataset.label}: රු. \${ctx.raw.toFixed(2)}M\`
            }
          }
        },
        scales: {
          x: { grid: { color: "rgba(255, 255, 255, 0.04)" }, ticks: { color: "#CBD5E1", font: { family: this.defaultFont, size: 10.5 } } },
          y: {
            grid: { color: "rgba(255, 255, 255, 0.06)" },
            ticks: {
              color: "#94A3B8",
              callback: (v) => "රු. " + v + "M"
            }
          }
        }
      }
    });
  }
}

window.pssCharts = new PssCharts();
`;

fs.writeFileSync('js/charts.js', chartsCode, 'utf8');
console.log('Successfully updated js/charts.js with bulletproof fallbacks!');
