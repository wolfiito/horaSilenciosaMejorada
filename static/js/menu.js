const   cloud        = document.getElementById("cloud"),
        barraLateral = document.querySelector(".barra-lateral"),
        spans        = document.querySelectorAll("span"),
        palanca      = document.querySelector(".switch"),
        circulo      = document.querySelector(".circulo"),
        menu         = document.querySelector(".menu"),
        main         = document.querySelector("main"),
        navBar       = document.querySelector(".nav-bar");

const isDarkMode = localStorage.getItem("darkMode") === "true";

const toggleDarkMode = () => {
    let body = document.body;
    body.classList.toggle("dark-mode");
    const currentMode = body.classList.contains("dark-mode") ? "true" : "false";
    localStorage.setItem("darkMode", currentMode);
    circulo.classList.toggle("prendido");
};

if (isDarkMode) {
    toggleDarkMode();
}

menu.addEventListener("click", () => {
    barraLateral.classList.toggle("max-barra-lateral");
    if (barraLateral.classList.contains("max-barra-lateral")) {
        // menu.children[0].style.display = "none";
        // menu.children[1].style.display = "block";
        navBar.style.backgroundColor     = "var(--color-bg-header-dark)";
        // navBar.style.color               = "var(--color-txt-header)";
        // menu.style.color                 = "var(--color-txt-header)";
    } else {
        // menu.children[0].style.display = "block";
        // menu.children[1].style.display = "none";
        navBar.style.backgroundColor     = "var(--color-bg-header-light)";
        // navBar.style.color               = "var(--color-txt-light)";
        // menu.style.color                 = "var(--color-txt-light)";
    }
    // if (window.innerWidth <= 320) {
    //     barraLateral.classList.add("mini-barra-lateral");
    //     main.classList.add("min-main");
    //     spans.forEach((span) => {
    //         span.classList.add("oculto");
    //     });
    // }
});

palanca.addEventListener("click", toggleDarkMode);

cloud.addEventListener("click", () => {
    barraLateral.classList.toggle("mini-barra-lateral");
    main.classList.toggle("min-main");
    spans.forEach((span) => {
        span.classList.toggle("oculto");
    });
});