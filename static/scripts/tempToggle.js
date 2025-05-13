const tempLabel = document.getElementById('star_temp_label');
const tempField = document.getElementById('star_temp');


/**
 * Listen for a change in the point source menu
 * If a non blackbody source is selected then disable the temperature field
 * If a blackbody is selected then enable the tempertature field
 */
document.getElementById('point_src').addEventListener('change', function() {

    if(this.value != '') {
        disable();
    }
    else {
        enable();
    }
    
});


document.addEventListener('DOMContentLoaded', function() {

    document.getElementById("defaultOpen").addEventListener("click", function() {

        let selectedOption = document.getElementById('point_src').value;

        if(selectedOption == '') {
            enable();
        }
    })

    document.getElementById("defaultClose").addEventListener("click", function() {
        disable();    
    })
});



function enable() {

    
    tempLabel.style.background = "slategray";
    tempLabel.style.color = "white";
    tempField.style.background = "white";
    tempField.style.border = "white";
    tempField.style.color = "black";
    tempField.required = true;
    tempField.readOnly = false;
}


function disable() {

    tempLabel.style.background = "lightgray";
    tempLabel.style.color = "darkgray";
    tempField.style.background = "lightgray";
    tempField.style.border = "lightgray";
    tempField.style.color = "lightgray";
    tempField.required = false;
    tempField.readOnly = true;
    tempField.value = "";
}