// URL de ton API FastAPI
const API_BASE = "http://127.0.0.1:8000";

// === Sélecteurs DOM ===
const arrSelect = document.getElementById("arr-select");
const yearSlider = document.getElementById("year-slider");
const yearDisplay = document.getElementById("year-display");
const yearPrev = document.getElementById("year-prev");
const yearNext = document.getElementById("year-next");

const kpiPrix = document.getElementById("kpi-prix");
const kpiVentes = document.getElementById("kpi-ventes");
const kpiLog = document.getElementById("kpi-log");

// === État global ===
let map;
let markersLayer;

let arrMeta = [];
let prixData = [];
let logData = [];
let delinquanceData = [];
let densiteData = [];
let vacanceData = [];
let typologieData = [];

let years = [];
let currentArr = null;
let currentYear = null;

let polygonsLayer;
let highlighted = null;
let geojsonData = null;

// === Palette 20 couleurs (1 couleur par arrondissement)
const ARR_COLORS = {
  1: "#3b82f6",
  2: "#6366f1",
  3: "#10b981",
  4: "#14b8a6",
  5: "#f59e0b",
  6: "#ef4444",
  7: "#8b5cf6",
  8: "#0ea5e9",
  9: "#22c55e",
  10: "#e11d48",
  11: "#f97316",
  12: "#0d9488",
  13: "#16a34a",
  14: "#7c3aed",
  15: "#ea580c",
  16: "#4f46e5",
  17: "#06b6d4",
  18: "#84cc16",
  19: "#d946ef",
  20: "#475569"
};

// === Utils simples pour foncer/saturer une couleur (hover/sélection)
function darken(color, amount = 0.2) {
  let c = parseInt(color.slice(1), 16);
  let r = (c >> 16) - 255 * amount;
  let g = ((c >> 8) & 0xff) - 255 * amount;
  let b = (c & 0xff) - 255 * amount;
  r = Math.max(0, r);
  g = Math.max(0, g);
  b = Math.max(0, b);
  return `rgb(${r},${g},${b})`;
}

