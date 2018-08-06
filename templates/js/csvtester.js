function onload(){
    document.getElementById("loading").style.display="none";
}

function checkupload(){
    var x = document.getElementById("csv");
    txt = "Select one or more files.";
    if ('files' in x) {
        if (x.files.length == 0) {
            txt = "Select one or more files.";
        } else {
            for (var i = 0; i < x.files.length; i++) {
                txt += "<br><strong>" + (i+1) + ". file</strong><br>";
                var file = x.files[i];
                if ('name' in file) {
                    txt += "name: " + file.name + "<br>";
                }
                if ('size' in file) {
                    txt += "size: " + file.size + " bytes <br>";
                }
            }
        }
    }else {
        if (x.value == "") {
            txt += "Select one or more files.";
        } else {
            txt += "The files property is not supported by your browser!";
            txt  += "<br>The path of the selected file: " + x.value; // If the browser does not support the files property, it will return the path of the selected file instead.
        }
    }
    document.getElementById("result").innerHTML = txt;
}

function csvUpload(){
    url="https://mccptester.herokuapp.com/csvupload";
    checkupload();
    var fd = new FormData();
    fd.append('data', document.getElementById("csv").files[0]);
    $.ajax({
      url: url,
      type: 'GET',
      processData: false,
      contentType: false,
      dataType: 'json',
      data:fd,
      success: function (data) {
        alert(data);
        document.getElementById("loading").style.display="none";
      },
      error: function(jqxhr, status, exception) {
          alert('Exception:', exception);
          document.getElementById("loading").style.display="none";
      }
    });
}
