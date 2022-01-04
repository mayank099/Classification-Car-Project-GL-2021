
/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
        const formData = new FormData();
        formData.append('file', input.files[0]);
        console.log("Image: ", formData.get('file'));
        $.ajax({
            type:'POST',
            url: "http://127.0.0.1:5000/image-upload",
            data: formData,
            enctype: "multipart/form-data",
            contentType: false,
            processData: false,
            success:function(data) {
                console.log("success");
                console.log(data);
                $('#classify-image').text("Image Classification: " + data[1])
            },
            error: function(data) {
                console.log("error");
                console.log(data);
            }
        });
    });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById( 'upload' );
var infoArea = document.getElementById( 'upload-label' );

input.addEventListener( 'change', showFileName );
function showFileName( event ) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = 'File name: ' + fileName;
}
