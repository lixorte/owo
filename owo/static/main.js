const address = "http://keddad.wtf";

function toggleSidebar() {
    if (!document.cookie.hasOwnProperty("isAdmin")) {
        console.log("pidoras");
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

function sendData() {
    if (document.getElementById("input-song-title").checkValidity() === false ||
        document.getElementById("input-song-author").checkValidity() === false) {
        document.getElementById("required-alert").style.display = "block";
        return;
    } else {
        document.getElementById("required-alert").style.display = "none";
    }

    fetch(address + "/election/getlast/song")
        .then(response => response.json())
        .then(dataa => dataa)
        .catch(error => console.log(error));
    console.log(data);
    let electionUid = data["electionInfo"]["id"];
    let addItemData = JSON.stringify($(".add-song").serializeArray());
    fetch(address + "/election/" + electionUid + "/vote/new", {
        method: "POST",
        credentials: "include",
        mode: 'no-cors',
        body: {
            addItemData
        }
    }).catch(error => console.log(error))
}

function auth() {
    let link = "https://auth.eljur.ru/auth/hselyceum_ring?client_id=hselyceum_ring&response_type=code&redirect_uri=http%3A%2F%2Fkeddad.wtf%2Fauth&state="
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