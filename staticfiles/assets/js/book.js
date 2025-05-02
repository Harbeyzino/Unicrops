$(document).ready(function () {
    const reasonSelect = $('#appointment_reason');
    const customReasonContainer = $('#custom_reason_container');
    const customReasonInput = $('#custom_reason');

    // Show custom input field when "Other" is selected
    reasonSelect.change(function () {
      if ($(this).val() === 'Other') {
        customReasonContainer.show();
        customReasonInput.prop('required', true);
      } else {
        customReasonContainer.hide();
        customReasonInput.prop('required', false);
        customReasonInput.val(''); // Clear the custom reason input
      }
    });

    const contactMethodInput = $('#contact_method');
    const phoneNumberContainer = $('#phone_number_container');
    const phoneNumberInput = $('#phone_number');
    const whatsappContactContainer = $('#whatsapp_contact_container');
    const whatsappContactInput = $('#whatsapp_contact');

    // Handle contact method selection
    $('.contact-method-btn').click(function () {
      $('.contact-method-btn').removeClass('active'); // Remove active class from all buttons
      $(this).addClass('active'); // Add active class to the clicked button
      contactMethodInput.val($(this).data('value'));

      // Show phone number input if "Phone Call" is selected
      if ($(this).data('value') === 'phone') {
        phoneNumberContainer.show();
        phoneNumberInput.prop('required', true);
        whatsappContactContainer.hide();
        whatsappContactInput.prop('required', false);
        whatsappContactInput.val(''); // Clear WhatsApp input
      }
      // Show WhatsApp contact input if "WhatsApp Call" is selected
      else if ($(this).data('value') === 'whatsapp') {
        whatsappContactContainer.show();
        whatsappContactInput.prop('required', true);
        phoneNumberContainer.hide();
        phoneNumberInput.prop('required', false);
        phoneNumberInput.val(''); // Clear phone number input
      } else {
        phoneNumberContainer.hide();
        phoneNumberInput.prop('required', false);
        phoneNumberInput.val(''); // Clear phone number input
        whatsappContactContainer.hide();
        whatsappContactInput.prop('required', false);
        whatsappContactInput.val(''); // Clear WhatsApp input
      }
    });

    // Automatically format phone and WhatsApp numbers
    phoneNumberInput.on('input', function () {
      let value = $(this).val();
      if (value.startsWith('0')) {
        $(this).val(value.replace(/^0/, '')); // Remove leading 0
      }
    });

    whatsappContactInput.on('input', function () {
      let value = $(this).val();
      if (value.startsWith('0')) {
        $(this).val(value.replace(/^0/, '')); // Remove leading 0
      }
    });

    // Ensure formatted numbers appear on other pages
    $('#appointment-form').on('submit', function () {
      if (contactMethodInput.val() === 'phone') {
        const formattedPhoneNumber = '+234' + phoneNumberInput.val();
        phoneNumberInput.val(formattedPhoneNumber); // Prepend +234 before submission
      } else if (contactMethodInput.val() === 'whatsapp') {
        const formattedWhatsAppNumber = '+234' + whatsappContactInput.val();
        whatsappContactInput.val(formattedWhatsAppNumber); // Prepend +234 before submission
      }
    });

    let currentStep = 1;

    // Handle progress bar updates
    function updateProgressBar(step) {
      $('.progress-bar-step').each(function (index) {
        const stepIndex = index + 1;
        if (stepIndex < step) {
          $(this).addClass('completed').removeClass('active inactive loading');
          $(this).find('.loading-circle').remove();
        } else if (stepIndex === step) {
          $(this).addClass('active').removeClass('completed inactive loading');
        } else {
          $(this).addClass('inactive').removeClass('completed active loading');
          $(this).find('.loading-circle').remove();
        }
      });

      // Show or hide the "Previous" button
      if (step > 1) {
        $('#prevBtn').show();
      } else {
        $('#prevBtn').hide();
      }
    }

    // Show next step with spinner
    $('#nextBtn').click(function () {
      if (currentStep < 3) {
        const currentStepElement = $(`#step-${currentStep}`);
        const nextStepElement = $(`#step-${currentStep + 1}`);
        const currentProgressStep = $('.progress-bar-step').eq(currentStep - 1);

        // Add spinner to the current step
        currentProgressStep.addClass('loading');
        currentProgressStep.find('.step-number').append('<div class="loading-circle"></div>');

        setTimeout(() => {
          currentStepElement.hide();
          currentStep++;
          nextStepElement.show();
          updateProgressBar(currentStep);
          currentProgressStep.removeClass('loading');
          currentProgressStep.find('.loading-circle').remove();
        }, 1000); // Simulate loading delay
      }
    });

    // Show previous step
    $('#prevBtn').click(function () {
      if (currentStep > 1) {
        $(`#step-${currentStep}`).hide();
        currentStep--;
        $(`#step-${currentStep}`).show();
        updateProgressBar(currentStep);
      }
    });

    // Initially update the progress bar
    updateProgressBar(currentStep);

  });
  

  function attachCalendarListeners() {
    document.querySelectorAll('.nav-btn').forEach(button => {
      button.addEventListener('click', function () {
        const month = this.dataset.month;
        const year = this.dataset.year;

        fetch(`/appointments/get-calendar/?month=${month}&year=${year}`)
          .then(response => response.json())
          .then(data => {
            document.getElementById('calendar-body').innerHTML = data.calendar;
            document.getElementById('current-month').textContent = `${data.current_month} ${data.current_year}`;

            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');

            // Update prev
            prevBtn.dataset.month = data.prev_month;
            prevBtn.dataset.year = data.prev_year;
            toggleBtnState(prevBtn, data.is_prev_disabled);

            // Update next
            nextBtn.dataset.month = data.next_month;
            nextBtn.dataset.year = data.next_year;
            toggleBtnState(nextBtn, data.is_next_disabled);

            attachCalendarListeners(); // Reattach for new calendar
          });
      });
    });
  }

  function toggleBtnState(button, disabled) {
    if (disabled) {
      button.disabled = true;
      button.classList.add('disabled');
      button.style.pointerEvents = 'none';
      button.style.opacity = '0.5';
      button.style.cursor = 'not-allowed';
    } else {
      button.disabled = false;
      button.classList.remove('disabled');
      button.style.pointerEvents = 'auto';
      button.style.opacity = '1';
      button.style.cursor = 'pointer';
    }
  }

  document.addEventListener('DOMContentLoaded', attachCalendarListeners);


