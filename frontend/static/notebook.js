website = {
	API_URL : "http://localhost:5000",
	notebook : document.getElementById("notebook")
}

//fetch(`${API_URL}/api/course/`, {
//	method: "POST",
		

function markit(event) {
	selection = window.getSelection()
	offset = selection.anchorOffset

	selectionNode = selection.anchorNode.parentNode
	console.log(selectionNode)
	markdown = marked.parseInline(selectionNode.innerHTML)
	selectionNode.innerHTML = markdown
	range = document.createRange()
	range.setStart(selectionNode.childNodes[0], offset)
	range.collapse()
	window.getSelection().removeAllRanges()
	window.getSelection().addRange(range)
}

website.notebook.addEventListener("input", markit)

