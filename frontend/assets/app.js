const form = document.getElementById("predict-form");
const fileInput = document.getElementById("file-input");
const dropzone = document.getElementById("dropzone");
const previewWrap = document.getElementById("preview-wrap");
const previewImage = document.getElementById("preview-image");
const resultState = document.getElementById("result-state");
const submitBtn = document.getElementById("submit-btn");

const API_URL = "/api/v1/predict";
const diseaseLabels = {
  healthy: "Здоровая кожа",
  eczema: "Экзема",
  psoriasis: "Псориаз",
};

const setResultHtml = (html) => {
  resultState.innerHTML = html;
};

const renderSuccess = (data) => {
  const confidence = Number(data.confidence || 0);
  const confidencePercent = Math.max(0, Math.min(100, Math.round(confidence * 100)));
  const severityLabel = data.severity || "не определена";
  const severityPercent = Math.max(
    0,
    Math.min(100, Math.round(Number(data.severity_score || 0) * 100))
  );
  setResultHtml(`
    <span class="result-chip success">Результат AI</span>
    <h3 class="result-main">${diseaseLabels[data.disease] || data.disease}</h3>
    <div class="confidence-row">
      <span>Уверенность модели</span>
      <strong id="confidence-percent">0%</strong>
    </div>
    <div class="confidence-track">
      <div class="confidence-fill" id="confidence-fill"></div>
    </div>
    <p class="confidence">Тяжесть: <strong>${severityLabel}</strong> (${severityPercent}%)</p>
    <p class="recommendation">${data.recommendation}</p>
  `);

  requestAnimationFrame(() => {
    const fillEl = document.getElementById("confidence-fill");
    const percentEl = document.getElementById("confidence-percent");
    if (!fillEl || !percentEl) {
      return;
    }
    fillEl.style.width = `${confidencePercent}%`;
    percentEl.textContent = `${confidencePercent}%`;
  });
};

const renderError = (message) => {
  setResultHtml(`
    <span class="result-chip error">Ошибка</span>
    <p class="result-main">${message}</p>
  `);
};

const renderLoading = () => {
  setResultHtml(`
    <div class="skeleton skeleton-chip"></div>
    <div class="skeleton skeleton-title"></div>
    <div class="skeleton skeleton-line mid"></div>
    <div class="skeleton skeleton-line"></div>
    <div class="skeleton skeleton-line short"></div>
    <p class="result-placeholder">Выполняется анализ изображения...</p>
  `);
};

const showPreview = (file) => {
  const reader = new FileReader();
  reader.onload = (event) => {
    previewImage.src = event.target.result;
    previewWrap.hidden = false;
  };
  reader.readAsDataURL(file);
};

const applyDroppedFiles = (files) => {
  if (!files || files.length === 0) {
    return;
  }
  fileInput.files = files;
  showPreview(files[0]);
};

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropzone.classList.add("drag-over");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("drag-over");
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropzone.classList.remove("drag-over");
  applyDroppedFiles(event.dataTransfer.files);
});

fileInput.addEventListener("change", () => {
  const [file] = fileInput.files;
  if (file) {
    showPreview(file);
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const [file] = fileInput.files;

  if (!file) {
    renderError("Сначала выберите изображение.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  submitBtn.disabled = true;
  renderLoading();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      renderError(data.error || "Не удалось выполнить анализ.");
      return;
    }
    renderSuccess(data);
  } catch (error) {
    renderError("Ошибка сети. Попробуйте еще раз.");
  } finally {
    submitBtn.disabled = false;
  }
});
