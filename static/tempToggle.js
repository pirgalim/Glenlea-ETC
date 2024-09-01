const tempLabel = document.getElementById('star_temp_label');
const tempField = document.getElementById('star_temp');


document.getElementById('point_src').addEventListener('change', function() {

    var selectedOption = this.value;

   
    console.log(selectedOption);

    if(selectedOption != '') {

        alert("change");
        tempLabel.style.background = "lightgray";
        tempLabel.style.color = "darkgray";
        tempField.style.background = "lightgray";
        tempField.style.border = "lightgray";
        tempField.style.color = "lightgray";

        tempField.value = "   01.  ";
        tempField.readOnly = true;
        }

    else {

        alert("revert");
        tempLabel.style.background = "slategray";
        tempLabel.style.color = "white";
        tempField.style.background = "white";
        tempField.style.border = "white";
        tempField.style.color = "black";

        //tempField.value = document.getElementById("conditions").value;
        tempField.readOnly = false;
        tempField.value = "";
}
    
    
});