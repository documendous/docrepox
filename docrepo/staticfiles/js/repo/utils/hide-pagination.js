function hide(elementName) {
  let element = document.getElementById(elementName);
  if (element) {element.classList.add('hidden');}
}

function main() {
  hide('pagination');
}

main();
