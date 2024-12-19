const toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  ['blockquote', 'code-block'],
  ['link'],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  [{ 'direction': 'rtl' }],                         // text direction

  [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
  [{ 'font': [] }],
  [{ 'align': [] }],
];

const options = {
  // debug: 'info',
  modules: {
    toolbar: toolbarOptions,
  },
  theme: 'snow'
};
document.addEventListener('DOMContentLoaded', function() {
  const quill = new Quill('#editor', options);
  const contentInput = document.querySelector('#content');        
  quill.on('text-change', function() {
    contentInput.value = quill.root.innerHTML.trim();
  });
});
