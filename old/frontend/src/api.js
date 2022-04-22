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

export {lesson, material, course, API_URL};
