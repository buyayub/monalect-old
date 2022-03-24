website = {
	API_URL : "http://localhost:5000",
	notebook : document.getElementById("notebook")
}

//fetch(`${API_URL}/api/course/`, {
//	method: "POST",
		

function markit(event) {
	selection = window.getSelection()
	selectionNode = selection.anchorNode.parentNode

	markdown = marked.parseInline(selectionNode.innerHTML)
	dummy = document.createElement("div")
	dummy.innerHTML = markdown
	console.log(dummy)
}

website.notebook.addEventListener("input", markit)

