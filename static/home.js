form = document.querySelector("#sign-up")
console.log(form)
form.addEventListener("submit", (event) => 
{
	event.preventDefault();

	data = new FormData(form);

	objectData = { 	username : data.get('username'),
			email: data.get('email'),
			password: data.get('password'),
			recaptcha: data.get('g-recaptcha-response')}

	fetch("/api/register", {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(objectData)
	}).then(
		(response)=>{console.log(response)});
})
