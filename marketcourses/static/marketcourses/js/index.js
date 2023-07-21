menu = document.getElementsByClassName('menu-icon-p')[0];
menu_items = document.getElementById('menu_items');
menu_items.style.maxHeight = "0px";

function menu_items_dissapear(){
    if (menu_items.style.maxHeight == "0px")
        {
            menu_items.style.maxHeight = "200px";
        }
    else
    {
        menu_items.style.maxHeight = "0px";
    }
}

menu.addEventListener("click", menu_items_dissapear);


function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    const offsetTop = section.offsetTop;
    window.scrollTo({
      top: offsetTop,
      behavior: 'smooth'
    });
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    const cursosLink = document.querySelector('#menu_items li:first-child a');
  
    cursosLink.addEventListener("click", function(event) {
      event.preventDefault();
      scrollToSection('cursos');
    });
  });