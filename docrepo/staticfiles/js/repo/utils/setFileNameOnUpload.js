function setFileNameOnUpload(contentFileId, documentNameId) {
  const fileInput = document.getElementById(contentFileId);
  const nameInput = document.getElementById(documentNameId);

  fileInput.addEventListener('change', function() {
    nameInputValue = fileInput.files[0].name
    nameInput.value = nameInputValue;
  });
}

function main() {
  setFileNameOnUpload('id_content_file', 'id_document_name');
}

main();
