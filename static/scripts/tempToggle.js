const tempLabel = document.getElementById('star_temp_label');
const tempField = document.getElementById('star_temp');

// let prev = document.getElementById('point_src').value;



document.getElementById('point_src').addEventListener('change', function() {

    let selectedOption = this.value;

    if(selectedOption != '') {

        disable();

        // tempLabel.style.background = "lightgray";
        // tempLabel.style.color = "darkgray";
        // tempField.style.background = "lightgray";
        // tempField.style.border = "lightgray";
        // tempField.style.color = "lightgray";
        // tempField.required = false;
        // tempField.readOnly = true;
        // tempField.value = "";
    }

    else {

        
        enable();

        // this.value = selectedOption;
        // tempLabel.style.background = "slategray";
        // tempLabel.style.color = "white";
        // tempField.style.background = "white";
        // tempField.style.border = "white";
        // tempField.style.color = "black";
        // tempField.required = true;
        // tempField.readOnly = false;
    }
    
});


document.addEventListener('DOMContentLoaded', function() {


    document.getElementById("defaultOpen").addEventListener("click", function() {

        let selectedOption = document.getElementById('point_src').value;

        if(selectedOption == '') {
            enable();
        }

        
        // tempLabel.style.background = "slategray";
        // tempLabel.style.color = "white";
        // tempField.style.background = "white";
        // tempField.style.border = "white";
        // tempField.style.color = "black";
        // tempField.required = true;
        // tempField.readOnly = false;
        
    })


    
    document.getElementById("defaultClose").addEventListener("click", function() {

        disable();

        // tempLabel.style.background = "lightgray";
        // tempLabel.style.color = "darkgray";
        // tempField.style.background = "lightgray";
        // tempField.style.border = "lightgray";
        // tempField.style.color = "lightgray";
        // tempField.required = false;
        // tempField.readOnly = true;
        
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








// window.onload = changeTemp;






// function changeTemp() {


//     var selectedOption = document.getElementById('point_src').value;

//     if(selectedOption != '') {

//         tempLabel.style.background = "lightgray";
//         tempLabel.style.color = "darkgray";
//         tempField.style.background = "lightgray";
//         // tempField.style.border = "lightgray";
//         tempField.style.color = "lightgray";
//         tempField.required = false;
//         tempField.readOnly = true;
//     }

//     else {

//         tempLabel.style.background = "slategray";
//         tempLabel.style.color = "white";
//         tempField.style.background = "white";
//         // tempField.style.border = "white";
//         tempField.style.color = "black";
//         tempField.required = true;
//         tempField.readOnly = false;
//     }
    
// }