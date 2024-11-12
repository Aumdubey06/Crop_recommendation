function getPrediction() {
    const formData = {
        Nitrogen: document.getElementById("nitrogen").value,
        Phosphorus: document.getElementById("phosphorus").value,
        Potassium: document.getElementById("potassium").value,
        Temperature: document.getElementById("temperature").value,
        Humidity: document.getElementById("humidity").value,
        pH: document.getElementById("ph").value,
        Rainfall: document.getElementById("rainfall").value,
        Region_Central_India: document.getElementById("region_central").checked ? 1 : 0,
        Region_Eastern_India: document.getElementById("region_eastern").checked ? 1 : 0,
        Region_North_Eastern_India: document.getElementById("region_northeastern").checked ? 1 : 0,
        Region_Northern_India: document.getElementById("region_northern").checked ? 1 : 0,
        Region_Other: document.getElementById("region_other").checked ? 1 : 0,
        Region_Western_India: document.getElementById("region_western").checked ? 1 : 0
    };

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.prediction !== undefined) {
            document.getElementById("result").innerHTML = "Recommended Crop: " + data.prediction;
        } else {
            document.getElementById("result").innerHTML = "Error: " + data.error;
        }
    })
    .catch(error => {
        console.error("Error during fetch:", error);
        document.getElementById("result").innerHTML = "Error during fetch.";
    });
}
