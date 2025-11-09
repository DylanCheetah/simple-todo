document.addEventListener("DOMContentLoaded", () => {
    // Add event listeners to task completion checkboxes
    const onTaskCompletionToggle = (evt) => {
        // Send task completion update request
        fetch(evt.target.dataset.url, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                completed: evt.target.checked
            })
        })
        .then((response) => {
            // Did the request fail?
            if(response.status != 204) {
                // Read error message
                return response.json()
                .then((payload) => {
                    // Reset checkbox to previous state and display error message
                    evt.target.checked = !evt.target.checked;
                    alert(payload.error);
                });
            }
        })
        .catch((msg) => {
            // Reset checkbox to previous state and display error message
            evt.target.checked = !evt.target.checked;
            alert(msg);
        });
    };

    document.querySelectorAll(".task-checkbox").forEach((checkbox) => {
        // Add event listener to detect checkbox toggle
        checkbox.addEventListener("change", onTaskCompletionToggle);
    });
});
