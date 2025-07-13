const uploadBox = document.getElementById('uploadBox');
const uploadText = document.getElementById('uploadText');
const fileInput = document.getElementById('fileInput');

uploadBox.addEventListener('dragover', function (e) {
    e.preventDefault();
    uploadBox.style.backgroundColor = "#e6f7ff";
});

uploadBox.addEventListener('dragleave', function () {
    uploadBox.style.backgroundColor = "white";
});

fileInput.addEventListener('change', function () {
    if (fileInput.files.length > 0) {
        uploadText.innerText = "Selected File: " + fileInput.files[0].name;
    }
});

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    event.target.classList.add('active');
}

function addManualRow() {
    const container = document.getElementById('manual-entries');
    const row = document.createElement('div');
    row.className = 'manual-row';
    row.innerHTML = `
        <input type="date" name="date">
        <input type="number" name="amount" placeholder="Amount">
        <input type="text" name="category" placeholder="Category">
        <input type="text" name="vendor" placeholder="Vendor">
    `;
    container.appendChild(row);
}
