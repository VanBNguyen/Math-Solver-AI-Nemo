async function solveMath() {
    // Gets input from text box
    let query = document.getElementById("mathInput").value;

    // Assuming this shit is valid llmao
    if (!query) {
        alert("Please enter a math equation.");
        return;
    }


    // Send a POST request to the '/solve' endpoint with the input query
    let response = await fetch("/solve", {
        method: "POST", // HTTP method

        // Set request headers
        headers: { "Content-Type": "application/json" },

        // Convert query into JSON format
        body: JSON.stringify({ query: query })
    });

    // Parse the response as JSON
    let result = await response.json();
    
    // Display the solution or error message in the 'result' element
    document.getElementById("result").innerText = result.solution || result.error;
}
