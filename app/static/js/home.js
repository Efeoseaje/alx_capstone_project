// Wait for the DOM to fully load before executing the JavaScript code
document.addEventListener('DOMContentLoaded', function () {
  // Select the profile icon and profile dropdown elements
  const profileIcon = document.querySelector('.profile-icon');
  const profileDropdown = document.querySelector('.profile-dropdown');

  // Show the profile dropdown when the mouse enters the profile icon
  profileIcon.addEventListener('mouseenter', () => {
    profileDropdown.style.display = 'block';
  });

  // Hide the profile dropdown when the mouse leaves the profile dropdown itself
  profileDropdown.addEventListener('mouseleave', () => {
    profileDropdown.style.display = 'none';
  });

  // Set up the FullCalendar component
  const calendarEl = document.getElementById('calendar');
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    editable: true,
    selectable: true,
    events: [], // Initialize with an empty array
    displayEventTime: false, // Hide event times on the calendar

    // Handle date clicks (single or double click)
    dateClick: function (info) {
      const currentTime = new Date().getTime();
      if (currentTime - (calendar.lastClickTime || 0) < 300) {
        // When a date is double-clicked, show the event overlay
        document.getElementById('eventOverlay').style.display = 'flex';
      } else {
        calendar.lastClickTime = currentTime;
      }
    }
  });

  // Render the calendar
  calendar.render();

  // Function to display an alert overlay with a given message
  function showAlert (message) {
    const alertOverlay = document.getElementById('alertOverlay');
    const alertMessage = document.getElementById('alertMessage');
    const okButton = document.getElementById('okButton');
    alertMessage.textContent = message;
    alertOverlay.style.display = 'flex';

    // Event listener for closing the alert overlay
    okButton.addEventListener('click', function () {
      alertOverlay.style.display = 'none';
      // Show the event overlay again after closing the alert
      document.getElementById('eventOverlay').style.display = 'flex';
    });
  }

  // Event listener for the "Create Event" button
  document.getElementById('createEvent').addEventListener('click', function () {
    // Get event details from the form
    const eventTitle = document.getElementById('eventTitle').value;
    const eventStartDate = document.getElementById('eventStartDate').value;
    const eventStartTime = document.getElementById('eventStartTime').value;
    const eventEndDate = document.getElementById('eventEndDate').value;
    const eventEndTime = document.getElementById('eventEndTime').value;
    const eventDescription = document.getElementById('eventDescription').value;

    // Check if the required fields are filled
    if (eventTitle && eventStartDate && eventStartTime && eventEndDate && eventEndTime) {
      // Create JavaScript Date objects from date and time inputs
      const startDate = new Date(`${eventStartDate}T${eventStartTime}`);
      const endDate = new Date(`${eventEndDate}T${eventEndTime}`);

      // Check if the start date is before the end date
      if (startDate < endDate) {
        // Create an event object
        const eventData = {
          title: eventTitle,
          start: startDate.toISOString(),
          end: endDate.toISOString(),
          description: eventDescription,
        };

        // Add the event to the calendar
        calendar.addEvent(eventData);

        console.log(eventData);
        // Hide the event overlay after creating the event
        document.getElementById('eventOverlay').style.display = 'none';

        // Clear the form inputs
        document.getElementById('eventForm').reset();

        console.log('before');
        fetch('/create_event', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(eventData)
        })
          .then(response => response.json())
          .then(data => {
            console.log(data); // Response from Flask server
          })
          .catch(error => {
            console.error(error);
          });
        console.log('after');
      } else {
        showAlert('Start date must be less than the end date.');
      }

      // Function to check if today's date falls within an event's date range
      function isTodayWithinEventDateRange (event) {
        const today = new Date().toISOString().split('T')[0];
        return today >= event.start.toISOString().split('T')[0] && today <= event.end.toISOString().split('T')[0];
      }

      // Function to display today's events
      function displayTodayEvents () {
        const events = calendar.getEvents();
        const todayEvents = events.filter(isTodayWithinEventDateRange);

        const eventsTodayDiv = document.getElementById('eventsToday');
        eventsTodayDiv.innerHTML = ''; // Clear existing content

        if (todayEvents.length > 0) {
          todayEvents.forEach((event) => {
            // Create event details elements
            const eventDetails = document.createElement('div');
            eventDetails.classList.add('event-details');

            const eventTitle = document.createElement('h3');
            eventTitle.textContent = event.title;

            const eventStart = document.createElement('p');
            eventStart.textContent = `Start Date & Time: ${event.start.toLocaleString()}`;

            const eventEnd = document.createElement('p');
            eventEnd.textContent = `End Date & Time: ${event.end.toLocaleString()}`;

            const eventDescription = document.createElement('p');
            eventDescription.textContent = event.description;

            // Append event details to the eventsTodayDiv
            eventDetails.appendChild(eventTitle);
            eventDetails.appendChild(eventStart);
            eventDetails.appendChild(eventEnd);
            eventDetails.appendChild(eventDescription);
            eventsTodayDiv.appendChild(eventDetails);
          });
        } else {
          eventsTodayDiv.innerHTML = 'No events today.';
        }
      }

      // Initial display of today's events or "No events today"
      displayTodayEvents();

      // Listen to changes in the calendar (e.g., events added/removed) and update displayed events
      calendar.on('eventAdd', displayTodayEvents);
      calendar.on('eventRemove', displayTodayEvents);
    }
  });

  // Event listener for the "Cancel Event" button
  document.getElementById('cancelEvent').addEventListener('click', function () {
    // Clear the form inputs and hide the event overlay
    document.getElementById('eventForm').reset();
    document.getElementById('eventOverlay').style.display = 'none';
  });
});
