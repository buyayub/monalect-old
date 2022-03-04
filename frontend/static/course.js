API_URL = "http://localhost:9000"
EDIT = false

save_button = document.querySelector("#save")
save_button.style.display = "none"

finish_button = document.querySelector("#finish")
finish_button.style.display = "none"

delete_button = document.querySelector("#delete")
delete_button.style.display = "none"

cancel_button = document.querySelector("#cancel")
cancel_button.style.display = "none"

modify_button = document.querySelector("#modify")

lessons_empty = document.querySelector("#lessons_empty")
lessons_empty.style.display = "none"

goals_empty = document.querySelector("#goals_empty")
goals_empty.style.display = "none"

materials_empty = document.querySelector("#materials_empty")
materials_empty.style.display = "none"

add_lesson = document.querySelector("#add_lesson")
add_lesson.style.display = "none"

add_goal = document.querySelector("#add_goal")
add_goal.style.display = "none"

add_material = document.querySelector("#add_material")
add_material.style.display = "none"

document.querySelector("#material_form").style.display = "none"

function getCourseId() {
	URL = window.location.pathname
	URL = URL.split("/")
	URL = URL[2]
	return URL
}

COURSE_ID = getCourseId()

function initDisplay(data)
{
	title = document.querySelector("#course-title")
	created = document.querySelector("#course-timestamp")
	description = document.querySelector("#course-description div")
	title.data = (data['course']['title'] == null) ? "Untitled" : data['course']['title']
	created.data =  data['course']['created']
	description.data = data['course']['description']

	for (lesson of data['lessons'])
	{
		displayLesson(lesson)
	}
}

fetch(`${API_URL}/api/website/course/${COURSE_ID}`,  {
	method: 'GET',
	credentials: "include"})
.then((response) =>
{
	if (response.ok) {
		return response.json()		
	}
})
.then((data) =>
{
	lessons = data['lessons']
	goals = data['goals']
	textbooks = data['textbooks']
	course = data['course']
	if ((lessons.length === 0) && (goals.length === 0) && (textbooks.length === 0))
	{modify_button.click();}
	(lessons.length === 0) ? () => {lessons_empty.style.display = ""} : lessons_empty.style.display = "none"
	initDisplay(data)
})


modify_button.addEventListener("click", () =>
{
	save_button.style.display = "inline"
	cancel_button.style.display = "inline"
	finish_button.style.display = "inline"
	delete_button.style.display = "inline"
	modify_button.style.display = "none"

	add_lesson.style.display="flex"
	add_goal.style.display="block"
	add_material.style.display="block"

	edit_elements = document.querySelectorAll(".edit")
	for (element of edit_elements)
	{
		element.style.display = ""
	}
})

cancel_button.addEventListener("click", () =>
{
	save_button.style.display = "none"
	cancel_button.style.display = "none"
	finish_button.style.display = "none"
	delete_button.style.display = "none"
	modify_button.style.display = "inline"

	add_lesson.style.display = "none"
	add_goal.style.display="none"
	add_material.style.display="none"

	edit_elements = document.querySelectorAll(".edit")
	for (element of edit_elements)
	{
		element.style.display = "none"
	}
})

function deleteLesson()
{
	lesson = this.parentElement
	lesson_id = lesson.dataset.id
	request_body = {method: "delete"}
	fetch(`${API_URL}/api/course/${COURSE_ID}/lesson/${lesson_id}`, {
		method : 'DELETE',
		credentials: "include",
	})
	.then((response) =>
	{
		if (response.ok)
		{
			lesson.remove()
		}
	})
}

