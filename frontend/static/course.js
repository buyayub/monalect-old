const API_URL = "http://localhost:9000"
const COURSE_ID = getCourseId()

website = {
	material : {
		display : document.getElementById("materials"),
		form : document.getElementById("material_form"),
		success: document.querySelector("#material_form .success"),
		failure: document.querySelector("#material_form .failure"),
		select : document.getElementById("material_select"),
		empty : document.getElementById("materials_empty"),
		cards : document.getElementById("material_cards"),
		add : document.getElementById("add_material")
	},
	lesson : {
		display : document.getElementById("lessons"),
		empty : document.getElementById("lessons_empty"),
		add : document.getElementById("add_lesson"),
		form : document.getElementById("material_section"),
		cards : document.getElementById("lesson_cards"),
	},
	modify : document.getElementById("modify"),
	done : document.getElementById("done"),
	delete : document.getElementById("delete"),
	finish : document.getElementById("finish"),
	course : {
		title : document.getElementById("course_title"),
		created : document.getElementById("course_timestamp"),
		description: document.querySelector("#course_description div")
	},
	popup : document.getElementsByClassName("pop_up"),
	edit : document.getElementsByClassName("edit")
}


function lessonDisplay(data, root)
{
	card = document.createElement("div")
	card.setAttribute("data-id", data['id'])

	const delete_lesson = document.createElement("button")
	delete_lesson.innerText = "-"
	delete_lesson.addEventListener("click", deleteLesson)
	delete_lesson.classList.add("delete_lesson", "edit")

	// Find a less stupid way for this 
	if (!website.modify.classList.contains("hide"))
		delete_lesson.classList.add("hide");

	const title  = document.createElement("h2")
	title.innerText = data['title']
	title.className = "lesson_title"
	
	const material = document.createElement("div")
	material.className = "lesson_material"

	for (section of data['textbook_sections'])
		lesson.section.display(section, material);

	add_material = document.createElement("button")
	add_material.innerText = "+"
	add_material.classList.add("edit", "lesson_add_material")
	add_material.addEventListener("click", lesson.section.showForm) 

	//if does NOT contain
	if (!website.modify.classList.contains("hide")) 
		add_material.classList.add("hide");

	const questions = document.createElement("div")	
	questions.className = "lesson_questions"
	
	const question_stat = document.createElement("p")
	question_stat.innerText = data['question_count']	
	question_stat.className = "lesson_stat_data"

	const lesson_question_image = document.createElement("img")
	lesson_question_image.src = "/static/question.svg"
	lesson_question_image.className = "lesson_stat_image"

	const lesson_words = document.createElement("div")
	lesson_words.className = "lesson_words"

	words = data['notebook_words'] == null ? 0 : data['notebook_words']
	words_stat = document.createElement("p")	
	words_stat.innerText = words
	words_stat.className = "lesson_stat_data"

	words_image= document.createElement("img")
	words_image.src = "/static/question.svg"
	words_image.className = "lesson_stat_image"

	stats = document.createElement("div")
	stats.className = "lesson_stats"

	questions.append(lesson_question_image, question_stat)
	lesson_words.append(words_image, words_stat)
	stats.append(questions, lesson_words)
	card.append(delete_lesson, title, material, add_material, stats)
	root.append(card)
}

function sectionShowForm()
{
	website.lesson.form.setAttribute("data-id",  this.parentElement.dataset.id)
	website.lesson.form.classList.remove("hide")
	website.material.form.classList.add("hide")
}

toggleEdit() //Set to hide
function toggleEdit() {
	for (element of website.edit)
		element.classList.toggle("hide");
}

togglePopUp() //Set to hide
function togglePopUp() {
	for (element of website.popup)
		element.classList.toggle("hide");
}

function getCourseId() {
	URL = window.location.pathname
	URL = URL.split("/")
	URL = URL[2]
	return URL
}

