
document.addEventListener('DOMContentLoaded', function() {
    const seeingLabel = document.getElementById('seeing-label');
    const seeingField = document.getElementById('seeing');
    const selectMenu = document.getElementById('conditions');


    // testing
    // const tempLabel = document.getElementById('star_temp_label');
    // const tempField = document.getElementById('star_temp');



    console.log(seeingField)


    document.getElementById("defaultOpen").addEventListener("click", function() {


        seeingLabel.style.background = "slategray";
        seeingLabel.style.color = "white";
        seeingField.style.background = "white";
        seeingField.style.border = "white";
        seeingField.style.color = "black";
        seeingField.required = true;
        seeingField.readOnly = false;

        selectMenu.disabled = false;



        // let selectedOption = document.getElementById('point_src').value;

        // if(selectedOption != '') {

        //     tempLabel.style.background = "lightgray";
        //     tempLabel.style.color = "darkgray";
        //     tempField.style.background = "lightgray";
        //     tempField.style.border = "lightgray";
        //     tempField.style.color = "lightgray";
        //     tempField.required = false;
        //     tempField.readOnly = true;
        //     tempField.value = "";
        // }

        // else {

        //     tempLabel.style.background = "slategray";
        //     tempLabel.style.color = "white";
        //     tempField.style.background = "white";
        //     tempField.style.border = "white";
        //     tempField.style.color = "black";
        //     tempField.required = true;
        //     tempField.readOnly = false;
        // }





    })

    document.getElementById("defaultClose").addEventListener("click", function() {

        console.log("test");
        seeingLabel.style.background = "lightgray";
        seeingLabel.style.color = "darkgray";
        seeingField.style.background = "lightgray";
        seeingField.style.border = "lightgray";
        seeingField.style.color = "lightgray";
        seeingField.required = false;
        seeingField.readOnly = true;

        selectMenu.disabled = true;






        // console.log("Hello")
        // tempLabel.style.background = "lightgray";
        // tempLabel.style.color = "darkgray";
        // tempField.style.background = "lightgray";
        // tempField.style.border = "lightgray";
        // tempField.style.color = "lightgray";
        // tempField.required = false;
        // tempField.readOnly = true;
    })

});


// document.getElementById('point_src').addEventListener('change', function() {

//     var selectedOption = this.value;

//     if(selectedOption != '') {

//         seeingLabel.style.background = "lightgray";
//         seeingLabel.style.color = "darkgray";
//         seeingField.style.background = "lightgray";
//         seeingField.style.border = "lightgray";
//         seeingField.style.color = "lightgray";
//         seeingField.required = false;
//         seeingField.readOnly = true;
//     }

//     else {

//         seeingLabel.style.background = "slategray";
//         seeingLabel.style.color = "white";
//         seeingField.style.background = "white";
//         seeingField.style.border = "white";
//         seeingField.style.color = "black";
//         seeingField.required = true;
//         seeingField.readOnly = false;
//     }
    
// });


// window.onload = change;

// function change() {


//     var selectedOption = document.getElementById('point_src').value;

//     if(selectedOption != '') {

//         seeingLabel.style.background = "lightgray";
//         seeingLabel.style.color = "darkgray";
//         seeingField.style.background = "lightgray";
//         // seeingField.style.border = "lightgray";
//         seeingField.style.color = "lightgray";
//         seeingField.required = false;
//         seeingField.readOnly = true;
//     }

//     else {

//         seeingLabel.style.background = "slategray";
//         seeingLabel.style.color = "white";
//         seeingField.style.background = "white";
//         // seeingField.style.border = "white";
//         seeingField.style.color = "black";
//         seeingField.required = true;
//         seeingField.readOnly = false;
//     }
    
// }