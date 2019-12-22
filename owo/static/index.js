function toggleSidebar() {
    if (document.getElementById("sb").style.left === "-300px") {
        document.getElementById("sb").style.left = "0";
        document.getElementById("sb-btn-head").style.display = "none";
    } else {
        document.getElementById("sb").style.left = "-300px";
        document.getElementById("sb-btn-head").style.display = "block";
    }
}

function sendData() {
    if (document.getElementById("input-song-title").checkValidity() === false ||
        document.getElementById("input-song-author").checkValidity() === false) {
        document.getElementById("required-alert").style.display = "block";
        return;
    } else {
        document.getElementById("required-alert").style.display = "none";
    }

    let electionUid = "";
    let cookies = document.cookie;
    let jwt = cookies["JWT"];
    let addItemData = JSON.stringify($(".add-song").serializeArray());

    XMLHttpRequest.open("POST", "/election/" + electionUid + "/vote/new");
    XMLHttpRequest.setRequestHeader("Authorization", "Bearer " + jwt);
    XMLHttpRequest.send(addItemData);
}

function f() {

}