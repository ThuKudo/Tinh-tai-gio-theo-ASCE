const storageKey = "win-load-asce-state-v2";

const state = {
  config: null,
  values: {},
  result: null,
  reportBlocks: null,
  language: "vi",
};

const el = {
  form: document.getElementById("windForm"),
  sections: document.getElementById("formSections"),
  resultCards: document.getElementById("resultCards"),
  tablesWrap: document.getElementById("tablesWrap"),
  breakdownWrap: document.getElementById("breakdownWrap"),
  assumptionsWrap: document.getElementById("assumptionsWrap"),
  statusBanner: document.getElementById("statusBanner"),
  lastRunLabel: document.getElementById("lastRunLabel"),
  importFile: document.getElementById("importFile"),
  loadSampleBtn: document.getElementById("loadSampleBtn"),
  resetBtn: document.getElementById("resetBtn"),
  exportInputBtn: document.getElementById("exportInputBtn"),
  exportResultBtn: document.getElementById("exportResultBtn"),
  exportHtmlBtn: document.getElementById("exportHtmlBtn"),
  exportMarkdownBtn: document.getElementById("exportMarkdownBtn"),
  exportPdfBtn: document.getElementById("exportPdfBtn"),
  copySummaryBtn: document.getElementById("copySummaryBtn"),
  copyInputsBtn: document.getElementById("copyInputsBtn"),
  copyBreakdownBtn: document.getElementById("copyBreakdownBtn"),
  copyResultsBtn: document.getElementById("copyResultsBtn"),
  fieldTemplate: document.getElementById("fieldTemplate"),
  langViBtn: document.getElementById("langViBtn"),
  langEnBtn: document.getElementById("langEnBtn"),
};

function t(key) {
  return state.config?.ui_text?.[state.language]?.[key] ?? key;
}

function setBanner(message, mode = "success") {
  el.statusBanner.textContent = message;
  el.statusBanner.className = `status-banner ${mode}`;
}

function clearBanner() {
  el.statusBanner.className = "status-banner hidden";
  el.statusBanner.textContent = "";
}