function displayLesson(lesson)
{
	lesson_cards = document.querySelector("#lesson_cards")
	root = document.createElement("div")
	root.setAttribute("data-id", lesson['id'])

	const delete_lesson = document.createElement("button")
	delete_lesson.innerText = "-"
	delete_lesson.addEventListener("click", deleteLesson)
	delete_lesson.classList.add("delete_lesson")
	delete_lesson.classList.add("edit")

	if (document.querySelector("#modify").style.display !== "none")
		delete_lesson.style.display = "none";

	const lesson_title  = document.createElement("h2")
	lesson_title.innerText = lesson['title']
	lesson_title.className = "lesson_title"
	
	const lesson_material = document.createElement("div")
	lesson_material.className = "lesson_material"

	const lesson_questions = document.createElement("div")	
	lesson_questions.className = "lesson_questions"
	
	const lesson_question_stat = document.createElement("p")
	lesson_question_stat.innerText = lesson['question_count']	
	lesson_question_stat.className = "lesson_stat_data"

	const lesson_question_image = document.createElement("img")
	lesson_question_image.src = "/static/question.svg"
	lesson_question_image.className = "lesson_stat_image"

	const lesson_words = document.createElement("div")
	lesson_words.className = "lesson_words"

	words = lesson['notebook_words'] == null ? 0 : lesson['notebook_words']
	lesson_words_stat = document.createElement("p")	
	lesson_words_stat.innerText = words
	lesson_words_stat.className = "lesson_stat_data"

	lesson_words_image= document.createElement("img")
	lesson_words_image.src = "/static/question.svg"
	lesson_words_image.className = "lesson_stat_image"

	lesson_stats = document.createElement("div")
	lesson_stats.className = "lesson_stats"

	lesson_questions.append(lesson_question_image, lesson_question_stat)
	lesson_words.append(lesson_words_image, lesson_words_stat)
	lesson_stats.append(lesson_questions, lesson_words)
	root.append(delete_lesson, lesson_title, lesson_material, lesson_stats)
	lesson_cards.append(root)
}


add_lesson.addEventListener("submit", (e) =>
{
	e.preventDefault();
	var form_data = new FormData(add_lesson)
	console.log(form_data.get('title'))
	if (form_data.get('title') === "")
		form_data.set('title', "Untitled")
	lesson_data = {'title': form_data.get('title')}
	fetch(`${API_URL}/api/course/${COURSE_ID}/lesson`, {
		method : 'POST',
		headers : {'Content-Type' : 'application/json'},
		credentials: "include",
		body: JSON.stringify(lesson_data)
	})
	.then((response) => {
		if (response.ok)
			return response.json()
	})
	.then((data) => {
		displayLesson({
			id : data['id'],
			title : data['title'], 
			notebook_words : 0,
			question_count : 0
		})
	})
})


add_material.addEventListener("click", () =>
{
	document.querySelector("#material_form").style.display = ""
	document.querySelector("#material_form .success").style.display="none"
	document.querySelector("#material_form .failure").style.display="none"
})

function displayBook(data, root)
{
	material_card = document.createElement("div")
	material_card.className = "material_card"

	material_image = document.createElement("img")
	material_image.src = (data["isbn"] == null) ? "/static/textbook_red.svg" : "/static/textbook.svg"

	material_text = document.createElement("div")
	material_text.className = "material_text"

	material_title = document.createElement("h3")
	material_title.className = "material_title"
	material_title.innerText = data["title"]

	material_author = document.createElement("p")
	material_author.className = "material_author"
	material_author.innerText = data["author"]

	material_pages = document.createElement("p")
	material_pages.className = "material_pages"
	material_pages.innerText = `${data["pages"]}pg`

	material_text.append(material_title, material_author)
	material_card.append(material_image, material_text, material_pages)
	root.append(material_card)
}

material_form = document.querySelector("#material_form")
material_form.addEventListener("submit", (e) =>
{
	e.preventDefault();
	var form_data = new FormData(material_form)
	request = new XMLHttpRequest();
	request.open("POST", `${API_URL}/api/textbook`)
	request.responseType = 'json'
	request.onload = () => 
	{
		if (request.status == 202)
		{
			material_form.reset()
			document.querySelector("#material_form.failure").style.display="none"
			document.querySelector("#material_form.success").style.display=""
			response = request.response
			root = document.querySelector("#material_cards")
			displayBook(response, root)
		}
		else
		{
			document.querySelector("#material_form.success").style.display="none"
			document.querySelector("#material_form.failure").style.display=""
		}
	}
	request.send(form_data)
})