function saturate(color, amount = 0.35) {
  let c = parseInt(color.slice(1), 16);
  let r = (c >> 16);
  let g = ((c >> 8) & 0xff);
  let b = (c & 0xff);
  r = Math.min(255, r + 255 * amount);
  g = Math.min(255, g + 255 * amount);
  b = Math.min(255, b + 255 * amount);
  return `rgb(${r},${g},${b})`;
}

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Erreur API ${res.status} sur ${url}`);
  return res.json();
}

function getArrLabel(code) {
  const meta = arrMeta.find(m => m.code === code);
  return meta ? meta.label : `Arrondissement ${code}`;
}

// === Popup avec tous les indicateurs
function openArrondissementPopup(arrCode, layer) {
  if (!layer) return;

  const center = layer.getBounds().getCenter();

  const prix = prixData.find(d => d.arrondissement === arrCode && d.annee === currentYear);
  const loge = logData.find(d => d.arrondissement === arrCode && d.annee === currentYear);
  const delin = delinquanceData.find(d => d.arrondissement === arrCode && d.annee === currentYear);
  const dens = densiteData.find(d => d.arrondissement === arrCode && d.annee === currentYear);
  const vac = vacanceData.find(d => d.arrondissement === arrCode && d.annee === currentYear);
  const typo = typologieData.find(d => d.arrondissement === arrCode && d.annee === currentYear);

  const prixTxt = prix ? `${Math.round(prix.prix_m2_median).toLocaleString("fr-FR")} €/m²` : "—";
  const ventesTxt = prix ? prix.nb_ventes.toLocaleString("fr-FR") : "—";
  const logTxt = loge ? loge.nb_programmes : "—";

  const densTxt = dens && !isNaN(dens.densite_hab_km2)
    ? `${Math.round(dens.densite_hab_km2).toLocaleString("fr-FR")} hab/km²`
    : "—";

  const delinTxt = delin && !isNaN(delin.score_delinquance)
    ? `${delin.score_delinquance.toFixed(1)}/10`
    : "—";

  const vacTxt = vac && !isNaN(vac.taux_vacance)
    ? `${vac.taux_vacance.toFixed(1)} %`
    : "—";

  const t1 = typo && !isNaN(typo.part_T1) ? `${typo.part_T1.toFixed(1)}%` : "—";
  const t2 = typo && !isNaN(typo.part_T2) ? `${typo.part_T2.toFixed(1)}%` : "—";
  const t3 = typo && !isNaN(typo.part_T3) ? `${typo.part_T3.toFixed(1)}%` : "—";
  const t4 = typo && !isNaN(typo.part_T4) ? `${typo.part_T4.toFixed(1)}%` : "—";

  const html = `
    <div class="popup-container">
      <div class="popup-title">${getArrLabel(arrCode)}</div>

      <div class="popup-section">
        <div>💶 <strong>Prix :</strong> ${prixTxt}</div>
        <div>📊 <strong>Ventes :</strong> ${ventesTxt}</div>
        <div>🏘️ <strong>Logements sociaux :</strong> ${logTxt}</div>
      </div>

      <div class="popup-section">
        <div class="popup-subtitle">📌 Indicateurs</div>
        <div>👥 Densité : ${densTxt}</div>
        <div>🚓 Délinquance : ${delinTxt}</div>
        <div>🏚️ Vacance : ${vacTxt}</div>
      </div>

      <div class="popup-section">
        <div class="popup-subtitle">🏷️ Typologie</div>
        <div>T1 : ${t1} &nbsp;|&nbsp; T2 : ${t2}</div>
        <div>T3 : ${t3} &nbsp;|&nbsp; T4+ : ${t4}</div>
      </div>

      <div class="popup-footer">Année ${currentYear}</div>
    </div>
  `;

  L.popup({
    closeButton: false,
    autoPan: true,
    offset: [0, -6],
    className: "custom-popup"
  })
    .setLatLng(center)
    .setContent(html)
    .openOn(map);
}


// === Chargement GeoJSON
async function loadGeoJSON() {
  const res = await fetch("arrondissements.geojson");
  geojsonData = await res.json();
}

// === Mise en avant du polygone sélectionné
function highlightPolygon(layer, arrCode) {
  if (highlighted) {
    polygonsLayer.resetStyle(highlighted);
  }

  const baseColor = ARR_COLORS[arrCode] || "#6b7280";

  layer.setStyle({
    fillColor: saturate(baseColor, 0.45),
    fillOpacity: 0.95,
    weight: 3,
    color: "#000000"
  });

  highlighted = layer;
}

// === Dessin des polygones
function drawPolygons() {
  if (!geojsonData) return;

  if (polygonsLayer) map.removeLayer(polygonsLayer);

  polygonsLayer = L.geoJSON(geojsonData, {
    renderer: L.svg(),

    style: (feature) => {
      const code = parseInt(feature.properties.c_ar || feature.properties.code);
      return {
        fillColor: ARR_COLORS[code] || "#9ca3af",
        fillOpacity: 0.7,
        color: "#ffffff",
        weight: 1
      };
    },

    onEachFeature: (feature, layer) => {
      const arrCode = parseInt(feature.properties.c_ar || feature.properties.code);

      // HOVER
      layer.on("mouseover", () => {
        if (layer !== highlighted) {
          layer.setStyle({
            fillColor: darken(ARR_COLORS[arrCode] || "#9ca3af", 0.15),
            fillOpacity: 0.85,
            weight: 2
          });
        }
        openArrondissementPopup(arrCode, layer);
      });

      layer.on("mouseout", () => {
        if (layer !== highlighted) {
          polygonsLayer.resetStyle(layer);
        }
      });

      // CLICK
      layer.on("click", () => {
        currentArr = arrCode;
        arrSelect.value = String(arrCode);
        highlightPolygon(layer, arrCode);
        updateAll(false); // on ne redessine pas les polygones ici
        openArrondissementPopup(arrCode, layer);
      });
    }
  });

  polygonsLayer.addTo(map);
}

// === Leaflet init
function initMap() {
  map = L.map("map", {
    preferCanvas: false,
    minZoom: 12,     // 🔒 empêche de trop dézoomer
    maxZoom: 18,     // 🔒 limite le zoom maximum
    zoomControl: true
  }).setView([48.8566, 2.3522], 13); // zoom centré sur Paris

  // Fond de carte
  L.tileLayer('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=', {
    minZoom: 12,
    maxZoom: 18
}).addTo(map);


  // 🔒 Empêcher la carte de sortir de Paris
  const parisBounds = L.latLngBounds(
    [48.815, 2.22], // Sud-Ouest de Paris
    [48.90, 2.42]   // Nord-Est de Paris
  );
  map.setMaxBounds(parisBounds);
  map.setMinZoom(12);

  markersLayer = L.layerGroup().addTo(map);
}

// On n'utilise plus les markers
function updateMarkers() {
  return;
}

// === UI & KPIs
function updateYearUI() {
  if (!currentYear) {
    yearDisplay.textContent = "-";
    return;
  }
  yearDisplay.textContent = currentYear;
  yearSlider.value = currentYear;

  const idx = years.indexOf(currentYear);
  yearPrev.disabled = idx <= 0;
  yearNext.disabled = idx >= years.length - 1;
}

function updateKPIs() {
  if (!currentArr || !currentYear) {
    kpiPrix.textContent = "-";
    kpiVentes.textContent = "Nombre de ventes : -";
    kpiLog.textContent = "-";
    return;
  }

  const prix = prixData.find(d => d.arrondissement === currentArr && d.annee === currentYear);
  const loge = logData.find(d => d.arrondissement === currentArr && d.annee === currentYear);
  const delin = delinquanceData.find(d => d.arrondissement === currentArr && d.annee === currentYear);
  const dens = densiteData.find(d => d.arrondissement === currentArr && d.annee === currentYear);
  const vac = vacanceData.find(d => d.arrondissement === currentArr && d.annee === currentYear);

  if (prix) {
    kpiPrix.textContent =
      Math.round(prix.prix_m2_median).toLocaleString("fr-FR") + " €/m²";
    kpiVentes.textContent =
      "Nombre de ventes : " + prix.nb_ventes.toLocaleString("fr-FR");
  } else {
    kpiPrix.textContent = "-";
    kpiVentes.textContent = "Nombre de ventes : -";
  }

  const logTxt = loge ? `${loge.nb_programmes.toLocaleString("fr-FR")} programmes sociaux` : "Logements sociaux : n.d.";

  const densTxt = dens && !isNaN(dens.densite_hab_km2)
    ? `${Math.round(dens.densite_hab_km2).toLocaleString("fr-FR")} hab/km²`
    : "densité n.d.";

  const delinTxt = delin && !isNaN(delin.score_delinquance)
    ? `${delin.score_delinquance.toFixed(1)}/10`
    : "délinquance n.d.";

  const vacTxt = vac && !isNaN(vac.taux_vacance)
    ? `${vac.taux_vacance.toFixed(1)}%`
    : "vacance n.d.";

  kpiLog.innerHTML = `
  <div class="kpi-row">🏘️ <span class="kpi-label">Programmes :</span> <span>${loge ? loge.nb_programmes : "—"}</span></div>
  <div class="kpi-row">👥 <span class="kpi-label">Densité :</span> <span>${dens && !isNaN(dens.densite_hab_km2) ? densTxt : "—"}</span></div>
  <div class="kpi-row">🏚️ <span class="kpi-label">Vacance :</span> <span>${vac && !isNaN(vac.taux_vacance) ? vacTxt : "—"}</span></div>
  <div class="kpi-row">🚓 <span class="kpi-label">Délinquance :</span> <span>${delin && !isNaN(delin.score_delinquance) ? delinTxt : "—"}</span></div>
