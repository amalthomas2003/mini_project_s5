<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='student_dashboard_style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Welcome,{{student_name}}</h1>
        <div class="buttons">
            <a href="/student_dashboard/eligible_companies" class="button">View Eligible Companies</a>
            <a href="post_question.html" class="button">Post Question</a>
            <a href="view_questions.html" class="button">View Questions</a>
            <a href="logout.html" class="button">Logout</a>
        </div>
    </div>
</body>
</html>