const timeElement = document.getElementById('time');
const wordTimeElement = document.getElementById('wordTime');

// Fully hardcoded arrays
const hoursArray = [
    "Twelve", "One", "Two", "Three", "Four",
    "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven"
];

const zeroToNineWords = [
    "Zero", "One", "Two", "Three", "Four",
    "Five", "Six", "Seven", "Eight", "Nine"
];

const minutesArray = [
    // 0-9 minutes (not used in this array)
    '', '', '', '', '', '', '', '', '', '',

    // 10-19 minutes
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
    "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen",

    // 20-29 minutes
    "Twenty", "Twenty One", "Twenty Two", "Twenty Three", "Twenty Four",
    "Twenty Five", "Twenty Six", "Twenty Seven", "Twenty Eight", "Twenty Nine",

    // 30-39 minutes
    "Thirty", "Thirty One", "Thirty Two", "Thirty Three", "Thirty Four",
    "Thirty Five", "Thirty Six", "Thirty Seven", "Thirty Eight", "Thirty Nine",

    // 40-49 minutes
    "Forty", "Forty One", "Forty Two", "Forty Three", "Forty Four",
    "Forty Five", "Forty Six", "Forty Seven", "Forty Eight", "Forty Nine",

    // 50-59 minutes
    "Fifty", "Fifty One", "Fifty Two", "Fifty Three", "Fifty Four",
    "Fifty Five", "Fifty Six", "Fifty Seven", "Fifty Eight", "Fifty Nine"
];

function updateClock() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();

    // Digital time
    timeElement.textContent = hours + ':' + (minutes < 10 ? '0' : '') + minutes;

    // Word time
    const hourWord = hoursArray[hours % 12];
    let minuteWord;
        if (minutes === 0) {
            minuteWord = "O'Clock";
        } else if (minutes < 10) {
            minuteWord = "o'" + zeroToNineWords[minutes];
        } else {
            minuteWord = minutesArray[minutes];
        }

    wordTimeElement.textContent = `${hourWord} ${minuteWord}`;
}

// Initial update and interval
updateClock();
setInterval(updateClock, 1000);

function updateDayCycleImage() {
    var now = new Date();
    var hours = now.getHours();
    var imgElement = document.getElementById('dayCycleImg');
    var sunUrl = imgElement.getAttribute('data-sun-url');
    var moonUrl = imgElement.getAttribute('data-moon-url');
    if (hours >= 6 && hours < 18) {
        imgElement.src = sunUrl;
    } else {
        imgElement.src = moonUrl;
    }
    console.log('Day cycle image updated');
}
// Update the image when the page loads
updateDayCycleImage();

// Update the image every minute
setInterval(updateDayCycleImage, 60000);
