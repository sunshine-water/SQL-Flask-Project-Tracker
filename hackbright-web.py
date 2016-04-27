from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/student-search")
def get_student_form():
	"""Show form for searching for a student."""
	return render_template('student_search.html')

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    grades = hackbright.get_grades_by_github(github)
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template("student_info.html",
    						first=first,
    						last=last,
    						github=github,
    						grades=grades)

    return html

@app.route("/new-student")
def get_new_student_form():
	"""Show form for adding a new student."""
	return render_template('new_student.html')

@app.route("/student-add", methods=['POST'])
def student_add():
	"""Add a student."""

	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	github = request.form.get('github')
	hackbright.make_new_student(first_name, last_name, github)

	return render_template('new_student_response.html',
							first=first_name,
							last=last_name,
							github=github)

@app.route("/project")
def get_project_info():
	"""Display information about particular projects."""
	
	title = request.args.get('title', 'Markov')
	project_info = hackbright.get_project_by_title(title)
	student_grades = hackbright.get_grades_by_title(title)

	return render_template('project_info.html',
							project_info=project_info,
							student_grades=student_grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