// Desktop Version
function setupDesktopCalendar() {
  const timeColumn = document.getElementById('timeColumn');
  const calendarColumn = document.getElementById('calendarColumnDesktop');
  
  document.getElementById('calendar-body-desktop').addEventListener('click', function(e) {
    const dayElement = e.target.closest('.calendar-day');
    if (dayElement) handleDateSelection(dayElement, 'desktop');
  });
  
  // Navigation buttons
  document.getElementById('prev-btn-desktop').addEventListener('click', () => updateCalendarDesktop(-1));
  document.getElementById('next-btn-desktop').addEventListener('click', () => updateCalendarDesktop(1));
}

// Mobile Version
function setupMobileCalendar() {
  const backButton = document.getElementById('backToCalendar');
  
  document.getElementById('calendar-body-mobile').addEventListener('click', function(e) {
    const dayElement = e.target.closest('.calendar-day');
    if (dayElement) handleDateSelection(dayElement, 'mobile');
  });
  
  backButton.addEventListener('click', function() {
    document.getElementById('timeViewMobile').style.display = 'none';
    document.getElementById('calendarViewMobile').style.display = 'block';
  });
  
  // Ensure calendar adjusts dynamically for mobile view
  window.addEventListener('resize', function() {
    const calendarBody = document.getElementById('calendar-body-mobile');
    if (window.innerWidth <= 768) {
      calendarBody.style.overflowX = 'auto'; // Enable horizontal scrolling
    } else {
      calendarBody.style.overflowX = 'hidden'; // Disable scrolling for larger screens
    }
  });
}

