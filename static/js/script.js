// ==============================
// Mobile Navigation
// ==============================

const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("nav-links");

if (menuToggle) {
    menuToggle.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });
}

// Close menu after clicking a link (mobile)

const links = document.querySelectorAll("#nav-links a");

links.forEach(link => {
    link.addEventListener("click", () => {
        if (window.innerWidth <= 768) {
            navLinks.classList.remove("active");
        }
    });
});


// ==============================
// Smooth Button Animation
// ==============================

const buttons = document.querySelectorAll(".btn");

buttons.forEach(btn => {
    btn.addEventListener("mouseenter", () => {
        btn.style.transform = "scale(1.05)";
    });

    btn.addEventListener("mouseleave", () => {
        btn.style.transform = "scale(1)";
    });
});