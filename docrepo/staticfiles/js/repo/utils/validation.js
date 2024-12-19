document.addEventListener('alpine:init', () => {
  Alpine.data('updateElementFormValidation', () => ({
    name: '',
    message: 'Recycle is a reserved system element name and cannot be used.',
    errorMessage: '',
    validateName() {
      this.errorMessage = (this.name.toLowerCase() === 'recycle')
        ? this.message
        : '';
    },
    handleSubmit(event) {
      if (this.name.toLowerCase() === 'recycle') {
        event.preventDefault();
        this.errorMessage = this.message;
      } else {
        this.errorMessage = '';
        event.target.submit();
      }
    }
  }));
});
