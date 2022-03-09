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

export {lesson, textbook};
