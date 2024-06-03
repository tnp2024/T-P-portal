function goBack() {
    window.history.back();
}

function deleteNotice() {

    fetch("{% url 'delete-activity' activity.id %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => {
        if (response.ok) {
            window.location.href = "{% url 'activities' %}"; p
        }
    }).catch(error => console.error('Error:', error));
}