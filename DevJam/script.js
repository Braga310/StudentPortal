const form = document.querySelector('form');
const resultsDiv = document.querySelector('#results');

form.addEventListener('submit', (e) => {
	e.preventDefault();
	const studentId = form.elements.student_id.value;
	if (studentId) {
		getResults(studentId);
	}
});

function getResults(studentId) {
	fetch(`get_results.php?student_id=${studentId}`)
		.then(response => response.json())
		.then(data => {
			if (data) {
				showResults(data);
			} else {
				showError('No results found');
			}
		})
		.catch(error => showError(error.message));
}

function showResults(data) {
	let html = '';
	html += `<h2>${data.student_name}'s Results</h2>`;
	html += `<table>`;
	html += `<tr><th>Subject</th><th>Marks</th></tr>`;
	data.results.forEach(result => {
		html += `<tr><td>${result.subject}</td><td>${result.marks}</td></tr>`;
	});
	html += `</table>`;
	resultsDiv.innerHTML = html;
}

function showError(message) {
	resultsDiv.innerHTML = `<p class="error">${message}</p>`;
}
