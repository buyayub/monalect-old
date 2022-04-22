/* 
 * Log-In
 */

login = document.querySelector("#login")
login.hidden = true
login_button = document.querySelector("#login_button")
login_button.addEventListener("click", (event) =>
{
	if (login.hidden) {login.hidden = false}
	else {login.hidden = true}
})

login_captcha = document.querySelector("#login_captcha");
API_URL = "http://localhost:9000"
if (login_captcha !== null) {login_captcha.hidden = true;}

login.addEventListener("submit", (event) => 
{
	event.preventDefault();
	data = new FormData(login);
	objectData = { 	username : data.get('username'),
			password: data.get('password'),
			recaptcha: data.get('g-recaptcha-response')}
	fetch(`${API_URL}/api/login`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(objectData)
	})
	.then((response) => {
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
	.then((data) => {
		console.log(data)
		session_id = data['session_id']
		expiry_date = data['expiry_date']
		user_id  = data['user_id']
		document.cookie = `session_id=${session_id}; Expires=${expiry_date} SameSite=Strict; Secure`
		document.cookie = `user_id=${user_id}; Expires=${expiry_date} SameSite=Strict; Secure`
		window.location.href = "/monalect"

	})
	.catch((error)=> {
		console.log("ERROR: ", error)
	})
});


/*
 * SIGN UP
 */

signup = document.querySelector("#signup")
signup.style.display = "none"
signup_button = document.querySelector("#create")
article = document.querySelector("main.home article") 

signup_button.addEventListener("click", (event) =>
{
	if (signup.display !== "none") {
		article.style.display = "none"
		signup.style.display = "flex"
	}
	else {
		article.style.display = "flex"
		signup.style.display = "none"
	}
})


signup.addEventListener("submit", (event) => 
{
	event.preventDefault();

	data = new FormData(signup);

	objectData = { 	username : data.get('username'),
			email: data.get('email'),
			password: data.get('password'),
			recaptcha: data.get('g-recaptcha-response')}

	fetch(`${API_URL}/api/register`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(objectData)
	})
	.then((response)=>{
		if (response.status == 403) { 
			console.log("Incorrect captcha, or username and password.")
			captcha.hidden = false
		}
		else if (response.status == 401) {
			console.log("Incorrect Username or Password")
			captcha.hidden = true
		}
		else if (response.status == 201) {
			return response.json()
		}
		else {
			console.log("something went wrong")
		}
	})
	.then((data) => {
		session_id = data['session_id']
		expiry_date = data['expiry_date']
		user_id  = data['user_id']
		document.cookie = `session_id=${session_id}; Expires=${expiry_date} SameSite=Strict; Secure`
		document.cookie = `user_id=${user_id}; Expires=${expiry_date} SameSite=Strict; Secure`
		window.location.href = "/monalect"
	})
});
