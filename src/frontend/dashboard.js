// ── UTILITIES ─────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const fmt = (n, dec = 0, prefix = '') =>
  prefix + n.toLocaleString('es-ES', { minimumFractionDigits: dec, maximumFractionDigits: dec });

const AMBER = '#f5a623';
const MUTED = '#7a8088';
const BORDER = '#2a2d32';
const BLUE = '#5b9cf6';
const RED = '#e05c5c';  // <--- ¡AÑADE ESTA LÍNEA!
const CAT_COLORS = [AMBER, '#5b9cf6', '#3dd68c', '#e05c5c', '#a78bfa', '#f472b6'];

const baseOptions = () => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  animation: { duration: 800 }
});

// ── INICIALIZACIÓN (SOLO REAL) ────────────────────────────────────────────────
async function init() {
  let result;

  // FASE 1: Conexión
  try {
    // Asegúrate de usar localhost si en el navegador usas localhost
    const response = await fetch('http://localhost:8000/api/dashboard');
    result = await response.json();
  } catch (error) {
    console.error("❌ Error de red/CORS:", error);
    showError("Fallo de red: El navegador bloquea la conexión (CORS).");
    return; // Paramos aquí
  }

  // FASE 2: Dibujado
  try {
    if (result.status === "success") {
      console.log("✅ Datos listos para dibujar:", result);
      renderDashboard(result);
    } else {
      showError("Error en la Base de Datos: " + result.message);
    }
  } catch (error) {
    console.error("❌ Error dibujando gráficas:", error);
    showError("Datos recibidos, pero falló el código al dibujar. Pulsa F12.");
  }
}

function renderDashboard(data) {
  $('ts').textContent = new Date().toLocaleString('es-ES', {
    day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  // ¡DESBLOQUEAMOS EL PODER TOTAL! 🎉
  if (data.next_week_predictions) {
    buildPredChart(data.next_week_predictions);
    buildPredTable(data.next_week_predictions);
  }
  if (data.kpis) buildKPIs(data.kpis);
  if (data.revenue_series) {
    buildRevenueChart(data.revenue_series);
    buildRevenueArea(data.revenue_series);
  }
  if (data.sales_by_category) {
    buildCatChart(data.sales_by_category);
    buildCatDoughnut(data.sales_by_category);
  }
  if (data.top_dishes) {
    buildTopDishChart(data.top_dishes);
    buildTopDishTable(data.top_dishes);
  }
  // Funciones extra (asegúrate de que las tenías definidas abajo, si no, puedes quitarlas)
  if (data.dim_context_summary && typeof buildClimate === 'function') buildClimate(data.dim_context_summary);
  if (data.waste_risk && typeof buildWasteChart === 'function') {
    buildWasteChart(data.waste_risk);
    buildWasteTable(data.waste_risk);
  }
  if (data.ingredient_demand && typeof buildIngChart === 'function') {
    buildIngChart(data.ingredient_demand);
    buildIngTable(data.ingredient_demand);
  }

  // Quitamos el loader
  const loader = $('loading');
  loader.style.opacity = '0';
  setTimeout(() => loader.style.display = 'none', 400);
}

function showError(msg) {
  const loader = $('loading');
  loader.innerHTML = `<div class="loader-text" style="color:#e05c5c">ERROR: ${msg}</div>`;
}

// ── TABS (Esto estaba fuera de sitio) ────────────────────────────────────────
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    tab.classList.add('active');
    $('tab-' + tab.dataset.tab).classList.add('active');
  });
});


// ── TABS ──────────────────────────────────────────────────────────────────────
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    tab.classList.add('active');
    $('tab-' + tab.dataset.tab).classList.add('active');
  });
});

// ── KPIs ──────────────────────────────────────────────────────────────────────
function buildKPIs(k) {
  $('kpi-revenue').textContent = fmt(k.total_revenue, 0, '') + ' €';
  $('kpi-tickets').textContent = fmt(k.total_tickets);
  $('kpi-avg').textContent = fmt(k.avg_ticket, 2) + ' €';
  $('kpi-days').textContent = k.days_analyzed;
}

