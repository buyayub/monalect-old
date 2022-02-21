sign_up = document.querySelector("#sign-up")

if (sign_up) 
{
	sign_up.addEventListener("submit", (event) => 
	{
		event.preventDefault();

		const data = new FormData(sign_up);
		objectData = { 	username : data.get('username'),
				email: data.get('email'),
				password: data.get('password'),
				recaptcha: data.get('g-recaptcha-response')}

		fetch("/api/register", {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(objectData)
		})
		.then((response) =>
		{
			if (response.status == 201)
			{
				
			}
			else
			{

			}
		});
	});
};
