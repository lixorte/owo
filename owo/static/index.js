function toggleSidebar() {
    if (document.getElementById("sb").style.left === "-300px") {
        document.getElementById("sb").style.left = "0";
        document.getElementById("sb-btn-head").style.display = "none";
    } else {
        document.getElementById("sb").style.left = "-300px";
        document.getElementById("sb-btn-head").style.display = "block";
    }
}