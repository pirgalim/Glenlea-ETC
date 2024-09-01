const tempLabel = document.getElementById('star_temp_label');
const tempField = document.getElementById('star_temp');


document.getElementById('point_src').addEventListener('change', function() {

    var selectedOption = this.value;

    if(selectedOption != '') {

        tempLabel.style.background = "lightgray";
        tempLabel.style.color = "darkgray";
        tempField.style.background = "lightgray";
        tempField.style.border = "lightgray";
        tempField.style.color = "lightgray";
        tempField.value = "   07.  ";
        tempField.readOnly = true;
        }

    else {

        tempLabel.style.background = "slategray";
        tempLabel.style.color = "white";
        tempField.style.background = "white";
        tempField.style.border = "white";
        tempField.style.color = "black";
        tempField.readOnly = false;
        tempField.value = "";
    }
    
});