function initDisplay(data)
{
	website.course.title.innerText = (data['course']['title'] == null) ? "Untitled" : data['course']['title']
	website.course.innerText =  data['course']['created']
	website.course.description.innerText = data['course']['description']

	for (element of data['lessons'])
	{
		lesson.display(element, website.lesson.cards)
	}

	for (textbook of data['textbooks'])
	{
		displayBook(textbook, website.material.cards)
		listTextbook(textbook, website.material.select)
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

website.modify.addEventListener("click", () =>
{
	website.modify.classList.add("hide")
	toggleEdit()
})

website.done.addEventListener("click", () =>
{
	document.querySelector("#modify").classList.remove("hide")
	toggleEdit()
})

function deleteLesson()
{
	lesson = this.parentElement
	lesson_id = lesson.dataset.id

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

function deleteTextbook()
{
	textbook = this.parentElement.parentElement
	textbook_id = textbook.dataset.id 

	fetch(`${API_URL}/api/course/${COURSE_ID}/textbook`, {
		method : 'DELETE',
		credentials: 'include'
	})
	.then((response) =>
	{
		if (response.ok)
		{
			textbook.remove()
		}
	})
}


//is DOM manipulation supposed to be this verbose

function displaySettings()
{
	material_settings = document.createElement("div")
	material_settings.className("settings")

	delete_material = document.createElement("p")
	delete_material.className("settings_delete")
	delete_material.addEventListener("click",  deleteTextbook)

	material_settings.attach(delete_material)
}


add_lesson.addEventListener("submit", (e) =>
{
	e.preventDefault();
	var form_data = new FormData(add_lesson)
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
			textbook_sections: [],
			notebook_words : 0,
			question_count : 0
		}, website.lesson.cards)
	})
})

website.modify.addEventListener("click", () =>
{
	website.material.form.classList.remove("hide")
	website.material.success.classList.add("hide")
	website.material.success.classList.add("hide")
	website.lesson.material_section.add("hide")
})

//add_goal.addEventListener("click", () => {})

function listTextbook(data, root)
{
	textbook_option = document.createElement("option")
	textbook_option.value= data['id']
	textbook_option.innerText = data['title']
	root.append(textbook_option)
}

function displayBook(data, root)
{
	material_card = document.createElement("div")
	material_card.className = "material_card"
	material_card.setAttribute("data-id", data['id'])

	material_image = document.createElement("img")
	material_image.src = (data["filename"] == null) ? "/static/textbook_red.svg" : "/static/textbook.svg"

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

	material_settings = document.createElement("img")
	material_settings.className = "material_settings" 
	material_settings.addEventListener("click", displaySettings)

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
	request.open("POST", `${API_URL}/api/${COURSE_ID}/textbook`)
	request.responseType = 'json'
	request.withCredentials = true
	request.onload = () => 
	{
		if (request.status == 201)
		{
			material_form.reset()
			website.material.failure.add("hide")
			website.material.success.remove("hide")
			displayBook(request.response, website.material.cards)
			listTextbook(request.response)
		}
		else
		{
			website.material.failure.remove("hide")
			website.material.success.add("hide")
		}
	}
	request.send(form_data)
})

website.lesson.form.addEventListener("submit", (e) =>
{
	e.preventDefault();
	lesson_id = material_section.dataset.id

	var form_data = new FormData(material_section)
	payload = {
		textbook_id : form_data.get('textbook'),
		lesson_id : lesson_id,
		start_page : form_data.get('start_page'),
		end_page : form_data.get('end_page')
	}

	fetch(`${API_URL}/api/${COURSE_ID}/section/${lesson_id}`,{
		method: "POST",
		headers : {"Content-Type" : "application/json"},
		credentials: "include",
		body: JSON.stringify(payload)
	})
	.then((response) =>
	{
		if (response.ok)
		{
			return response.json()
		}
	})
	.then((data) =>
	{
		lesson_material = document.querySelector(`div[data-id=${lesson_id}] .lesson_material`)
		displaySection(data, lesson_material)
	})
})


function displaySection(data, root)
{
	section_img = document.createElement("img")	
	section_img.src = "/static/textbook.svg"
	section_img.className = "section_img"

	section_text = document.createElement("div")
	section_text.className = "section_text"

	section_title = document.createElement("h3")
	section_title.className = "section_title"
	section_title.innerText = data['title']

	section_pages = document.createElement("p")
	section_pages.className = "section_pages"
	section_pages.innerText = `pg. ${data['start_page']}-${data['end_page']}`

	section_text.append(section_title, section_pages)
	root.append(section_img, section_text)
}

