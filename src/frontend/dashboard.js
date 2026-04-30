// Utilidades globales: selector DOM y formateador numerico.
const $ = id => document.getElementById(id);
const fmt = (n, dec = 0, prefix = '') =>
  prefix + n.toLocaleString('es-ES', { minimumFractionDigits: dec, maximumFractionDigits: dec });

const AMBER = '#f5a623';
const MUTED = '#7a8088';
const BORDER = '#2a2d32';
const BLUE = '#5b9cf6';
const RED = '#e05c5c';
const CAT_COLORS = [AMBER, '#5b9cf6', '#3dd68c', '#e05c5c', '#a78bfa', '#f472b6'];

const baseOptions = () => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  animation: { duration: 800 }
});

// Punto de entrada. Obtiene datos del backend y dispara el renderizado.
async function init() {
  try {
    // Ruta relativa: Nginx reescribe /api/* hacia el backend interno.
    const response = await fetch('/api/dashboard');

    // Captura errores HTTP (4xx, 5xx) antes de parsear el cuerpo.
    if (!response.ok) {
      throw new Error(`Error HTTP ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();

    // Valida que la capa de negocio haya resuelto correctamente.
    if (result.status !== "success") {
      throw new Error("Error en el backend: " + (result.message || "respuesta inesperada"));
    }

    renderDashboard(result);

  } catch (error) {
    console.error("Error en init():", error);
    showError(error.message);
  }
}

function renderDashboard(data) {
  $('ts').textContent = new Date().toLocaleString('es-ES', {
    day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  // Renderiza cada modulo solo si el dato esta presente en la respuesta.
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
  // Renderiza modulos opcionales si su funcion esta disponible en el scope.
  if (data.dim_context_summary && typeof buildClimate === 'function') buildClimate(data.dim_context_summary);
  if (data.waste_risk && typeof buildWasteChart === 'function') {
    buildWasteChart(data.waste_risk);
    buildWasteTable(data.waste_risk);
  }
  if (data.ingredient_demand && typeof buildIngChart === 'function') {
    buildIngChart(data.ingredient_demand);
    buildIngTable(data.ingredient_demand);
  }

  // Oculta el overlay con transicion de opacidad.
  const loader = $('loading');
  loader.style.opacity = '0';
  setTimeout(() => loader.style.display = 'none', 400);
}

// Reemplaza el overlay de carga con un panel de error visible.
function showError(msg) {
  const loader = $('loading');
  loader.style.opacity = '1';
  loader.style.display = 'flex';
  loader.innerHTML = `
    <div style="
      background:#1c1e21;
      border:1px solid #e05c5c;
      border-radius:8px;
      padding:32px 40px;
      max-width:480px;
      text-align:center;
      font-family:'Space Mono',monospace;
    ">
      <div style="font-size:28px;margin-bottom:16px;">&#9888;</div>
      <div style="color:#e05c5c;font-size:13px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px;">
        Error de conexion
      </div>
      <div style="color:#e8e9ea;font-size:12px;line-height:1.6;margin-bottom:20px;">
        ${msg}
      </div>
      <div style="color:#7a8088;font-size:11px;">
        Comprueba que el backend esta activo y vuelve a cargar la pagina.
      </div>
    </div>
  `;
}

// Navegacion por pestanas: activa seccion y tab correspondiente.
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    tab.classList.add('active');
    $('tab-' + tab.dataset.tab).classList.add('active');
  });
});


// Segundo registro del listener de tabs (bloque heredado).
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    tab.classList.add('active');
    $('tab-' + tab.dataset.tab).classList.add('active');
  });
});

// Rellena los 4 indicadores clave en el DOM.
function buildKPIs(k) {
  $('kpi-revenue').textContent = fmt(k.total_revenue, 0, '') + ' €';
  $('kpi-tickets').textContent = fmt(k.total_tickets);
  $('kpi-avg').textContent = fmt(k.avg_ticket, 2) + ' €';
  $('kpi-days').textContent = k.days_analyzed;
}

// Grafico de linea con ingresos diarios muestreados (1 de cada 3).
function buildRevenueChart(series) {
  // Reduce densidad visual mostrando 1 punto de cada 3.
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

// Grafico de barras horizontales por categoria de plato.
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

// Renderiza resumen climatico en los 3 bloques del grid.
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

// Grafico de barras con ranking de platos por unidades vendidas.
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

// Grafico de area con degradado para la vista detallada de ingresos.
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

// Grafico de anillo con distribucion de ventas por categoria.
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

// Tabla de ranking de platos con barra de proporcion relativa.
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

// Grafico de barras horizontales con cantidades predichas por ingrediente.
function buildPredChart(preds) {
  // Cortamos el array para quedarnos solo con los 15 primeros
  const topPreds = preds.slice(0, 15);

  new Chart($('predChart'), {
    type: 'bar',
    data: {
      labels: topPreds.map(p => p.ingrediente),
      datasets: [
        {
          label: 'Cantidad predicha',
          data: topPreds.map(p => p.kg_predicho), 
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
        legend: { display: false }
      },
      scales: {
        x: { ticks: { color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
        y: { ticks: { color: MUTED, font: { size: 11 } }, grid: { display: false } },
      }
    }
  });
}

// Tabla de predicciones ML: cantidad predicha e intervalo de confianza.
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

// Grafico comparativo: cantidad predicha vs historico semanal.
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

// Tabla de riesgo de desperdicio con nivel de alerta por ingrediente.
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

// Grafico de barras con demanda agregada de ingredientes.
function buildIngChart(ing) {
  new Chart($('ingChart'), {
    type: 'bar',
    data: {
      labels: ing.map(i => i.ingrediente),
      datasets: [{
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
        x: { ticks: { color: MUTED, font: { size: 10 } }, grid: { color: BORDER } },
        y: { ticks: { color: MUTED, font: { size: 11 } }, grid: { display: false } },
      }
    }
  });
}

// ── TABLA DE DEMANDA DE INGREDIENTES ──────────────────────────────────────────
function buildIngTable(ing) {
  const tbody = $('ingTable').querySelector('tbody');

  tbody.innerHTML = ing.map((item, i) => `
    <tr>
      <td class="mono" style="color:${MUTED}">${String(i + 1).padStart(2, '0')}</td>
      <td>${item.ingrediente}</td>
      <td class="mono" style="text-align: center; color:${AMBER}">${fmt(item.total_valor || 0, 1)} ${item.unidad || ''}</td>
    </tr>
  `).join('');
}
// Arranque de la aplicacion.
init();