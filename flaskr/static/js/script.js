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
    // 0-9 minutes
    "Zero", "One", "Two", "Three", "Four",
    "Five", "Six", "Seven", "Eight", "Nine",

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

/**
 * Update the clock display with the current time in both digital and word formats.
 */
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

/**
 * Update the day cycle image based on the current time.
 * Displays a sun image during the day and a moon image during the night.
 */
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

/**
 * Automatically hide flash messages after a few seconds.
 * Flash messages are used to display notifications to the user.
 */
document.addEventListener('DOMContentLoaded', function() {
    const flashes = document.querySelectorAll('.flashes li');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            setTimeout(() => {
                flash.remove();
            }, 300); 
        }, 3000);
    });
});


function logMood(mood) {
    fetch('/log_mood', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood: mood })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error logging mood: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error logging mood');
    });
}

// Function to fetch user's IP address and send it to the backend
function setUserIp() {
    fetch('https://ipinfo.io/json')
        .then(response => response.json())
        .then(data => {
            const userIp = data.ip;
            fetch('/set_user_ip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ip: userIp })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('User IP set successfully');
                } else {
                    console.error('Error setting user IP:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        })
        .catch(error => {
            console.error('Error fetching IP:', error);
        });
}

// Call setUserIp function on every page load
window.addEventListener('load', setUserIp);


// Function to set custom location for testing
function testLocation(city, ip) {
    // Override the fetch for ipinfo.io
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
      if (url.includes('ipinfo.io')) {
        console.log(`Mocking location: ${city} with IP: ${ip}`);
        return Promise.resolve({
          json: () => Promise.resolve({
            ip: ip,
            city: city,
            region: "Test Region",
            country: "Test Country",
            loc: "51.5074,-0.1278", // Default to London coords
          })
        });
      }
      return originalFetch(url, options);
    };
    
    // Trigger the setUserIp function
    setUserIp();
    
    // Restore original fetch after 2 seconds
    setTimeout(() => {
      window.fetch = originalFetch;
      console.log("Location test complete. Refresh the page to see results.");
    }, 2000);
  }
  
  // Example locations to test
  const testLocations = {
    "London": "82.34.12.45",
    "New York": "74.125.45.100",
    "Tokyo": "123.45.67.89",
    "Sydney": "1.2.3.4",
    "Paris": "5.6.7.8"
  };
  
  console.log("Available test locations:");
  Object.keys(testLocations).forEach(city => {
    console.log(`- ${city}`);
  });
  console.log("Usage: testLocation('London', '82.34.12.45')");
  console.log("Or use a preset: testLocation('New York', testLocations['New York'])");