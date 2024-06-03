document.addEventListener("DOMContentLoaded", function () {
    // Function to detect and set text color based on background brightness
    function setTextColor(card) {
        var backgroundColor = window.getComputedStyle(card).backgroundColor;
        var rgb = backgroundColor.match(/\d+/g);
        var brightness = (parseInt(rgb[0]) * 299 + parseInt(rgb[1]) * 587 + parseInt(rgb[2]) * 114) / 1000;
        var textColor = (brightness > 125) ? "#000" : "#fff"; // Choose black or white text based on background brightness
        card.style.color = textColor;
    }

    // Call setTextColor function for each card
    var cards = document.querySelectorAll('.pr-card');
    cards.forEach(function (card) {
        setTextColor(card);
    });
});
