const pointSource = document.getElementById("defaultOpen");
const extendedSource = document.getElementById("defaultClose");



pointSource.addEventListener("click", point);
extendedSource.addEventListener("click", extended);




function point() {

    document.getElementById('source_type').value = "point";

    // readonly

    document.getElementById("ext_mag").required = false;
    document.getElementById('ext_mag').readOnly = true;


    //document.getElementById("dist").value = "   01.  ";
    //document.getElementById('dist').readOnly = true;
    

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


    document.getElementById("star_temp").required = true;
    document.getElementById('star_temp').readOnly = false;
    
    //document.getElementById("star_ab_mag").value = "";

    document.getElementById('star_ab_mag').required = true;
    document.getElementById('star_ab_mag').readOnly = false;



    document.getElementById('point_src').disabled = false;


    document.getElementById('extended_src').required = false;


}





function extended() {


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


        document.getElementById("star_temp").required = false;
        document.getElementById('star_temp').readOnly = true;


        //document.getElementById("star_ab_mag").value = "   01.  ";
        document.getElementById('star_ab_mag').required = false;
        document.getElementById('star_ab_mag').readOnly = true;
        

        // reset

        document.getElementById("ext_mag").required = true;
        document.getElementById('ext_mag').readOnly = false;

        //document.getElementById("dist").value = "";
        //document.getElementById('dist').readOnly = false;

        document.getElementById('extended_src').required = true;
}


