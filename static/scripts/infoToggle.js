let coll = document.getElementsByClassName("collapsible");
let i;

for (i = 0; i < coll.length; i++) {

    coll[i].addEventListener("click", function() {

        this.classList.toggle("active");
        let content = this.nextElementSibling;  // this requires the next HTML element to be the paragraph

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } 
        else {
            content.style.maxHeight = content.scrollHeight + "px";
        } 
    });
}
