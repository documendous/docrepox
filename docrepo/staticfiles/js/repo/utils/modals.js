function showModal(modalId) {
  event.preventDefault();
  document.getElementById(modalId).classList.remove('hidden');
}

function showProjectGroupModal(modalId, groupName, formActionUrl) {
  const form = document.getElementById(`addUserForm_${groupName}`);

  if (form) {
    form.setAttribute('action', formActionUrl);
  }

  showModal(modalId);
}

function reloadParentPage() {
  // Reloads the parent page in case needed.
  window.location.reload();
}

function hideModal(modalId) {
  document.getElementById(modalId).classList.add('hidden');
}

document.addEventListener('alpine:init', () => {
  Alpine.data('handleModal', ({hasErrors}) => ({
      hasErrors: hasErrors,
  }))
})
