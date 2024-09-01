function Tab(e, name) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(name).style.display = "flex";
    e.currentTarget.className += " active";



    if(name == "target-point") {

        document.getElementById('source_type').value = "point";

        // readonly

        document.getElementById("ext_mag").value = "   01.  ";
        document.getElementById('ext_mag').readOnly = true;
        document.getElementById("dist").value = "   01.  ";
        document.getElementById('dist').readOnly = true;
        

        // reset
        document.getElementById("seeing-label").style.background = "slategray";
        document.getElementById("seeing-label").style.color = "white";
        document.getElementById("seeing").style.background = "white";
        document.getElementById("seeing").style.border = "white";
        document.getElementById("seeing").style.color = "black";

        //document.getElementById("seeing").value = document.getElementById("conditions").value;
        document.getElementById('seeing').readOnly = false;
        document.getElementById("seeing").value = "";
        document.getElementById('conditions').disabled = false;


        document.getElementById("star_temp").value = "";
        document.getElementById('star_temp').readOnly = false;
        document.getElementById("star_ab_mag").value = "";
        document.getElementById('star_ab_mag').readOnly = false;

        document.getElementById('point_src').disabled = false;

        document.getElementById('extended_src').required = false;





        // disable temperature

        document.getElementById('point_src').addEventListener('change', function() {

            var selectedOption = this.value;

            

            if(selectedOption != 'Blackbody') {

                alert("change");
                document.getElementById("star_temp-label").style.background = "lightgray";
                document.getElementById("star_temp-label").style.color = "darkgray";
                document.getElementById("star_temp").style.background = "lightgray";
                document.getElementById("star_temp").style.border = "lightgray";
                document.getElementById("star_temp").style.color = "lightgray";

                document.getElementById("star_temp").value = "   01.  ";
                document.getElementById('star_temp').readOnly = true;
                }
            
            
        });


    }
    else {

        document.getElementById('source_type').value = "extended";

        //readonly

        document.getElementById("seeing-label").style.background = "lightgray";
        document.getElementById("seeing-label").style.color = "darkgray";
        document.getElementById("seeing").style.background = "lightgray";
        document.getElementById("seeing").style.border = "lightgray";
        document.getElementById("seeing").style.color = "lightgray";

        document.getElementById("seeing").value = "   01.  ";
        document.getElementById('seeing').readOnly = true;
        document.getElementById('conditions').disabled = true;

        document.getElementById('point_src').disabled = true;


        document.getElementById("star_temp").value = "   01.  ";
        document.getElementById('star_temp').readOnly = true;
        document.getElementById("star_ab_mag").value = "   01.  ";
        document.getElementById('star_ab_mag').readOnly = true;
        

        // reset

        document.getElementById("ext_mag").value = "";
        document.getElementById('ext_mag').readOnly = false;
        document.getElementById("dist").value = "";
        document.getElementById('dist').readOnly = false;

        document.getElementById('extended_src').required = true;
        
    }
}         

document.getElementById("defaultOpen").click();





Tab()