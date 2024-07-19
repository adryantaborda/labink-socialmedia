function getMatchingCities() {
    var input = document.getElementsByName('_!username').value;
    var url = '/searchfor/?_!username=' + input;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data); // Inspect the structure of the data
        var ul = document.getElementById('search-results');
        ul.innerHTML = ''; // Clear previous results
        data.forEach(cityInfo => {
            console.log(cityInfo); // Debug: log each cityInfo object
            var li = document.createElement('li');
            li.textContent = `${cityInfo.city}`; // Ensure backticks are used
            ul.appendChild(li);
        });
    })
    .catch(error => console.error('Error:', error));
}
