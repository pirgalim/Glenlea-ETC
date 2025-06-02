//TODO: clean up the file


// const buttons = document.getElementsByClassName(tablinks);



//  <button class="tablinks" type="button" onclick="Tab(event, 'target-point')" id="defaultOpen" style="border-top-left-radius:5px;">Point Source</button>


document.getElementById("defaultOpen").addEventListener("click", function() {

    Tab(this, 'target-point')

});

document.getElementById("defaultClose").addEventListener("click", function() {

    Tab(this, 'target-extended')

});




function Tab(button, name) {

    let i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");


    // the for loop is here in case another tab is added in the future
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");

    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(name).style.display = "flex";
    button.classList.add("active");



    if(name == "target-point") {

        document.getElementById('source_type').value = "point";

        // readonly

        document.getElementById("ext_mag").required = false;
        document.getElementById('ext_mag').readOnly = true;

        document.getElementById('star_ab_mag').required = true;
        document.getElementById('star_ab_mag').readOnly = false;

        document.getElementById('point_src').disabled = false;

        document.getElementById('extended_src').required = false;                       


    }
    else {  // extended sources

        document.getElementById('source_type').value = "extended";

        //readonly


        document.getElementById('point_src').disabled = true;
        document.getElementById('star_ab_mag').required = false;
        document.getElementById('star_ab_mag').readOnly = true;
        

        // reset

        document.getElementById("ext_mag").required = true;
        document.getElementById('ext_mag').readOnly = false;

        document.getElementById('extended_src').required = true;
        
    }
}         

    document.getElementById("defaultOpen").click();
                