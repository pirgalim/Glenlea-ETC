var cameraPresets;
var telescopePresets;

function setup(cameras, telescopes) {

    cameraPresets = cameras;
    telescopePresets = telescopes;
}

const sensor_x = document.getElementById('sensor_x').value;
const sensor_y = document.getElementById('sensor_y').value

const px_size = document.getElementById('px_size').value;
const q_efficiency = document.getElementById('q_efficiency').value;
const read_noise = document.getElementById('read_noise').value;
const gain = document.getElementById('gain').value;
const offset = document.getElementById('offset').value;
const dark_noise = document.getElementById('dark_noise').value;
const full_well = document.getElementById('full_well').value;





document.getElementById('camera').addEventListener('change', function() {

    const select = document.getElementById('camera');
    var presets = cameraPresets;
    var preset;

    console.log(presets)

    // match the selection with a preset
    for( let i = 0; i < presets.length; i++ ) {
        if( presets[i]['name'] == select.value ) { preset = presets[i]; }
    }
   
    // autofill the values
    if(select.value != '') {
        document.getElementById('sensor_x').value = preset['sensor_x'];
        document.getElementById('sensor_y').value = preset['sensor_y'];
        document.getElementById('px_size').value = preset['px_size'];
        document.getElementById('q_efficiency').value = preset['q_efficiency'];
        document.getElementById('read_noise').value = preset['read_noise'];
        document.getElementById('gain').value = preset['gain'];
        document.getElementById('offset').value = preset['offset'];
        document.getElementById('dark_noise').value = preset['dark_noise'];
        document.getElementById('full_well').value = preset['full_well'];




        const pixelSize = parseFloat( document.getElementById('px_size').value );
        const focalLength = parseFloat( document.getElementById('scope_focal').value ) * 1000; // converting focalLength to mm
        pixelScale = ( pixelSize/focalLength )  * 206.265;
        if(pixelScale) {
            document.getElementById('plate_scale').value =   Math.round(pixelScale * 100) / 100; // round to 2 decimal places

            console.log("should change");
        }
    }
    else {
        document.getElementById('sensor_x').value = '';
        document.getElementById('sensor_y').value = '';
        document.getElementById('px_size').value = '';
        document.getElementById('q_efficiency').value = '';
        document.getElementById('read_noise').value = '';
        document.getElementById('gain').value = '';
        document.getElementById('offset').value = '';
        document.getElementById('dark_noise').value = '';
        document.getElementById('full_well').value = '';
    }

    
});





document.getElementById('telescope').addEventListener('change', function() {

    const select = document.getElementById('telescope');
    var presets = telescopePresets;
    var preset;

    // match the selection with a preset
    for( let i = 0; i < presets.length; i++ ) {
        if( presets[i]['name'] == select.value ) { preset = presets[i]; }
    }
   
    // autofill the values
    if(select.value != '') {
        document.getElementById('scope_dia').value = preset['scope_dia'];
        document.getElementById('scope_focal').value = preset['scope_focal'];


        const pixelSize = parseFloat( document.getElementById('px_size').value );
        const focalLength = parseFloat( document.getElementById('scope_focal').value ) * 1000; // converting focalLength to mm

       
        pixelScale = ( pixelSize/focalLength )  * 206.265;
        if(pixelScale) {
            document.getElementById('plate_scale').value =   Math.round(pixelScale * 100) / 100; // round to 2 decimal places
        }
        
    }
    else {
        document.getElementById('scope_dia').value = '';
        document.getElementById('scope_focal').value = '';
        document.getElementById('plate_scale').value = '';
    }
});



//TODO: run setup here instead