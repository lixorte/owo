function readCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function toggleSidebar() {
    if (readCookie("isAdmin") !== 'true') {
        console.log("я ненавижу веб я хочу чтобы он умер натурал тупой");
        document.getElementById("adminu").style.display = "none";
        document.getElementById("adminv").style.display = "none";
    }
    if (document.cookie.hasOwnProperty("access_token_cookie")) {
        document.getElementById("auth").innerText = "Выйти";
    }
    if (window.getComputedStyle(document.getElementById("sb"), null).getPropertyValue("left") === "-300px") {
        document.getElementById("sb").style.left = "0";
        document.getElementById("darken").style.opacity = "60%";
        document.getElementById("darken").style.zIndex = "1";
        document.getElementById("sb-btn-head").style.display = "none";
    } else {
        document.getElementById("sb").style.left = "-300px";
        document.getElementById("darken").style.opacity = "0";
        setTimeout(function () {
            document.getElementById("darken").style.zIndex = "-1"
        }, 500);
        document.getElementById("sb-btn-head").style.display = "block";
    }
}

function getData() {
    return fetch("/election/getlast/song")
        .then(response => response.json())
        .then(result => result)
        .catch(error => console.log(error));
}

function sendData() {
    if (document.getElementById("input-song-title").checkValidity() === false ||
        document.getElementById("input-song-author").checkValidity() === false) {
        document.getElementById("required-alert").style.display = "block";
        return;
    } else {
        document.getElementById("required-alert").style.display = "none";
    }
    let jsondata;
    getData().then(result => jsondata = result);
    console.log(jsondata);
    let electionUid = jsondata["electionInfo"]["id"];
    let addItemData = JSON.stringify($(".add-song").serializeArray());
    fetch("/election/" + electionUid + "/vote/new", {
        method: "POST",
        credentials: "include",
        headers: {
            'Content-Type': 'application/json',
        },
        body: addItemData
    }).catch(error => console.log(error))
}

function auth() {
    let link = "https://auth.eljur.ru/auth/hselyceum_ring?client_id=hselyceum_ring&response_type=code&redirect_uri=" + encodeURIComponent(window.location.hostname + "/auth") + "&state="
        + encodeURIComponent(window.location.pathname);
    window.open(link);
}

function color(element) {
    if (document.getElementById(element.id).style.backgroundColor === "#ffffff") {
        document.getElementById(element.id).style.backgroundColor = "#000000";
    } else {
        document.getElementById(element.id).style.backgroundColor = "#ffffff"
    }
}