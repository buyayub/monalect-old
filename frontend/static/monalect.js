API_URL = "http://localhost:9000"

function createCourseCards(courses, root){
	for (course of courses) {
		textbook_pages = (course['textbook_pages'] == null) ? 0 : course['textbook_pages']
		notebook_words = (course['notebook_words'] == null) ? 0 : course['notebook_words']
		question_count = course['question_count']
		description = (course['description'] == null) ? "" : course['description']
		title = (course['title'] == null) ? "Untitled" : course['title']
		cardHTML = 
		`
		<article>
			<div>
				<img src="/static/notebook.svg">
				<div>
					<h2>${title}</h2>
					<div>
						<div>
							<img src="/static/textbook.svg" class="card_stats">
							<p>${textbook_pages}</p>
						</div>
						<div>
							<img src="/static/notebook.svg" class="card_stats">
							<p>${notebook_words}</p>
						</div>
						<div>
							<img src="/static/question.svg" class="card_stats">
							<p>${question_count}</p>
						</div>
					</div>
				</div>
			</div>
			<div>
				<textarea placeholder="Add description...">
				${description}
				</textarea>
			</div>
			<div>
				<a href="${course['course_id']}"><p>Study</p></a>
			</div>
		</article>
		`
		root.innerHTML += cardHTML
	}
}

function createNavList(courses, root)
{
	for (course of courses) {
		title = (course['title'] == null) ? "Untitled" : course['title']
		navHTML = `
		<a href="/monalect/${course['course_id']}"<div class="course_list"> 
			<img src="/static/notebook.svg">
			<p>${title}</p>
		</div>`
		root.innerHTML += navHTML
	}
}

fetch (`${API_URL}/api/website/monalect`, {
	method: 'GET',
	credentials: "include"})
.then((response) => {
	if (response.ok){
		return response.json()
	}
	else
	{
		console.log("Problem.")
	}
})
.then((data) => {
	username = data['username']
	courses = data['courses']
	cards = document.querySelector("main.monalect div")
	createCourseCards(courses, cards)
	nav_list = document.querySelector("nav.monalect ul")
	createNavList(courses, nav_list)
})

document.querySelector("#create_course").addEventListener("click", () => 
{
	fetch(`${API_URL}/api/course`, {method:'POST', credentials:'include'})
	.then((response) => 
	{
		if (response.ok)
		{
			return response.json()		
		}
		else
		{
			console.log("Problem.")
		}
	})
	.then((data) => 
	{
		course_id = data['course_id']
		window.location.href = `/monalect/${course_id}`
	})
})