`;


}

// full = true si on veut redessiner la carte (changement de données de base)
function updateAll(full = false) {
  updateYearUI();
  updateKPIs();
  if (full) {
    drawPolygons();
  }
}

// === Contrôles
function initControls() {
  arrSelect.addEventListener("change", () => {
    currentArr = parseInt(arrSelect.value, 10);
    updateAll(false);
  });

  yearSlider.addEventListener("input", () => {
    currentYear = parseInt(yearSlider.value, 10);
    updateAll(false);
    // popup se mettra à jour au prochain hover/clic
  });

  yearPrev.addEventListener("click", () => {
    const idx = years.indexOf(currentYear);
    if (idx > 0) {
      currentYear = years[idx - 1];
      updateAll(false);
    }
  });

  yearNext.addEventListener("click", () => {
    const idx = years.indexOf(currentYear);
    if (idx < years.length - 1) {
      currentYear = years[idx + 1];
      updateAll(false);
    }
  });
}

// === Boot ===
async function main() {
  initMap();
  await loadGeoJSON();

  const [
    arrRaw,
    prixRaw,
    logRaw,
    delinRaw,
    densRaw,
    vacRaw,
    typoRaw
  ] = await Promise.all([
    fetchJSON(`${API_BASE}/arrondissements`),
    fetchJSON(`${API_BASE}/prix_m2`),
    fetchJSON(`${API_BASE}/logements_sociaux`),
    fetchJSON(`${API_BASE}/delinquance`),
    fetchJSON(`${API_BASE}/densite`),
    fetchJSON(`${API_BASE}/vacance`),
    fetchJSON(`${API_BASE}/typologie`)
  ]);

  // Arrondissements
  arrMeta = arrRaw
    .map((d) => {
      const code = parseInt(d.code_arrondissement, 10);
      if (!Number.isInteger(code) || code < 1 || code > 20) return null;
      const labelBase = d.nom_officiel || d.nom || `Arrondissement ${code}`;
      const suffix = code === 1 ? "er" : "ème";
      return { code, label: `${code}${suffix} - ${labelBase}` };
    })
    .filter(Boolean)
    .sort((a, b) => a.code - b.code);

  // Prix m²
  prixData = prixRaw
    .map((d) => ({
      arrondissement: parseInt(d.arrondissement, 10),
      annee: parseInt(d.annee, 10),
      prix_m2_median: Number(d.prix_m2_median),
      nb_ventes: Number(d.nb_ventes),
    }))
    .filter((d) => !isNaN(d.arrondissement) && !isNaN(d.annee));

  // Logements sociaux
  logData = logRaw
    .map((d) => ({
      arrondissement: parseInt(d.arrondissement, 10),
      annee: parseInt(d.annee, 10),
      nb_programmes: Number(d.nb_programmes),
    }))
    .filter((d) => !isNaN(d.arrondissement) && !isNaN(d.annee));

  // Délinquance
  delinquanceData = delinRaw
    .map((d) => ({
      arrondissement: parseInt(d.arrondissement, 10),
      annee: parseInt(d.annee, 10),
      score_delinquance: Number(d.score_delinquance),
    }))
    .filter((d) => !isNaN(d.arrondissement) && !isNaN(d.annee));

  // Densité
  densiteData = densRaw
    .map((d) => ({
      arrondissement: parseInt(d.arrondissement, 10),
      annee: parseInt(d.annee, 10),
      densite_hab_km2: Number(d.densite_hab_km2),
    }))
    .filter((d) => !isNaN(d.arrondissement) && !isNaN(d.annee));

  // Vacance
  vacanceData = vacRaw
    .map((d) => ({
      arrondissement: parseInt(d.arrondissement, 10),
      annee: parseInt(d.annee, 10),
      taux_vacance: Number(d.taux_vacance),
    }))
    .filter((d) => !isNaN(d.arrondissement) && !isNaN(d.annee));

  // Typologie
  typologieData = typoRaw
    .map((d) => ({
      arrondissement: parseInt(d.arrondissement, 10),
      annee: parseInt(d.annee, 10),
      part_T1: Number(d.part_T1),
      part_T2: Number(d.part_T2),
      part_T3: Number(d.part_T3),
      part_T4: Number(d.part_T4),
    }))
    .filter((d) => !isNaN(d.arrondissement) && !isNaN(d.annee));

  // Années
  const yearSet = new Set(prixData.map(d => d.annee));
  years = Array.from(yearSet).sort((a, b) => a - b);
  currentYear = years[years.length - 1];

  yearSlider.min = years[0];
  yearSlider.max = years[years.length - 1];

  // Remplir le select
  arrMeta.forEach((a) => {
    const opt = document.createElement("option");
    opt.value = a.code;
    opt.textContent = a.label;
    arrSelect.appendChild(opt);
  });

  currentArr = arrMeta[0].code;
  arrSelect.value = String(currentArr);

  drawPolygons();
  initControls();
  updateAll(true);
}

// Lancer
main().catch((err) => {
  console.error(err);
  alert("Erreur : " + err.message);
});
