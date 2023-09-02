// function to limit the choice of datetime bar a minimum of current time and a maximum of 16days in the future
window.addEventListener("load", function() {

const datetimeInput = document.getElementById("datetime");
const now = new Date();

// Set the minimum value to the current date and time
datetimeInput.setAttribute("min", now.toISOString().slice(0, 11)+"00:00");

// Set the maximum value to one week from now
const maxDate = new Date(now.getTime() + 16 * 24 * 60 * 60 * 1000);
datetimeInput.setAttribute("max", maxDate.toISOString().slice(0, 11)+"00:00");
})