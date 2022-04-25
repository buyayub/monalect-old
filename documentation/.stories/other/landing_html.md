### HTML generation

Okay, so because this is the first implementation, I have to figure it out. 

I'm thinking of using staticjinja, as I'm already familiar with jinja. It'll put out the html. Then I'll create a quick script to build the static site using jinja, putting everything together, and then deploy a test server.

I'm thinking of using this for the webapp too, as it basically pushes out a template html file for each page, and then the javascript at the client-end will immediately fill it in with an initial call to the backend REST api. I can cache the hell out of it, and make it highly optimized.

Then I'll just quickly write the js scripts using webpack. A script will then build the javascript, and then build the html. I shouldn't have to build the css, but if I do I'll just the script again. The server will then deploy.

The reason why I'm using python and javascript together and not just javascript is because javascript's templating engines, and javascript's static site generators go for different things, and it'll be the same process anyways. I'm more familiar with python and jinja.

...

Carbon Design System is integrated heavily with javascript. I'm moving templating engine to javascript.
