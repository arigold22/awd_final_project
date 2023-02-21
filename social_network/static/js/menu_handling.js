
function toggleMenu(){
    if(document.getElementById("mobileMenu").style.display == "flex"){
        document.getElementById("mobileMenu").style.display = "none";
        
    }else{
    document.getElementById("mobileMenu").style.display = "flex";
    document.getElementById("mobileMenu").style.flexDirection = "column";
    }
}

window.onresize = function(event) {
    if(window.innerWidth >= 768){
    document.getElementById("mobileMenu").style.display = "none";
    }
};
