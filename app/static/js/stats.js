// LOAD PUBLIC STATS
async function loadStats() {
  try {
    const response = await fetch('/public/stats');
    const stats = await response.json();

    document.getElementById("total-farmers").textContent =
      stats.total_farmers.toLocaleString();
    document.getElementById("active-crops").textContent =
      stats.active_crops.toLocaleString();
    document.getElementById("total-harvest").textContent =
      stats.total_harvest.toLocaleString() + ' kg';
    document.getElementById("total-crops").textContent =
      stats.total_crops.toLocaleString();

  } catch (err) {
    console.error('Failed to load stats:', err);
  }
}

//LOAD TOP CROPS
async function loadTopCrops() {
  try {
    const response = await fetch('/public/top-crops');
    const crops = await response.json();
    const container = document.getElementById("top-crops-list");

    if (crops.length === 0) {
      container.innerHTML = '<p class="empty-state">No data yet.</p>';
      return;
    }

    const medals = [];
    container.innerHTML = crops.map((crop, index) => `
        <div class="top-crop-item">
          <span class="crop-medal">${medals[index]}</span>
          <div class="crop-details">
              <strong>${crop.name}</strong>
              <p>${crop.count} farmers
                 ${crop.total_harvest.toLocaleString()} kg harvested</p>
          </div>
          <div class="crop-price">
              TZS ${crop.avg_price.toLocaleString()}/kg
          </div>
        </div>
    `).join('');
  } catch (err) {
      console.error('Failed to load top crops:', err);
  }
}

// LOAD PRICE TRENDS CHART
async function loadPriceTrends() {
  try {
    const response = await fetch('/public/price-trends');
    const data = await response.json();

    if (data.length === 0) {
      document.getElementById("price-chart").parentElement.innerHTML =
        <h3> Price Trends</h3><p class="empty-state">No price history yet. Record harvests to see trends.</p>';
      return;
    }

    // Group by crop name
    const crops = {};
    data.forEach(item =>{
      if (!crops[item.crop_name]) crops[item.crop_name] = [];
      crops[item.crop_name].push({ x: item.date, y: item.price });
    });

    const colors = ['#2d7a4f', '#f6ad55', '#fc8181', '#63b3ed', '#9f7aea'];
    const datasets = Object.keys(crops).slice(0, 5).map((nam, i) => ({
      label: name,
      data: crops[name],
      borderColor: colors[i],
      backgroundColor: colors[i] + '20',
      tension: 0.4,
      fill: false
    }));
    const ctx = document.getElementById('price-chart').getContenxt('2d');
    new Chart(ctx, {
      type: 'line',
      data: { datasets },
      options: {
        responsive: true,
        parsing: { xAxisKey: 'x', yAxisKey: 'y' },
        plugins: {
          legend: { position: 'bottom' }
        },
        scales: {
          x: { type: 'category' },
          y: {
            beginAtZero: false,
            ticks: {
              callback: value => 'TZS ' + value.toLocaleString()
            }
          }
        }
      }
    });

  } catch (err) {
    console.error('Failed to load price trends:', err);
  }
}

// LOAD REGIONS
async function loadRegions() {
  try {
    const response = await fetch('/public/regions');
    const regions = await response.json();
    const container = document.getElementById("regions-list");

    if (regions.length === 0) {
      container.innerHTML = '<p class="empty-state">No regional data yet.</p>';
      return;
    }

    container.innerHTML = regions.map(region => `
        <div class="region-card">
            <h4> ${region.region}</h4>
            <p>${region.total_harvest.toLocaleString()} kg harvested</p>
        </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load regions:', err);
  }
}

// LOAD NEW
async function loadNews() {
  try {
    const response = await fetch('/public/news');
    const news = document.getElementById("news-list");

    if (news.length === 0) {
      container.innerHTML = '<p class="empty-state">No updates yet.</p>';
      return;
    }

    container.innerHTML = news.map(item => `
        <div class="news-item">
            <div class="news-meta">
                <span class="news-author"> ${item.author}</span>
                <span class="news-date">${new Date(item.create_at)
                  .toLocaleDateString('en-TZ', {
                    year: 'numeric', month: 'long', day: 'numeric'
                  })})</span>
            </div>
            <h4 class="news-title">${item.title}</h4>
            <p class="new-content">${item.content}</p>
          </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load news:', err);
  }
}

//RUN ALL
loadStats();
loadTopCrops();
loadPriceTrends();
loadRegions();
loadNews();