function handleDateSelection(dayElement, version) {
  const dateStr = dayElement.getAttribute('data-date');
  
  // Format the selected date for display
  const displayDate = new Date(dateStr).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  // Remove selected class from all days
  document.querySelectorAll('.calendar-day').forEach(el => {
    el.classList.remove('selected');
  });

  // Add selected class to clicked day
  dayElement.classList.add('selected');

  // Show loading state
  const timeSlotsContainer = document.getElementById(`timeSlots${version === 'mobile' ? 'Mobile' : 'Desktop'}`);
  timeSlotsContainer.innerHTML = '<div class="text-center py-3">Loading available times...</div>';

  if (version === 'desktop') {
    // Slide calendar left and show time column
    document.querySelector('.time-column').classList.add('active');
    document.querySelector('.calendar-column').classList.add('slide-left');
  } else {
    // Mobile - hide calendar, show times
    document.getElementById('calendarViewMobile').style.display = 'none';
    document.getElementById('timeViewMobile').style.display = 'block';
  }

  // Update selected date display
  document.getElementById(`selectedDate${version === 'mobile' ? 'Mobile' : 'Desktop'}`).innerHTML = `
    <i class="bi bi-calendar"></i>
    <span>${displayDate}</span>
  `;

  // Fetch available times via AJAX
  fetch(`/appointments/get-available-times/?date=${dateStr}`)
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        timeSlotsContainer.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        return;
      }

      // Populate time slots
      timeSlotsContainer.innerHTML = '';
      data.times.forEach(time => {
        const timeSlot = document.createElement('button');
        timeSlot.className = 'btn btn-outline-primary time-slot-btn m-1';
        timeSlot.textContent = time;
        timeSlot.dataset.time = time;
        timeSlot.dataset.date = dateStr;
        timeSlot.addEventListener('click', function () {
          selectTimeSlot(this);
        });
        timeSlotsContainer.appendChild(timeSlot);
      });
    })
    .catch(error => {
      timeSlotsContainer.innerHTML = '<div class="alert alert-danger">Failed to load available times</div>';
      console.error('Error:', error);
    });
}

// Ensure the calendar days have the correct data-date attribute
function attachDateListeners() {
  document.querySelectorAll('.calendar-day.available').forEach(dayElement => {
    dayElement.addEventListener('click', function () {
      handleDateSelection(this, 'desktop');
    });
  });

  document.querySelectorAll('.calendar-day.available').forEach(dayElement => {
    const dateStr = dayElement.getAttribute('data-date');
    if (!dateStr) {
      console.error('Missing data-date attribute on calendar day element.');
    }
  });
}

// Initialize both desktop and mobile calendars
document.addEventListener('DOMContentLoaded', function () {
  setupDesktopCalendar();
  setupMobileCalendar();
  attachDateListeners();
});

// Initialize both versions
document.addEventListener('DOMContentLoaded', function() {
  setupDesktopCalendar();
  setupMobileCalendar();
});


// Show custom reason field when "Other" is selected
document.getElementById('appointment_reason').addEventListener('change', function() {
  const customReasonContainer = document.getElementById('custom_reason_container');
  customReasonContainer.style.display = this.value === 'Other' ? 'block' : 'none';
  if (this.value !== 'Other') {
    document.getElementById('custom_reason').value = '';
  }
});

// Show appropriate contact method fields
document.querySelectorAll('.btn-check').forEach(radio => {
  radio.addEventListener('change', function() {
    document.getElementById('phone_number_container').style.display = 'none';
    document.getElementById('whatsapp_contact_container').style.display = 'none';
    
    if (this.value === 'phone') {
      document.getElementById('phone_number_container').style.display = 'block';
    } else if (this.value === 'whatsapp') {
      document.getElementById('whatsapp_contact_container').style.display = 'block';
    }
  });
});


// Initialize calendar with available dates
function initCalendar() {
    fetch('/get-available-dates/')
        .then(response => response.json())
        .then(data => {
            // Mark available dates in your calendar UI
            data.dates.forEach(dateStr => {
                const date = new Date(dateStr);
                // Your code to highlight available dates
            });
        });
}

