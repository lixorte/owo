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
    if (readCookie("access_token_cookie") !== null) {
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

function auth() {
    let link = "https://auth.eljur.ru/auth/hselyceum_ring?client_id=hselyceum_ring&response_type=code&redirect_uri=" + encodeURIComponent("http://" + window.location.hostname + "/auth") + "&state="
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