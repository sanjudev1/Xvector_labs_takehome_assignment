function validateForm() {
  var filenameInput = document.getElementById('filename');
  var filename = filenameInput.value.trim();
  var fileInput = document.getElementById('fileInput');
  var selectedFile = fileInput.files[0];

  if (!selectedFile) {
    alert('Please choose a file to upload.');
    return false;
  }

  if (filename === '' || filename.length < 3) {
    alert('Please enter a valid filename with at least three characters.');
    return false;
  }

  return true;
}
