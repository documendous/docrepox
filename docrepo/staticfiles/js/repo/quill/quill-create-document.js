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

  quill.container.previousSibling
    .querySelector('button.ql-bold')
    .setAttribute('title', 'Bold text');
  
  quill.container.previousSibling
    .querySelector('button.ql-italic')
    .setAttribute('title', 'Italicize text');
  
  quill.container.previousSibling
    .querySelector('button.ql-strike')
    .setAttribute('title', 'Strike through text');
  
  quill.container.previousSibling
    .querySelector('button.ql-blockquote')
    .setAttribute('title', 'Blockquote text');
  
  quill.container.previousSibling
    .querySelector('button.ql-code-block')
    .setAttribute('title', 'Code block text');

  quill.container.previousSibling
    .querySelector('button.ql-link')
    .setAttribute('title', 'Insert hyperlink');

  quill.container.previousSibling
    .querySelector('button.ql-list')
    .setAttribute('title', 'Order list');

  quill.container.previousSibling
    .querySelector('button.ql-list[value="bullet"]')
    .setAttribute('title', 'Unorder list');

  quill.container.previousSibling
    .querySelector('button.ql-indent[value="-1"]')
    .setAttribute('title', 'De-indent text');

  quill.container.previousSibling
    .querySelector('button.ql-indent[value="+1"]')
    .setAttribute('title', 'Indent text');
  
  quill.container.previousSibling
    .querySelector('button.ql-direction[value="rtl"]')
    .setAttribute('title', 'Text direction');

  quill.container.previousSibling
    .querySelector('span.ql-size')
    .setAttribute('title', 'Resize text');

  quill.container.previousSibling
    .querySelector('span.ql-header')
    .setAttribute('title', 'Resize header');

  quill.container.previousSibling
    .querySelector('span.ql-color')
    .setAttribute('title', 'Foreground color');

  quill.container.previousSibling
    .querySelector('span.ql-background')
    .setAttribute('title', 'Background color');
  
  quill.container.previousSibling
    .querySelector('span.ql-font')
    .setAttribute('title', 'Select font');
  
  quill.container.previousSibling
    .querySelector('span.ql-align')
    .setAttribute('title', 'Select alignment');

  const contentInput = document.querySelector('#content');
    
  quill.on('text-change', function() {
    contentInput.value = quill.root.innerHTML.trim();
  });
});
