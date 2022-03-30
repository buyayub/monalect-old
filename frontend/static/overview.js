/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/api.js":
/*!********************!*\
  !*** ./src/api.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "API_URL": () => (/* binding */ API_URL),
/* harmony export */   "course": () => (/* binding */ course),
/* harmony export */   "lesson": () => (/* binding */ lesson),
/* harmony export */   "material": () => (/* binding */ material)
/* harmony export */ });
const API_URL = "http://localhost:9000"

const lesson =
{
	create: async function (data, course_id) 
	{
		const response = await fetch(`${API_URL}/api/course/${course_id}/lesson`,
		{
			method : 'POST',
			headers : {'Content-Type' : 'application/json'},
			credentials: "include",
			body: JSON.stringify(data)
		})
		if (response.ok)
			return response.json()
		throw Error("Server request failed.")
	},
	delete: async function (course_id, lesson_id)
	{
		const response = await fetch(`${API_URL}/api/course/${course_id}/lesson/${lesson_id}`, {
			method : 'DELETE',
			credentials: "include"
		})
		if (response.ok)
			return response.json()
		throw Error("Server request failed.")
	},
	section: 
	{
		create: async function (data, course_id, lesson_id)
		{
			const response = await fetch(`${API_URL}/api/${course_id}/section/${lesson_id}`, {
				method: "POST",
				headers : {"Content-Type" : "application/json"},
				credentials: "include",
				body: JSON.stringify(data)
			})
			if (response.ok)
				return response.json()
			throw Error("Server request failed.")
		},
		delete: async function (data, course_id, lesson_id, section_id)
		{
			const response = await fetch(`${API_URL}/api/${course_id}/section/${lesson_id}/${section_id}`, {
				method: "DELETE",
				credentials: "include"
			})
			if (response.ok)
				return response.json()
			throw Error("Server request failed.")
		}
	}
}

const material =
{
	textbook :
	{
		create: async function (data, course_id) 
		{
			const response = await fetch(`${API_URL}/api/${course_id}/textbook`, {
				method: "POST",
				headers : {"Content-Type" : "multipart/form-data"},
				credentials: "include",
				body: data
			})
			if (response.ok)
				return response.json()
			throw Error("Server request failed.")
		},
		delete: async function (data, course_id)
		{
			const response = await fetch(`${API_URL}/api/${course_id}/section/${lesson_id}/${section_id}`, {
				method: "DELETE",
				credentials: "include"
			})
			if (response.ok)
				return response.json()
			throw Error("Server request failed.")
		}
	}
}

const course =
{
	id : function () 
	{
		URL = window.location.pathname
		URL = URL.split("/")
		URL = URL[2]
		return URL
	}
}




/***/ }),

/***/ "./src/display.js":
/*!************************!*\
  !*** ./src/display.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "lesson": () => (/* binding */ lesson),
/* harmony export */   "textbook": () => (/* binding */ textbook)
/* harmony export */ });
const lesson =
{
	card : function (data, root, removeFunc=null, showForm = null, hide=false)
	{
		const card = document.createElement("div")
		card.setAttribute("data-id", data['id'])

		const delete_lesson = document.createElement("button")
		delete_lesson.innerText = "-"
		delete_lesson.addEventListener("click", removeFunc)
		delete_lesson.classList.add("delete_lesson", "edit")

		// Find a less stupid way for this 
		if (hide)
			delete_lesson.classList.add("hide");

		const title  = document.createElement("h1")
		title.innerText = data['title']
		title.className = "lesson_title"
		
		const material = document.createElement("div")
		material.className = "lesson_material"

		for (section of data['textbook_sections'])
			lesson.section.display(section, material);

		const add_material = document.createElement("button")
		add_material.innerText = "+"
		add_material.classList.add("edit", "lesson_add_material")
		add_material.addEventListener("click", showForm) 

		//if does NOT contain
		if (hide)
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

		const words = data['notebook_words'] == null ? -1 : data['notebook_words']
		const words_stat = document.createElement("p")	
		words_stat.innerText = words
		words_stat.className = "lesson_stat_data"

		const words_image = document.createElement("img")
		words_image.src = "/static/question.svg"
		words_image.className = "lesson_stat_image"

		const stats = document.createElement("div")
		stats.className = "lesson_stats"

		questions.append(lesson_question_image, question_stat)
		lesson_words.append(words_image, words_stat)
		stats.append(questions, lesson_words)
		card.append(delete_lesson, title, material, add_material, stats)
		root.append(card)
	},
	section: 
	{
		textbook: function (data, element)
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
	}
}

/*
 * textbook
 *	card
 *	list (adds option to the selection element)
 */

const textbook = 
{
	card: function(data, root, displaySettings)
	{
		const card = document.createElement("div")
		card.className = "card"
		card.setAttribute("data-id", data['id'])

		const image = document.createElement("img")
		image.src = (data["filename"] == null) ? "/static/textbook_red.svg" : "/static/textbook.svg"

		const text = document.createElement("div")
		text.className = "text"

		const title = document.createElement("h3")
		title.className = "title"
		title.innerText = data["title"]

		const author = document.createElement("p")
		author.className = "author"
		author.innerText = data["author"]

		const pages = document.createElement("p")
		pages.className = "pages"
		pages.innerText = `${data["pages"]}pg`

		const settings = document.createElement("img")
		settings.className = "settings" 
		settings.addEventListener("click", displaySettings)

		text.append(title, author)
		card.append(image, text, pages)
		root.append(card)
	},
	list: function(data, root)
	{
		const option = document.createElement("option")
		option.value= data['id']
		option.innerText = data['title']
		root.append(option)
	}
}




/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
/*!*************************!*\
  !*** ./src/overview.js ***!
  \*************************/
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./api.js */ "./src/api.js");
/* harmony import */ var _display_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./display.js */ "./src/display.js");




/* GLOBALS */

const COURSE = _api_js__WEBPACK_IMPORTED_MODULE_0__.course.id()
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

fetch(`${_api_js__WEBPACK_IMPORTED_MODULE_0__.API_URL}/api/website/course/${COURSE}`,  {
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
	const form_data = new FormData(undefined);
	const data = {title : (form_data.get("title") == "") ? "Untitled" : form_data.get("title")}

	_api_js__WEBPACK_IMPORTED_MODULE_0__.lesson.create(data, COURSE)
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
	
	_api_js__WEBPACK_IMPORTED_MODULE_0__.lesson.section.create(payload, COURSE, lesson_id)
	.then((data) =>
	{
		lesson_material = document.querySelector(`div[data-id=${lesson_id}] .lesson_material`)
		_display_js__WEBPACK_IMPORTED_MODULE_1__.lesson.card(data, lesson_material, deleteLesson)
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
		_display_js__WEBPACK_IMPORTED_MODULE_1__.lesson.card(element, website.lesson.cards, deleteLesson, sectionShowForm, !website.modify.classList.contains("hide"))
	}

	for (const textbook of data['textbooks'])
	{
		_display_js__WEBPACK_IMPORTED_MODULE_1__.textbook.card(textbook, website.material.cards)
		_display_js__WEBPACK_IMPORTED_MODULE_1__.textbook.list(textbook, website.material.select)
	}
}



})();

/******/ })()
;
//# sourceMappingURL=overview.js.map