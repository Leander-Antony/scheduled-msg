document.addEventListener("DOMContentLoaded", function () {
    const datetimeInput = document.getElementById('datetime');
    const now = new Date();
    const formattedDate = now.toISOString().slice(0, 16); 
    datetimeInput.setAttribute("min", formattedDate);
});

document.getElementById('emailForm').addEventListener('submit', function (event) {
    const datetimeInput = document.getElementById('datetime').value;
    const userDatetime = new Date(datetimeInput);
    const now = new Date();

    if (userDatetime <= now) {
        alert("Please select a time in the future.");
        event.preventDefault(); 
    } else {
        event.preventDefault(); 
        showPopup(); 
        setTimeout(function () {
            event.target.submit(); 
        }, 3000); 
    }
});


function showPopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'block';
}


function closePopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'none';
}
