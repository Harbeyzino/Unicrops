document.addEventListener('DOMContentLoaded', function() {
    // 1. Highlight current date in date pickers
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(input => {
        if (input.value === today) {
            input.style.border = '2px solid #4CAF50';
        }
    });

    // 2. Add color coding to time slots
    const timeSlots = document.querySelectorAll('.field-formatted_time_range');
    timeSlots.forEach(slot => {
        const isBooked = slot.closest('tr').querySelector('.field-has_appointment img').alt === 'True';
        if (isBooked) {
            slot.style.color = '#dc3545';
            slot.style.fontWeight = 'bold';
        } else {
            slot.style.color = '#28a745';
        }
    });

    // 3. Add quick action buttons
    const actionBar = document.querySelector('.submit-row');
    if (actionBar) {
        const quickGenerateBtn = document.createElement('input');
        quickGenerateBtn.type = 'button';
        quickGenerateBtn.value = 'Generate Time Slots';
        quickGenerateBtn.className = 'default';
        quickGenerateBtn.style.marginRight = '10px';
        quickGenerateBtn.onclick = function() {
            const availabilityId = window.location.pathname.split('/')[4];
            fetch(`/admin/appointments/availability/${availabilityId}/generate_slots/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Accept': 'application/json'
                }
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                }
            });
        };
        actionBar.prepend(quickGenerateBtn);
    }
});