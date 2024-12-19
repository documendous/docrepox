document.addEventListener('alpine:init', () => {
  Alpine.data('localeString', ({dateTime}) => ({
    dateTime: dateTime,
    localDateTime: null,

    setToLocale() {
      const date = new Date(this.dateTime);
      const localeString = date.toLocaleString(
        'en-US', {
          month: 'numeric',
          day: 'numeric',
          year: 'numeric',
          hour: 'numeric',
          minute: '2-digit',
          // second: '2-digit',
          hour12: true
        }
      );
      
      const timeZoneAbbr = date.toLocaleTimeString('en-us',{timeZoneName:'short'}).split(' ')[2]
      this.localDateTime = `${localeString} ${timeZoneAbbr}`;
    },

    init() {
      this.setToLocale();
      },
  }))
})
