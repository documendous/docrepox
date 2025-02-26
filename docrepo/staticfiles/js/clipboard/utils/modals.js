document.addEventListener('alpine:init', () => {
  Alpine.data('handleClipboardModal', ({hasClipboardErrors}) => ({
      hasClipboardErrors: hasClipboardErrors,
  }))
})

function removeClipboardIcon(elementId, elementType) {
  // Removes clipboard icons for elements when removed from the clipboard modal
  let elementName = '';

  if (elementType === 'document')
    elementName = 'in_clipboard_icon_doc_';
  else
    elementName = 'in_clipboard_icon_folder_';

  const icon = document.getElementById(elementName + elementId);
  if (icon) icon.remove();
}

document.addEventListener("htmx:afterRequest", function (event) {
  if (!event.detail.successful) return;

  let triggerElement = event.detail.elt;

  if (triggerElement && triggerElement.id === "remove-documents") {
    document.querySelectorAll('[id^="in_clipboard_icon_doc_"]').forEach(icon => icon.remove());
  }

  if (triggerElement && triggerElement.id === "remove-folders") {
    document.querySelectorAll('[id^="in_clipboard_icon_folder_"]').forEach(icon => icon.remove());
  }
});
