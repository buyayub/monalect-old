session = document.querySelector("#session")

session.addEventListener("submit", (event) => 
{
	event.preventDefault();

	data = new FormData(session);
	const user_id = document.cookie
		.split('; ')
		.find(row => row.startsWith('user_id='))
		.split('=')[1];
	const session_id  = document.cookie
		.split('; ')
		.find(row => row.startsWith('session_id='))
		.split('=')[1];
	
	objectData = { 	user_id: user_id,
			session_id: session_id

		}

	fetch("/api/session", {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(objectData)
	})
	.then(
	(response) => {
		if (response.status == 403) { 
			console.log("403")
		}
		else if (response.status == 401) {
			console.log("unverified")
		}
		else if (response.status == 200) {
			console.log("verified")
		}
		else
		{
			console.log("something went wrong")
		}})
	.then((data) =>
	{
		console.log(data)
	})
		.catch((error)=> {
		console.log("Error: ", error)
	})})