// ── REVENUE MINI CHART ────────────────────────────────────────────────────────
function buildRevenueChart(series) {
  // Sample every 3rd day for clarity
  const sampled = series.filter((_, i) => i % 3 === 0);
  new Chart($('revenueChart'), {
    type: 'line',
    data: {
      labels: sampled.map(d => d.fecha.slice(5)),
      datasets: [{
        data: sampled.map(d => d.revenue),
        borderColor: AMBER,
        backgroundColor: 'rgba(245,166,35,0.05)',
        borderWidth: 1.5,
        pointRadius: 0,
        tension: 0.4,
        fill: true,
      }]
    },
    options: {
      ...baseOptions(),
      scales: {
        x: { ticks: { maxTicksLimit: 6, color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
        y: { ticks: { color: MUTED, font: { size: 10 }, callback: v => v + '€' }, grid: { color: BORDER } },
      }
    }
  });
}

// ── CATEGORY BAR ─────────────────────────────────────────────────────────────
function buildCatChart(cats) {
  new Chart($('catChart'), {
    type: 'bar',
    data: {
      labels: cats.map(c => c.categoria),
      datasets: [{
        data: cats.map(c => c.unidades),
        backgroundColor: CAT_COLORS,
        borderRadius: 3,
        borderSkipped: false,
      }]
    },
    options: {
      ...baseOptions(),
      indexAxis: 'y',
      scales: {
        x: { ticks: { color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
        y: { ticks: { color: MUTED, font: { size: 10 } }, grid: { display: false } },
      }
    }
  });
}

// ── CLIMATE ───────────────────────────────────────────────────────────────────
function buildClimate(ctx) {
  $('climateGrid').innerHTML = `
    <div class="climate-item">
      <div class="climate-value">${ctx.avg_temp}°</div>
      <div class="climate-label">Temp. media</div>
    </div>
    <div class="climate-item">
      <div class="climate-value">${ctx.rainy_days}</div>
      <div class="climate-label">Días lluvia</div>
    </div>
    <div class="climate-item">
      <div class="climate-value">${ctx.holiday_days}</div>
      <div class="climate-label">Festivos</div>
    </div>
  `;
}

// ── TOP DISH CHART ────────────────────────────────────────────────────────────
function buildTopDishChart(dishes) {
  new Chart($('topDishChart'), {
    type: 'bar',
    data: {
      labels: dishes.map(d => d.plato),
      datasets: [{
        data: dishes.map(d => d.unidades),
        backgroundColor: dishes.map((_, i) => i === 0 ? AMBER : 'rgba(245,166,35,0.35)'),
        borderRadius: 3,
        borderSkipped: false,
      }]
    },
    options: {
      ...baseOptions(),
      scales: {
        x: { ticks: { color: MUTED, font: { size: 11 } }, grid: { display: false } },
        y: { ticks: { color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
      }
    }
  });
}

// ── REVENUE AREA (ventas tab) ─────────────────────────────────────────────────
function buildRevenueArea(series) {
  new Chart($('revenueArea'), {
    type: 'line',
    data: {
      labels: series.map(d => d.fecha.slice(5)),
      datasets: [{
        data: series.map(d => d.revenue),
        borderColor: AMBER,
        backgroundColor: ctx => {
          const g = ctx.chart.ctx.createLinearGradient(0, 0, 0, 220);
          g.addColorStop(0, 'rgba(245,166,35,0.25)');
          g.addColorStop(1, 'rgba(245,166,35,0)');
          return g;
        },
        borderWidth: 1.5,
        pointRadius: 0,
        tension: 0.4,
        fill: true,
      }]
    },
    options: {
      ...baseOptions(),
      scales: {
        x: { ticks: { maxTicksLimit: 12, color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
        y: { ticks: { color: MUTED, font: { size: 10 }, callback: v => v + '€' }, grid: { color: BORDER } },
      }
    }
  });
}

// ── CATEGORY DOUGHNUT ─────────────────────────────────────────────────────────
function buildCatDoughnut(cats) {
  new Chart($('catDoughnut'), {
    type: 'doughnut',
    data: {
      labels: cats.map(c => c.categoria),
      datasets: [{
        data: cats.map(c => c.unidades),
        backgroundColor: CAT_COLORS,
        borderColor: '#141517',
        borderWidth: 3,
        hoverOffset: 6,
      }]
    },
    options: {
      ...baseOptions(),
      cutout: '68%',
      plugins: {
        legend: {
          display: true,
          position: 'right',
          labels: { color: '#e8e9ea', padding: 12, font: { size: 12 }, boxWidth: 12 }
        },
        tooltip: baseOptions().plugins.tooltip,
      }
    }
  });
}

// ── TOP DISH TABLE ────────────────────────────────────────────────────────────
function buildTopDishTable(dishes) {
  const max = dishes[0].unidades;
  const tbody = $('topDishTable').querySelector('tbody');
  tbody.innerHTML = dishes.map((d, i) => `
    <tr>
      <td class="mono" style="color:${MUTED}">${String(i + 1).padStart(2, '0')}</td>
      <td>${d.plato}</td>
      <td class="mono right">${fmt(d.unidades)}</td>
      <td>
        <div class="bar-cell">
          <div class="bar-bg">
            <div class="bar-fill" style="width:${(d.unidades / max * 100).toFixed(1)}%"></div>
          </div>
          <span class="mono" style="font-size:10px;color:${MUTED};width:38px;text-align:right">
            ${(d.unidades / max * 100).toFixed(0)}%
          </span>
        </div>
      </td>
    </tr>
  `).join('');
}

// ── PREDICTIONS CHART ─────────────────────────────────────────────────────────
function buildPredChart(preds) {
  new Chart($('predChart'), {
    type: 'bar',
    data: {
      labels: preds.map(p => p.ingrediente),
      datasets: [
        {
          label: 'Cantidad predicha',
          data: preds.map(p => p.kg_predicho), // Solo dibujamos el número real
          backgroundColor: 'rgba(245,166,35,0.7)',
          borderColor: AMBER,
          borderWidth: 1,
          borderRadius: 3,
        }
      ]
    },
    options: {
      ...baseOptions(),
      indexAxis: 'y',
      plugins: {
        ...baseOptions().plugins,
        legend: { display: false } // Quitamos la leyenda al haber solo 1 barra
      },
      scales: {
        // Quitamos el +'kg' porque ahora hay uds, litros, etc.
        x: { ticks: { color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
        y: { ticks: { color: MUTED, font: { size: 11 } }, grid: { display: false } },
      }
    }
  });
}

// ── PREDICTIONS TABLE ─────────────────────────────────────────────────────────
function buildPredTable(pred) {
  const tbody = $('predTable').querySelector('tbody');
  tbody.innerHTML = pred.map((item, i) => `
    <tr>
      <td>${item.ingrediente}</td>
      <td class="mono right" style="color:${AMBER}">
        ${fmt(item.kg_predicho, 2)} ${item.unidad || ''}  </td>
      <td class="mono right" style="color:${MUTED}; font-size:11px;">
        &plusmn; ${item.intervalo_confianza}
      </td>
    </tr>
  `).join('');
}

// ── WASTE CHART ───────────────────────────────────────────────────────────────
function buildWasteChart(waste) {
  const labels = waste.map(w => w.ingrediente);
  const pred = waste.map(w => w.kg_predicho);
  const hist = waste.map(w => w.kg_historico_semana);
  new Chart($('wasteChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Predicho (prox. semana)',
          data: pred,
          backgroundColor: waste.map(w =>
            w.riesgo === 'alto' ? 'rgba(224,92,92,0.7)' :
              w.riesgo === 'medio' ? 'rgba(245,166,35,0.7)' :
                'rgba(61,214,140,0.6)'
          ),
          borderRadius: 3,
        },
        {
          label: 'Histórico semanal',
          data: hist,
          backgroundColor: 'rgba(91,156,246,0.35)',
          borderColor: BLUE,
          borderWidth: 1,
          borderRadius: 3,
        }
      ]
    },
    options: {
      ...baseOptions(),
      plugins: {
        ...baseOptions().plugins,
        legend: {
          display: true,
          labels: { color: '#e8e9ea', font: { size: 11 }, boxWidth: 10 }
        }
      },
      scales: {
        x: { ticks: { color: MUTED, font: { size: 10 } }, grid: { display: false } },
        y: { ticks: { color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
      }
    }
  });
}

// ── WASTE TABLE ───────────────────────────────────────────────────────────────
function buildWasteTable(waste) {
  const tbody = $('wasteTable').querySelector('tbody');
  tbody.innerHTML = waste.map(w => {
    const devColor = w.desviacion_pct > 0 ? RED : GREEN;
    const sign = w.desviacion_pct > 0 ? '+' : '';
    return `
    <tr>
      <td>${w.ingrediente}</td>
      <td class="mono right">${fmt(w.kg_predicho, 2)} kg</td>
      <td class="mono right">${fmt(w.kg_historico_semana, 2)} kg</td>
      <td class="mono right" style="color:${devColor}">${sign}${fmt(w.desviacion_pct, 1)}%</td>
      <td class="center"><span class="risk risk-${w.riesgo}">${w.riesgo}</span></td>
    </tr>
  `}).join('');
}

// ── INGREDIENT CHART ──────────────────────────────────────────────────────────
function buildIngChart(ing) {
  new Chart($('ingChart'), {
    type: 'bar',
    data: {
      labels: ing.map(i => i.ingrediente),
      datasets: [{
        // OJO AQUÍ: Ahora lee total_valor, no kg_total
        data: ing.map(i => i.total_valor || 0),
        backgroundColor: ing.map((_, idx) => `hsla(${36 + idx * 18},90%,${60 - idx * 2}%,0.75)`),
        borderRadius: 3,
        borderSkipped: false,
      }]
    },
    options: {
      ...baseOptions(),
      indexAxis: 'y',
      scales: {
        // Hemos quitado el +'kg'
        x: { ticks: { color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
        y: { ticks: { color: MUTED, font: { size: 11 } }, grid: { display: false } },
      }
    }
  });
}

// ── INGREDIENT TABLE ──────────────────────────────────────────────────────────
function buildIngTable(ing) {
  const tbody = $('ingTable').querySelector('tbody');
  tbody.innerHTML = ing.map((item, i) => `
    <tr>
      <td class="mono" style="color:${MUTED}">${String(i + 1).padStart(2, '0')}</td>
      <td>${item.ingrediente}</td>
      <td class="mono right" style="color:${AMBER}">${fmt(item.total_valor || 0, 1)} ${item.unidad || ''}</td>
    </tr>
  `).join('');
}

// ── START ─────────────────────────────────────────────────────────────────────
init();