// Handle date selection
function handleDateClick(dateStr) {
    fetch(`/get-available-times/?date=${dateStr}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }
            
            const timeSlotsContainer = document.getElementById('timeSlots');
            timeSlotsContainer.innerHTML = '';
            
            if (data.times.length === 0) {
                timeSlotsContainer.innerHTML = `
                    <div class="alert alert-info">
                        No available times for this date
                    </div>
                `;
                return;
            }
            
            data.times.forEach(time => {
                const slot = document.createElement('div');
                slot.className = 'time-slot';
                slot.textContent = time;
                slot.dataset.time = time;
                slot.addEventListener('click', () => selectTimeSlot(dateStr, time));
                timeSlotsContainer.appendChild(slot);
            });
            
            document.getElementById('selectedDate').textContent = data.display_date;
        });
}

function fetchAvailableDates() {
  fetch('/appointments/get-available-dates/')
    .then(response => response.json())
    .then(data => {
      const availableDates = data.dates;
      document.querySelectorAll('.calendar-day').forEach(dayElement => {
        const date = dayElement.getAttribute('data-date');
        if (availableDates.includes(date)) {
          dayElement.classList.add('available');
          dayElement.classList.remove('unavailable');
        } else {
          dayElement.classList.add('unavailable');
          dayElement.classList.remove('available');
        }
      });
    })
    .catch(error => console.error('Error fetching available dates:', error));
}

document.addEventListener('DOMContentLoaded', function () {
  fetchAvailableDates();
  setupDesktopCalendar();
  setupMobileCalendar();
});

function updateCalendar(month, year) {
  fetch(`/appointments/book-appointment/?month=${month}&year=${year}`)
    .then(response => response.text())
    .then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const newCalendar = doc.querySelector('#calendar-body-desktop').innerHTML;
      document.querySelector('#calendar-body-desktop').innerHTML = newCalendar;

      // Reattach event listeners for date selection
      attachDateListeners();
    })
    .catch(error => console.error('Error updating calendar:', error));
}

function attachDateListeners() {
  document.querySelectorAll('.calendar-day.available').forEach(dayElement => {
    dayElement.addEventListener('click', function () {
      const dateStr = this.getAttribute('data-date');
      const timeSlotsContainer = document.getElementById('timeSlotsDesktop');

      // Highlight the selected date
      document.querySelectorAll('.calendar-day').forEach(el => el.classList.remove('selected'));
      this.classList.add('selected');

      // Show loading state
      timeSlotsContainer.innerHTML = '<div class="text-center py-3">Loading available times...</div>';

      // Fetch available times for the selected date
      fetch(`/appointments/get-available-times/?date=${dateStr}`)
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            timeSlotsContainer.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            return;
          }

          // Populate time slots
          timeSlotsContainer.innerHTML = '';
          data.times.forEach(time => {
            const timeSlot = document.createElement('button');
            timeSlot.className = 'btn btn-outline-primary time-slot-btn m-1';
            timeSlot.textContent = time;
            timeSlot.dataset.time = time;
            timeSlot.dataset.date = dateStr;
            timeSlot.addEventListener('click', function () {
              selectTime(dateStr, time);
            });
            timeSlotsContainer.appendChild(timeSlot);
          });
        })
        .catch(error => {
          timeSlotsContainer.innerHTML = '<div class="alert alert-danger">Failed to load available times</div>';
          console.error('Error:', error);
        });
    });
  });
}

// Reattach date listeners after calendar updates
document.addEventListener('DOMContentLoaded', function () {
  attachDateListeners();
});

document.addEventListener('DOMContentLoaded', function () {
  attachDateListeners();

  document.getElementById('prev-btn-desktop').addEventListener('click', function () {
    const currentMonth = parseInt(this.dataset.month);
    const currentYear = parseInt(this.dataset.year);
    const newMonth = currentMonth === 1 ? 12 : currentMonth - 1;
    const newYear = currentMonth === 1 ? currentYear - 1 : currentYear;
    updateCalendar(newMonth, newYear);
  });

  document.getElementById('next-btn-desktop').addEventListener('click', function () {
    const currentMonth = parseInt(this.dataset.month);
    const currentYear = parseInt(this.dataset.year);
    const newMonth = currentMonth === 12 ? 1 : currentMonth + 1;
    const newYear = currentMonth === 12 ? currentYear + 1 : currentYear;
    updateCalendar(newMonth, newYear);
  });
});











document.addEventListener('DOMContentLoaded', function() {
    // Desktop and mobile elements
    const desktopTimeSlots = document.getElementById('timeSlotsDesktop');
    const mobileTimeSlots = document.getElementById('timeSlotsMobile');
    const selectedDateDesktop = document.getElementById('selectedDateDesktop');
    const selectedDateMobile = document.getElementById('selectedDateMobile');
    const timeViewMobile = document.getElementById('timeViewMobile');
    const calendarViewMobile = document.getElementById('calendarViewMobile');
    const backToCalendar = document.getElementById('backToCalendar');

    // Handle date selection (both desktop and mobile)
    document.querySelectorAll('.calendar-day:not(.disabled)').forEach(day => {
        day.addEventListener('click', function() {
            const selectedDate = this.getAttribute('data-date');
            const formattedDate = formatDateForDisplay(selectedDate);
            
            // Update selected date display
            selectedDateDesktop.innerHTML = `<i class="bi bi-calendar"></i><span>${formattedDate}</span>`;
            selectedDateMobile.innerHTML = `<i class="bi bi-calendar"></i><span>${formattedDate}</span>`;
            
            // Show time slots section on mobile
            calendarViewMobile.style.display = 'none';
            timeViewMobile.style.display = 'block';
            
            // Fetch available time slots
            fetchAvailableTimeSlots(selectedDate);
        });
    });

    // Back button for mobile view
    backToCalendar.addEventListener('click', function() {
        timeViewMobile.style.display = 'none';
        calendarViewMobile.style.display = 'block';
    });

    // Format date for display (e.g., "Monday, January 1, 2023")
    function formatDateForDisplay(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    }

    // Fetch available time slots from Django backend
    function fetchAvailableTimeSlots(date) {
        fetch(`/api/available-time-slots/?date=${date}`)
            .then(response => response.json())
            .then(slots => {
                renderTimeSlots(slots);
            })
            .catch(error => {
                console.error('Error fetching time slots:', error);
                showErrorState();
            });
    }

    // Render time slots in both desktop and mobile views
    function renderTimeSlots(slots) {
        if (slots.length === 0) {
            showEmptyState();
            return;
        }

        const slotsHTML = slots.map(slot => {
            const isBooked = slot.is_booked;
            return `
                <div class="time-slot ${isBooked ? 'booked' : 'available'}" 
                     data-slot-id="${slot.id}"
                     ${isBooked ? '' : 'onclick="selectTimeSlot(this)"'}>
                    ${slot.start_time} - ${slot.end_time}
                    ${isBooked ? '<span class="badge bg-secondary">Booked</span>' : ''}
                </div>
            `;
        }).join('');

        desktopTimeSlots.innerHTML = slotsHTML;
        mobileTimeSlots.innerHTML = slotsHTML;
    }

    // Show empty state when no slots available
    function showEmptyState() {
        const emptyHTML = `
            <div class="empty-state">
                <i class="bi bi-calendar-x"></i>
                <p>No available time slots for this date</p>
            </div>
        `;
        desktopTimeSlots.innerHTML = emptyHTML;
        mobileTimeSlots.innerHTML = emptyHTML;
    }

    // Show error state when fetch fails
    function showErrorState() {
        const errorHTML = `
            <div class="empty-state text-danger">
                <i class="bi bi-exclamation-triangle"></i>
                <p>Error loading time slots. Please try again.</p>
            </div>
        `;
        desktopTimeSlots.innerHTML = errorHTML;
        mobileTimeSlots.innerHTML = errorHTML;
    }
});

// Handle time slot selection
function selectTimeSlot(element) {
    // Remove previous selection
    document.querySelectorAll('.time-slot.selected').forEach(slot => {
        slot.classList.remove('selected');
    });
    
    // Add selection to clicked slot
    element.classList.add('selected');
    
    // Enable next button if you have a multi-step form
    const nextButton = document.querySelector('.next-step-btn');
    if (nextButton) {
        nextButton.disabled = false;
    }
    
    // Store selected slot in hidden input if needed
    const slotId = element.getAttribute('data-slot-id');
    document.getElementById('selected-time-slot').value = slotId;
}


function renderTimeSlots(slots) {
  const container = document.getElementById('timeSlotsDesktop') || 
                   document.getElementById('timeSlotsMobile');
  
  if (!slots || slots.length === 0) {
      container.innerHTML = `
          <div class="empty-state">
              <i class="bi bi-calendar-x"></i>
              <p>No available time slots for this date</p>
          </div>
      `;
      return;
  }

  container.innerHTML = slots.map(slot => `
      <div class="time-slot ${slot.is_booked ? 'booked' : 'available'}" 
           data-slot-id="${slot.id}"
           ${slot.is_booked ? '' : 'onclick="selectTimeSlot(this)"'}
           style="background-color: ${slot.is_booked ? '#ffebee' : '#e3f2fd'}; 
                  color: ${slot.is_booked ? '#c62828' : '#0d47a1'}; 
                  border: 2px solid ${slot.is_booked ? '#ffcdd2' : '#2196f3'};">
          ${slot.start_time} - ${slot.end_time}
      </div>
  `).join('');
}


function updateSelectedDate(dateString) {
  const date = new Date(dateString);
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  document.getElementById('selectedDateDesktop').querySelector('span').textContent = 
      date.toLocaleDateString('en-US', options);
}

function showLoadingState() {
  const container = document.getElementById('timeSlotsDesktop');
  container.innerHTML = `
      <div class="empty-state">
          <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
          </div>
          <p>Loading available times...</p>
      </div>
  `;
}



let currentlySelectedSlot = null;

function selectTimeSlot(element) {
  // Ignore if booked
  if (element.classList.contains('booked')) return;

  // Remove previous selection
  if (currentlySelectedSlot) {
    currentlySelectedSlot.classList.remove('selected');
  }

  // Set new selection
  element.classList.add('selected');
  currentlySelectedSlot = element;

  // Store selected slot ID (for form submission)
  document.getElementById('selected-time-slot').value = element.dataset.slotId;
  
  // Optional: Scroll to keep selection visible
  element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Initialize from your slot rendering function
function renderTimeSlots(slots) {
  const container = document.getElementById('timeSlotsDesktop');
  container.innerHTML = slots.map(slot => `
    <div class="time-slot ${slot.is_booked ? 'booked' : 'available'}" 
         data-slot-id="${slot.id}"
         onclick="selectTimeSlot(this)"
         style="background-color: ${slot.is_booked ? '#ffebee' : '#e3f2fd'}; 
                color: ${slot.is_booked ? '#c62828' : '#0d47a1'}; 
                border: 2px solid ${slot.is_booked ? '#ffcdd2' : '#2196f3'};">
      ${slot.start_time} - ${slot.end_time}
    </div>
  `).join('');
}

function goToStep2() {
  // Get values from step 1 fields
  const name = document.getElementById('name').value.trim() || 'Empty';
  const email = document.getElementById('email').value.trim() || 'Empty';
  const reasonSelect = document.getElementById('appointment_reason');
  const reason = reasonSelect.options[reasonSelect.selectedIndex]?.text.trim() || 'Empty';
  const contactMethod = document.querySelector('input[name="contact_method"]:checked');

  // Update summary display
  document.getElementById('summary-name').textContent = name;
  document.getElementById('summary-email').textContent = email;
  document.getElementById('summary-reason').textContent = reason;

  // Update contact method
  if (contactMethod) {
    const contactLabel = document.querySelector(`label[for="${contactMethod.id}"]`);
    const contactText = contactLabel.textContent.trim() || 'Empty';
    const contactIcon = contactLabel.querySelector('i').cloneNode(true);

    document.getElementById('summary-contact').textContent = contactText;
    document.getElementById('summary-contact-icon').innerHTML = '';
    document.getElementById('summary-contact-icon').appendChild(contactIcon);
  } else {
    document.getElementById('summary-contact').textContent = 'Empty';
    document.getElementById('summary-contact-icon').innerHTML = '';
  }

  // Show Step 2
  document.getElementById('step-1').style.display = 'none';
  document.getElementById('step-2').style.display = 'block';

  // Update progress bar
  updateProgressBar(2);
}



















