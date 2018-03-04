(function() {

    // Also see .name, .type }); 

    var browseButton = null;
    var answerBox = null;

    function startup() {
        browseButton = document.getElementById('browsebutton');
        answerBox = document.getElementById('answerbox');

        browseButton.addEventListener('change', function(ev){
            var file = this.files[0];
            var isvalid = filevalid(file);
            if (isvalid == 0) {
                // ok
                var formData = new FormData();
                //formData.append('photo', file);
                formData = new FormData($('#upload-file')[0]); 

                answerBox.innerHTML = "Uploading...";
                $.ajax({
                    url: $SCRIPT_ROOT + '/_lookup_lookupface', 
                    type: "POST", 
                    cache: false,
                    contentType: false,
                    processData: false,
                    async: false,
                    data: formData,

                    success: function (response){
                        var error = response.error;
                        var errormsg = response.errormsg;
                        if (error) {
                            answerBox.innerHTML = errormsg;
                        } else {
                            answerBox.innerHTML = response.url;
                        }
                    }
                })
                    .done(function(e){
                        //alert('done');
                    }); 

                // do the upload
            } else if (isvalid == 1) {
                answerBox.innerHTML = "File must be an image";
            } else if (isvalid == 2) {
                answerBox.innerHTML = "Max upload size is 10Mb";
            } else {
                answerBox.innerHTML = "Unknown error; please try again";
            }

            ev.preventDefault();
        }, false); 
    }

    function filevalid(file) {
        if (file.type.match(/^image\//i)) {
            if (file.size > 1024*1024*10) {
                return 2;
            } else {
                return 0;
            }
        } else {
            return 1;
        }
    }

    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener('load', startup, false);
})();