function formatHeading(value) {
  return value.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function downloadBlob(filename, blob) {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

function persistState() {
  localStorage.setItem(storageKey, JSON.stringify({
    values: state.values,
    result: state.result,
    reportBlocks: state.reportBlocks,
    language: state.language,
  }));
}

function restoreState(defaults, defaultLanguage) {
  try {
    const raw = localStorage.getItem(storageKey);
    if (!raw) {
      state.values = { ...defaults };
      state.language = defaultLanguage;
      return;
    }
    const parsed = JSON.parse(raw);
    state.values = { ...defaults, ...(parsed.values || {}) };
    state.result = parsed.result || null;
    state.reportBlocks = parsed.reportBlocks || null;
    state.language = parsed.language || defaultLanguage;
  } catch {
    state.values = { ...defaults };
    state.language = defaultLanguage;
  }
}

function localizeStaticText() {
  document.documentElement.lang = state.language;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  el.langViBtn.classList.toggle("active", state.language === "vi");
  el.langEnBtn.classList.toggle("active", state.language === "en");
  if (!state.result) {
    resetOutputsOnly(false);
  } else {
    renderResult(state.result, false);
  }
}

function createField(field) {
  const fragment = el.fieldTemplate.content.cloneNode(true);
  const wrapper = fragment.querySelector(".field");
  const label = fragment.querySelector("label");
  const inputWrap = fragment.querySelector(".input-wrap");
  const helper = fragment.querySelector(".helper");
  const unit = fragment.querySelector(".unit");

  label.textContent = field.label[state.language];
  label.htmlFor = field.name;
  helper.textContent = field.helper?.[state.language] || "";
  unit.textContent = field.unit === "years" ? t("unit_years") : field.unit || "";

  let control;
  if (field.type === "select") {
    control = document.createElement("select");
    field.options.forEach((option) => {
      const node = document.createElement("option");
      node.value = option;
      node.textContent = option;
      control.appendChild(node);
    });
  } else {
    control = document.createElement("input");
    control.type = field.type || "text";
    if (field.step) control.step = field.step;
    control.placeholder = field.placeholder?.[state.language] || "";
  }

  control.id = field.name;
  control.name = field.name;
  control.value = state.values[field.name] ?? "";
  control.addEventListener("input", (event) => {
    state.values[field.name] = event.target.value;
    wrapper.classList.remove("invalid");
    wrapper.querySelector(".error").textContent = "";
    persistState();
  });

  inputWrap.appendChild(control);
  return wrapper;
}

function renderForm() {
  el.sections.innerHTML = "";
  state.config.sections.forEach((section) => {
    const card = document.createElement("section");
    card.className = "form-section";
    card.innerHTML = `<h3>${section.title[state.language]}</h3><p>${section.description[state.language]}</p>`;
    const grid = document.createElement("div");
    grid.className = "field-grid";
    section.fields.forEach((field) => grid.appendChild(createField(field)));
    card.appendChild(grid);
    el.sections.appendChild(card);
  });
}

function collectPayload() {
  const payload = {};
  state.config.sections.forEach((section) => {
    section.fields.forEach((field) => {
      const value = state.values[field.name];
      payload[field.name] = field.type === "number" ? (value === "" ? null : Number(value)) : value;
    });
  });
  return payload;
}

function renderCards(cards) {
  el.resultCards.classList.remove("empty-state");
  el.resultCards.innerHTML = cards.map((card) => `
    <article class="metric-card">
      <span>${card.title}</span>
      <strong>${card.display_value}</strong>
      <p class="helper">${card.detail}</p>
    </article>
  `).join("");
}

function renderTable(title, rows) {
  if (!rows.length) return "";
  const columns = Object.keys(rows[0]);
  return `
    <div class="table-card">
      <h3>${title}</h3>
      <div class="table-scroll">
        <table>
          <thead><tr>${columns.map((column) => `<th>${formatHeading(column)}</th>`).join("")}</tr></thead>
          <tbody>
            ${rows.map((row) => `<tr>${columns.map((column) => `<td>${row[column]}</td>`).join("")}</tr>`).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderBreakdown(items) {
  el.breakdownWrap.classList.remove("empty-state");
  el.breakdownWrap.innerHTML = items.map((item, index) => `
    <details class="accordion-item" ${index === 0 ? "open" : ""}>
      <summary>${item.title}</summary>
      <div class="accordion-content">
        <p><strong>${item.formula_label}:</strong></p>
        <div class="formula-block">${item.formula}</div>
        <p><strong>${item.substitute_label}:</strong></p>
        <div class="formula-block">${item.substitution}</div>
        <p><strong>${item.result_label}:</strong> ${item.result}</p>
        <p><strong>${item.note_label}:</strong> ${item.note}</p>
      </div>
    </details>
  `).join("");
}

function renderAssumptions(items, warnings = []) {
  el.assumptionsWrap.classList.remove("empty-state");
  el.assumptionsWrap.innerHTML = `
    <ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>
    ${warnings.length ? `<div class="warning-list"><strong>${t("title_warnings")}:</strong><ul>${warnings.map((item) => `<li>${item}</li>`).join("")}</ul></div>` : ""}
  `;
}

function setReportActions(enabled) {
  [el.exportResultBtn, el.exportHtmlBtn, el.exportMarkdownBtn, el.exportPdfBtn, el.copySummaryBtn, el.copyInputsBtn, el.copyBreakdownBtn, el.copyResultsBtn].forEach((button) => {
    button.disabled = !enabled;
  });
}

function renderResult(result, persist = true) {
  state.result = result;
  renderCards(result.cards);
  el.tablesWrap.classList.remove("empty-state");
  el.tablesWrap.innerHTML = [
    renderTable(t("case_a_title"), result.outputs.case_a),
    renderTable(t("case_b_title"), result.outputs.case_b),
    renderTable(t("intermediate_title"), Object.entries(result.intermediate).map(([name, value]) => ({ name, value }))),
  ].join("");
  renderBreakdown(result.breakdown);
  renderAssumptions(result.assumptions, result.warnings || []);
  el.lastRunLabel.textContent = `${t("last_run")}: ${new Date(result.meta.generated_at).toLocaleString(state.language === "vi" ? "vi-VN" : "en-US")}`;
  setReportActions(true);
  if (persist) persistState();
}

function clearValidationErrors() {
  document.querySelectorAll(".field").forEach((field) => {
    field.classList.remove("invalid");
    field.querySelector(".error").textContent = "";
  });
}

function applyValidationErrors(detail) {
  clearValidationErrors();
  detail.forEach((issue) => {
    const name = issue.loc[issue.loc.length - 1];
    const field = document.getElementById(name)?.closest(".field");
    if (field) {
      field.classList.add("invalid");
      field.querySelector(".error").textContent = issue.msg;
    }
  });
  setBanner(t("status_validation"), "error");
}

async function fetchReportBlocks() {
  const response = await fetch(`/api/report/blocks?lang=${state.language}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ inputs: collectPayload() }),
  });
  if (!response.ok) return;
  const data = await response.json();
  state.reportBlocks = data.blocks;
  persistState();
}

