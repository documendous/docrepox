document.addEventListener('alpine:init', () => {
  Alpine.data('handleClipboardModal', ({hasClipboardErrors}) => ({
      hasClipboardErrors: hasClipboardErrors,
  }))
})

function removeClipboardIcon(elementId) {
  // Removes clipboard icons for elements when removed from the clipboard modal
  document.getElementById('in_clipboard_icon_' + elementId).remove()
}
