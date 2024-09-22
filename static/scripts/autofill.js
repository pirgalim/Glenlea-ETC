var cameraPresets;
var telescopePresets;

function setup(cameras, telescopes) {

    cameraPresets = cameras;
    telescopePresets = telescopes;
}




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
        document.getElementById('plate_scale').value = preset['plate_scale'];
    }
    else {
        document.getElementById('scope_dia').value = '';
        document.getElementById('scope_focal').value = '';
        document.getElementById('plate_scale').value = '';
    }
});






// document.getElementById('telescope').addEventListener('change', function() {

//     var presets = telescopePresets;
//     var size = presets[0][1].length;

//     // I should check if there is actually anything here first
//     var preset = [size]

//     for(let i = 0; i < size; i++) { preset[i] = ''; }

//     // match the selection with a preset
//     for( let i = 0; i < presets.length; i++ ) {
//         if( presets[i][0] == document.getElementById('telescope').value ) { preset = presets[i][1]; }
//     }

//     document.getElementById('scope_dia').value = preset[0];
//     document.getElementById('scope_focal').value = preset[1];
//     document.getElementById('plate_scale').value = preset[2];

// });