async function runCalculation() {
  clearValidationErrors();
  clearBanner();
  const response = await fetch(`/api/calculate?lang=${state.language}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(collectPayload()),
  });
  if (!response.ok) {
    if (response.status === 422) {
      applyValidationErrors((await response.json()).detail);
      return;
    }
    setBanner(await response.text(), "error");
    return;
  }
  renderResult(await response.json());
  await fetchReportBlocks();
  setBanner(t("status_success"), "success");
}

async function exportEndpoint(endpoint, filename) {
  const response = await fetch(`${endpoint}?lang=${state.language}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ inputs: collectPayload() }),
  });
  const blob = await response.blob();
  const disposition = response.headers.get("content-disposition");
  const matched = disposition ? disposition.match(/filename=([^;]+)/) : null;
  downloadBlob(matched ? matched[1] : filename, blob);
}

async function copyBlock(key) {
  if (!state.reportBlocks) {
    await fetchReportBlocks();
  }
  const content = state.reportBlocks?.[key];
  if (!content) return;
  try {
    await navigator.clipboard.writeText(content);
    setBanner(t("status_copy_success"), "success");
  } catch {
    setBanner(t("status_copy_fail"), "error");
  }
}

function loadImportedInput(content) {
  try {
    const parsed = JSON.parse(content);
    state.values = { ...state.config.defaults, ...parsed };
    state.result = null;
    state.reportBlocks = null;
    persistState();
    renderForm();
    resetOutputsOnly(false);
    setBanner(t("status_imported"), "success");
  } catch {
    setBanner(t("status_invalid_json"), "error");
  }
}

function resetOutputsOnly(clear = true) {
  el.resultCards.className = "result-cards empty-state";
  el.resultCards.innerHTML = `<p>${t("run_to_populate")}</p>`;
  el.tablesWrap.className = "tables-wrap empty-state";
  el.tablesWrap.innerHTML = `<p>${t("tables_placeholder")}</p>`;
  el.breakdownWrap.className = "accordion-list empty-state";
  el.breakdownWrap.innerHTML = `<p>${t("breakdown_placeholder")}</p>`;
  el.assumptionsWrap.className = "notes-list empty-state";
  el.assumptionsWrap.innerHTML = `<p>${t("notes_placeholder")}</p>`;
  el.lastRunLabel.textContent = t("no_calculation");
  renderAssumptions(state.config.assumptions[state.language]);
  setReportActions(false);
  if (clear) clearBanner();
}

function resetForm() {
  state.values = { ...state.config.defaults };
  state.result = null;
  state.reportBlocks = null;
  persistState();
  renderForm();
  resetOutputsOnly();
}

async function init() {
  try {
    state.config = await (await fetch("/api/form-config")).json();
    restoreState(state.config.defaults, state.config.default_language);
    renderForm();
    localizeStaticText();
    if (state.result) {
      renderResult(state.result, false);
    } else {
      renderAssumptions(state.config.assumptions[state.language]);
    }

    el.form.addEventListener("submit", async (event) => {
      event.preventDefault();
      await runCalculation();
    });

    el.loadSampleBtn.addEventListener("click", () => {
      state.values = { ...state.config.defaults };
      state.result = null;
      state.reportBlocks = null;
      persistState();
      renderForm();
      resetOutputsOnly();
      setBanner(t("status_sample_loaded"), "success");
    });

    el.resetBtn.addEventListener("click", resetForm);
    el.exportInputBtn.addEventListener("click", () => downloadBlob("win-load-asce-input.json", new Blob([JSON.stringify(collectPayload(), null, 2)], { type: "application/json" })));
    el.exportResultBtn.addEventListener("click", () => {
      if (!state.result) return;
      downloadBlob("win-load-asce-result.json", new Blob([JSON.stringify(state.result, null, 2)], { type: "application/json" }));
    });
    el.exportHtmlBtn.addEventListener("click", () => exportEndpoint("/api/report/html", "wind-report.html"));
    el.exportMarkdownBtn.addEventListener("click", () => exportEndpoint("/api/report/markdown", "wind-report.md"));
    el.exportPdfBtn.addEventListener("click", () => exportEndpoint("/api/report/pdf", "wind-report.pdf"));
    el.copySummaryBtn.addEventListener("click", () => copyBlock("executive_summary"));
    el.copyInputsBtn.addEventListener("click", () => copyBlock("input_table"));
    el.copyBreakdownBtn.addEventListener("click", () => copyBlock("calculation_breakdown"));
    el.copyResultsBtn.addEventListener("click", () => copyBlock("final_results"));
    el.importFile.addEventListener("change", async (event) => {
      const file = event.target.files[0];
      if (file) loadImportedInput(await file.text());
      event.target.value = "";
    });
    el.langViBtn.addEventListener("click", async () => {
      state.language = "vi";
      persistState();
      renderForm();
      localizeStaticText();
      if (state.result) {
        await runCalculation();
      }
    });
    el.langEnBtn.addEventListener("click", async () => {
      state.language = "en";
      persistState();
      renderForm();
      localizeStaticText();
      if (state.result) {
        await runCalculation();
      }
    });
  } catch {
    setBanner(t("status_backend_error"), "error");
  }
}

init();
