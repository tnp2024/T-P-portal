document.addEventListener('DOMContentLoaded', function () {
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const cardBody = document.querySelector('.drive_card-body.hidden');

    dropdownBtn.addEventListener('click', function () {
        if (cardBody.style.display === 'block') {
            cardBody.style.display = 'none';
        } else {
            cardBody.style.display = 'block';
        }
    });

    // Close form when clicking outside
    window.addEventListener('click', function (event) {
        if (!dropdownBtn.contains(event.target) && !cardBody.contains(event.target)) {
            cardBody.style.display = 'none';
        }
    });
});