function character_count() {
    id_text = document.getElementById("id_text");
    text_characters = document.getElementById("text_characters");
    text_characters.innerHTML = id_text.value.length + "/1000 Characters";
}

function previewImages(input) {
    document.getElementById("previewImages").innerHTML = "";
    for(var i = 0; i < input.files.length; i++) {
        var src = URL.createObjectURL(input.files[i]);
        imgCode = '<img src="' + src + '"id="previewItem"/>';
        document.getElementById("previewImages").innerHTML += imgCode;
    }
  }