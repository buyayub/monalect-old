import {lesson as api_lesson, 
	material as api_textbook, 
	course as api_course, 
	API_URL} 
from "./api.js"

import {lesson as display_lesson, 
	textbook as display_textbook} 
from "./display.js"

/* GLOBALS */

const COURSE = api_course.id()
const website = {
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

/* Initialize Page */

toggleEdit() //Set to hide
togglePopUp() //Set to hide

fetch(`${API_URL}/api/website/course/${COURSE}`,  {
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
	const lessons = data['lessons']
	const goals = data['goals']
	const textbooks = data['textbooks']
	const course = data['course']
	if ((lessons.length === 0) && (goals.length === 0) && (textbooks.length === 0))
	{
		modify_button.click();
	}
	(lessons.length === 0) ? () => {lessons_empty.style.display = ""} : lessons_empty.style.display = "none"
	initDisplay(data)
})

/* CRUD: Events */

website.lesson.add.addEventListener("submit", (e) =>
{
	e.preventDefault()
	const form_data = new FormData(this);
	const data = {title : (form_data.get("title") == "") ? "Untitled" : form_data.get("title")}

	api_lesson.create(data, COURSE)
	.then((response) => {
		console.log(response)	
	})
	.catch((error) => {
		console.log(error)
	})
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
	
	api_lesson.section.create(payload, COURSE, lesson_id)
	.then((data) =>
	{
		lesson_material = document.querySelector(`div[data-id=${lesson_id}] .lesson_material`)
		display_lesson.card(data, lesson_material, deleteLesson)
	})
	.catch((e) => {console.log(error)})
})

/* CRUD: Functions */

function deleteLesson()
{
	const lesson_element = this.parentElement
	const lesson_id = lesson.dataset.id
	lesson.delete(COURSE, lesson_id)
	.then(() => {lesson_element.remove()})
	.catch((e) => {console.log(error)})
}

/* LOGIC: Events */

website.done.addEventListener("click", () =>
{
	document.querySelector("#modify").classList.remove("hide")
	toggleEdit()
})

website.modify.addEventListener("click", () =>
{
	website.material.form.classList.remove("hide")
	website.material.success.classList.add("hide")
	website.material.success.classList.add("hide")
	website.lesson.material_section.add("hide")
})

website.modify.addEventListener("click", () =>
{
	website.modify.classList.add("hide")
	toggleEdit()
})

website.done.addEventListener("click", () =>
{
	website.modify.classList.remove("hide")
	toggleEdit()
})

/* LOGIC: Functions */

function toggleEdit() {
	for (const element of website.edit)
		element.classList.toggle("hide");
}

function togglePopUp() {
	for (const element of website.popup)
		element.classList.toggle("hide");
}

function sectionShowForm()
{
	website.lesson.form.setAttribute("data-id",  this.parentElement.dataset.id)
	website.lesson.form.classList.remove("hide")
	website.material.form.classList.add("hide")
}

function initDisplay(data)
{
	website.course.title.innerText = (data['course']['title'] == null) ? "Untitled" : data['course']['title']
	website.course.innerText =  data['course']['created']
	website.course.description.innerText = data['course']['description']

	for (const element of data['lessons'])
	{
		display_lesson.card(element, website.lesson.cards, deleteLesson, sectionShowForm, !website.modify.classList.contains("hide"))
	}

	for (const textbook of data['textbooks'])
	{
		display_textbook.card(textbook, website.material.cards)
		display_textbook.list(textbook, website.material.select)
	}
}


