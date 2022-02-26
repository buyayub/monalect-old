API_URL = "http://localhost:9000"

//createCourseCard(course){`<div>`}

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
	//for course in courses {}
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
