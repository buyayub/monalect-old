# MVP Stories 

## Links

* [Journal](journal.md)
 
## Epic: Founder Stories 

I don't know what to name this, but this is the first thing I'm creating so that I can establish the workflow. Documentation can be saved for later, when I actually built it, but the blog, plans, and about need to be handled. The landing page is the 

* [o] Pre-Launch Landing Page 
	* [O] Design & Marketing
		* [O] Content
			* [o] [Keyword List for SEO](.stories/other/landing_keywords.md)
			* [O] Text
				* [X] [Eye grabber(first things users read, reel 'em in)](.stories/other/landing_headline.md)
					* [X] Headline 
					* [X] Supporting Copy 
				* [X] [Small Article (more in-depth overview of the course)](.stories/other/landing_article.md)
					* [X] Headline
					* [X] Product Description
				* [X] [Planned Features](.stories/other/landing_features.md)
				* [ ] Initial Blogpost
			* [-] Media
				* [-] Video
				* [-] Mascot Images
					* [-] Wizard Studying
					* [-] Wizard from SICP
				* [-] Statistics & Graphs
		* [X] Figma Prototype
			* [X] Logo
			* [X] Title
			* [-] Login Form 
				* [-] Username/Email
				* [-] Password
				* [-] Reset Password
				* [-] Sign-up Link
			* [-] Blog's Latest Posts
			* [X] Email Subscription Form
			* [X] Feature suggestions
			* [X] Encourage Sharing 
			* [X] Our Social Media Links
			* [X] Footer
	* [o] Frontend Implementation
		* [ ] Read through Sass tutorial
		* [ ] Setup webpack
		* [ ] Finish landing page
			* [o] [HTML](.stories/other/landing_html.md)
				* [X] Meta tags
				* [ ] Body
	* [ ] Production & Backend
		* [ ] Static generation (moved to webpack)
		* [ ] Deployment script
		* [ ] 
* [ ] Blog
	* [ ] Design
		* [ ] Figma Prototype
	* [ ] Frontend Implementation
* [-] Documentation
* [ ] Plans (Public to-do list)
	* [ ] Design
		* [ ] Figma Prototype
	* [ ] Frontend Implementation
		* [ ] HTML generation
		* [ ] Javascript + CSS
* [ ] About
	* [ ] Design
		* [ ] Figma Prototype
	* [ ] Frontend Implementation
		* [ ] HTML generation
		* [ ] Javascript + CSS
* [ ] Hosting
* [ ] **MOBILE FRIENDLY AND RESPONSIVE**

I might use a static site generator for this

## Epic: User Creation & Management

* [ ] User Creation & Management
	* [ ] [As a user I should be able to access a form to which I can sign up.](.stories/user/form)
	* [ ] [As a user I should be able to confirm my email address](.stories/user/confirm)
	* [ ] [As a user I should still be able to access my account without confirming my email address](.stories/user/account)
	* [ ] [As a user I should be able to automatically login once I register](.stories/user/login)
	* [ ] [As a user I should be able to login](.stories/user/login)

## Epic: Course Management

* [ ] Course Management
* [ ] As a user I should be able to define the title
* [ ] As a user I should be able to define the description
* [ ] As a user I should be able to manage my questions
	* [ ] As a user I should be able to import questions.
	* [ ] As a user I want to attach questions to specific lessons
	* [ ] As a user I want to be able to remove questions from the list if it doesn't belong
* [ ] As a user I should be able to manage my lessons
	* [ ] As a user I should be able to define lesson materials
	* [ ] As a user I want to namelessons
	* [ ] As a user I want to attach course materials to lessons.
	* [ ] As a user I should be able to define the order of my lesssons.
* [ ] As a user I should be able to manage my course materials
	* [ ] As a user I should be able to define a textbook as a course material
		* [ ] As a user I should be able to define the sections of a textbook
		* [ ] As a user I should be able to attach sections to a lesson
		* [ ] As a user I should be able to define the metadata of the textbook
	* [ ] As a user I should be able to define an article as a course material
		* [ ] As a user I should be able to attach an article to a lesson
		* [ ] As a user I should be able to upload an article
* [ ] as a user I should be able to save my course as a draft
* [ ] as a user I should be able to import a course template and modify it to my liking
* [ ] as a user I should be able to export my course after creating them
* [ ] as a user I should be able to access premade courses so I don't even have to think about creation

## Epic: Course Completion 

The actual act of going through a course and studying it. The meat of the program.

* [ ] Course Completion
* [ ] Notebook
	* [ ]  As a user I want to be able to format my notebook.
	* [ ]  As a user I want to be able to access my textbook while writing notes.
	* [ ]  As a user I want to create questions while writing notes.
	* [ ]  As a user I should be able to see how much words I've written.
	* [ ]  As a user I should be able to see progress towards certain goals. 
* [ ]  Text Reader
	* [ ]  As a user I should be able to read my learning materials
	* [ ]  As a user I should be able to see what lesson I'm on when reading a textbook or article
		* [ ]  As a user I should be able to jump to pages at the start of each lesson
	* [ ]  As a user I should be able to access my notebook while reading
	* [ ]  As a user I should be able to create a question while reading
	* [ ]  As a user I should be able to access the last textbook I opened when I open it again
	* [ ]  As a user I should be able to redownload my textbook
	* [ ]  As a user I should be able to highlight my texts (last priority)
* [ ]  Questions
	* [ ]  As a user I should be able to reassign my questions
	* [ ]  As a user I should be able to CRUD operations on a question
	* [ ]  As a user, answers should be hidden from me so I don't spoil myself everytime I want to edit questions
	* [ ]  As a user I should be able to create a test for these questions.
	* [ ]  As a user I should be able to export my questions
	* [ ]  As a user I should be able to review my questions
* [ ]  Goals
	* [ ]  As a user I should be able to CRUD goals
	* [ ]  As a user I should be able to automatically receive goals after they've completed
	* [ ]  As a user I should be able to see my goals as I progress through them on other pages
	* [ ]  As a user I should see a list of my previous completed goals/accomplishments
* [ ]  Quizzes & Exams
	* [ ]  As a user I should be able to quiz myself against questions without worry.
		* [ ]  As a user I should be able to see if I got it wrong right after I answer
	* [ ]  As a user I should be able to examinate myself against questions to formally measure my knowledge.
		* [ ]  As a user I should also be able to do practice exams to see my level without recording my mark
		* [ ]  As a user I shouldn't feel discouraged as I go through these questions that I quit before finishing it
		* [ ]  As a user I should be able to choose the number of questions from each lesson I test against
* [ ]  Completion
	* [ ]  As a user I want to be able to review completed courses
	* [ ]  As a user I want to see how long since I reviewed it so I can restudy it when necessary
	* [ ]  As a user I want to be able to "uncomplete" a course and access it

## Epic: Marketing

Marketing isn't a huge focus for Monalect in the beginning, but having a (free) way to publish to various networks and 

* [ ] Preliminaries
	* [ ] As a marketer, frontend metadata of various pages should allow for easy discovery 
		* [ ] SEO terms
* [ ] Value and content creation
	* [ ] As a marketer, I'd like trivial tools made to attract users
		* [ ] As a marketer, I'd like checklists people can use to become attracted to our website
	* [ ] As a marketer, I'd like videos made that showcase our philosophy and product
	* [ ] [As a marketer, I'd like weekly blogposts to be easily written, as they provide value and authority to the website](.stories/marketing/blog.md)
		* [ ] As a marketer, I'd like the ability to publish blog post at specific time
		* [ ] As a marketer, whenever a blog post is created, I'd like to have it put out to various mediums (pun intended)
		* [ ] As a marketer, I'd like blog posting to be fairly streamlined
