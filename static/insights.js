console.log("Insights dashboard loaded");
const cards = document.querySelectorAll(".card");

cards.forEach(card => {
    card.addEventListener("mouseenter", () => {
        card.style.transform = "translateY(-6px) scale(1.01)";
        card.style.transition = "transform 0.25s ease";
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0) scale(1)";
    });
});

const bubbles = document.querySelectorAll(".bubble");

bubbles.forEach((bubble, index) => {
    bubble.style.animationDelay = `${index * 0.4}s`;
});
