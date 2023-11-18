document.addEventListener("DOMContentLoaded", function () {
    tinymce.init({
        selector: '#editor',
        plugins: 'image link lists',
        menubar: 'edit view insert format table tools',
        toolbar: 'undo redo | styleselect | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | numlist bullist outdent indent | link image | forecolor backcolor | removeformat',
        content_style: 'body { font-size: 16px; }',
    });

    const form = document.getElementById('postQuestionsForm');
    const contentInput = document.getElementById('content-input');

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        const content = tinymce.get('editor').getContent();
        contentInput.value = content;

        // Create a FormData object to send the form data
        const formData = new FormData(form);

        // Send the form data to the server
        fetch('/student_dashboard/post_questions', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server
            if (data.message === "Save Success") {
                // Show a "Save Success" popup
                alert("Save Success");

                // Automatically redirect to the company_hr_dashboard page
                window.location.href = '/student_dashboard';
            }
        })
        .catch(error => {
            // Handle any errors that occur during the fetch request
            console.error('Error:', error);
        });
    });
});
