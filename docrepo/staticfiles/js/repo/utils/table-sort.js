document.addEventListener('alpine:init', () => {
  Alpine.data('orderByToggle', (column) => ({
    currentOrderBy: new URLSearchParams(window.location.search).get('order_by') || column,
    get nextOrderBy() {
      return this.currentOrderBy === column ? `-${column}` : column;
    }
  }));
});
