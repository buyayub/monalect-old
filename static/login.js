login = document.querySelector("#log-in")
captcha = document.querySelector(".g-recaptcha")
captcha.hidden = true

login.addEventListener("submit", (event) => 
{
	event.preventDefault();

	data = new FormData(login);

	objectData = { 	username : data.get('username'),
			password: data.get('password'),
			recaptcha: data.get('g-recaptcha-response')}

	fetch("/api/login", {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(objectData)
	})
	.then(
	(response) => {
		if (response.status == 403) { 
			console.log("Incorrect captcha, or username and password.")
			captcha.hidden = false
		}
		else if (response.status == 401) {
			console.log("Incorrect Username or Password")
			captcha.hidden = true
		}
		else if (response.status == 200) {
			return response.json()
		}
		else
		{
			console.log("something went wrong")
		}})
	.then((data) =>
	{
		session_id = data['session_id'][0]
		expiry_date = data['session_id'][1]
		user_id  = data['user_id']
		document.cookie = `session_id=${session_id}; Expires=${expiry_date} SameSite=Strict; Secure`
		document.cookie = `user_id=${user_id}; Expires=${expiry_date} SameSite=Strict; Secure`

	})
		.catch((error)=> {
	})})
