const API_BASE = 'http://localhost:8000';

const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const youtubeUrl = document.getElementById('youtube-url');
const processYtBtn = document.getElementById('process-yt-btn');
const progressSection = document.getElementById('progress-section');
const resultSection = document.getElementById('result-section');
const uploadSection = document.querySelector('.upload-section');
const progressBar = document.getElementById('progress-bar');
const statusText = document.getElementById('status-text');
const summaryContent = document.getElementById('summary-content');
const resetBtn = document.getElementById('reset-btn');

// Drag and Drop
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#6366f1';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = 'rgba(255, 255, 255, 0.1)';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFileUpload(files[0]);
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFileUpload(e.target.files[0]);
});

processYtBtn.addEventListener('click', () => {
    const url = youtubeUrl.value.trim();
    if (url) handleYoutubeProcess(url);
});

resetBtn.addEventListener('click', () => {
    resultSection.classList.add('hidden');
    uploadSection.classList.remove('hidden');
    youtubeUrl.value = '';
    progressBar.style.width = '0%';
});

async function handleFileUpload(file) {
    showProgress();
    statusText.innerText = `Uploading ${file.name}...`;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        pollStatus(data.job_id);
    } catch (err) {
        handleError(err);
    }
}

async function handleYoutubeProcess(url) {
    showProgress();
    statusText.innerText = 'Connecting to YouTube...';

    try {
        const response = await fetch(`${API_BASE}/process-youtube`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await response.json();
        pollStatus(data.job_id);
    } catch (err) {
        handleError(err);
    }
}

function showProgress() {
    uploadSection.classList.add('hidden');
    progressSection.classList.remove('hidden');
    progressBar.style.width = '10%';
}

async function pollStatus(jobId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/status/${jobId}`);
            const data = await response.json();

            if (data.status === 'processing') {
                progressBar.style.width = '70%'; // Increase visual progress
                statusText.innerText = data.status_msg || 'Analyzing video...';
            } else if (data.status === 'completed') {
                clearInterval(interval);
                showResult(data.results.summary_text);
            } else if (data.status === 'failed') {
                clearInterval(interval);
                handleError(data.error);
            }
        } catch (err) {
            clearInterval(interval);
            handleError(err);
        }
    }, 3000);
}

function showResult(summaryMarkdown) {
    progressSection.classList.add('hidden');
    resultSection.classList.remove('hidden');
    summaryContent.innerHTML = marked.parse(summaryMarkdown);
}

function handleError(err) {
    console.error(err);
    statusText.innerText = `Error: ${err}`;
    progressBar.style.background = '#ef4444';
}
