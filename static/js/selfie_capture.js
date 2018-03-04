(function() {


    // The width and height of the captured photo. We will set the
    // width to the value defined here, but the height will be
    // calculated based on the aspect ratio of the input stream.

    var width = 320;    // We will scale the photo width to this
    var height = 0;     // This will be computed based on the input stream

    // |streaming| indicates whether or not we're currently streaming
    // video from the camera. Obviously, we start at false.

    var streaming = false;

    // The various HTML elements we need to configure or control. These
    // will be set by the startup() function.

    var player = null;
    var canvas = null;
    var photo = null;
    var captureButton = null;
    var usePhotoButton = null;
    var photoData = null;

    var photoTaken = false;

    function startup() {
        player = document.getElementById('player');
        canvas = document.getElementById('canvas');
        context = canvas.getContext('2d');
        captureButton = document.getElementById('capture');
        usePhotoButton = document.getElementById('use_photo');
        photo = document.getElementById('photo'); 

        usePhotoButton.disabled = true;

        const constraints = {
            video: true,
            audio: false
        };


        player.addEventListener('canplay', function(ev){
            if (!streaming) {
                height = player.videoHeight / (player.videoWidth/width);

                // Firefox currently has a bug where the height can't be read from
                // the video, so we will make assumptions if this happens.

                if (isNaN(height)) {
                    height = width / (4/3);
                }

                player.setAttribute('width', width);
                player.setAttribute('height', height);
                canvas.setAttribute('width', width);
                canvas.setAttribute('height', height);
                streaming = true;
            } }, false); 

        captureButton.addEventListener('click', function(ev){
            if (photoTaken) {
                retrypicture();
            } else {
                takepicture();
            }
            ev.preventDefault();
        }, false); 

        navigator.mediaDevices.getUserMedia(constraints)
            .then((stream) => {
                // Attach the video stream to the video element and autoplay.
                player.srcObject = stream; }); //

        usePhotoButton.addEventListener('click', function(ev){
            if (photoTaken) {
                usethisphoto();
            }
            ev.preventDefault();
        }, false); 
    }

    // Capture a photo by fetching the current contents of the video
    // and drawing it into a canvas, then converting that to a PNG
    // format data URL. By drawing it on an offscreen canvas and then
    // drawing that to the screen, we can change its size and/or apply
    // other changes before drawing it.

    function takepicture() {

        var context = canvas.getContext('2d');
        if (width && height) {
            canvas.width = width;
            canvas.height = height;
            context.drawImage(player, 0, 0, width, height);

            photoData = canvas.toDataURL('image/png');
            //photo.setAttribute('src', data);

            // Stop all video streams.
            player.srcObject.getVideoTracks().forEach(track => track.stop()); 
            photoTaken = true;
            usePhotoButton.disabled = false;
            captureButton.innerHTML = "Clear photo and try again"
        } else {
        }
    }

    function retrypicture() {

        // clear photoData
        photoData = null;

        photoTaken = false;
        usePhotoButton.disabled = true;
        captureButton.innerHTML = "Take photo"
        //
        // Restart all video streams.
        const constraints = {
            video: true,
            audio: false
        };
        navigator.mediaDevices.getUserMedia(constraints)
            .then((stream) => {
                // Attach the video stream to the video element and autoplay.
                player.srcObject = stream; }); //
    }

    function usethisphoto() {
        // https://stackoverflow.com/questions/34779799/upload-base64-image-with-ajax 
        var formData = new FormData();
        formData.append('photo',photoData);

        $.ajax({
            url: $SCRIPT_ROOT + '/_registration_testimage', 
            type: "POST", 
            cache: false,
            contentType: false,
            processData: false,
            data: formData,
            success: function (response){
                var error = response.error;
                if (error) {
                    // handle error
                    $("#photomessage").text("error: ...");
                } else {
                    // show url registration form
                    $("#photomessage").text("Nice picture!");
                    usePhotoButton.disabled = true;
                    captureButton.disabled = true;
                    document.getElementById('urlarea').style.display = "inline";
                }
            }
        })
            .done(function(e){
                //alert('done');
            }); 

        //$.getJSON($SCRIPT_ROOT + '/_registration_testimage', {
        //photo_data: "photoData" // later remove quotes
      //}, function(data) {
        //$("#result").text(data.msg);
      //});


    }

    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener('load', startup, false);
})();

