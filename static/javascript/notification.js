function my_function() {
    var copyText = document.getElementById("short_link"); // Get the text field
    copyText.select(); // Select the text field
    copyText.setSelectionRange(0, 99999); // For mobile devices
    
    navigator.clipboard.writeText(copyText.value); // Copy the text inside the text field
    alert("Short-URL has been copied!");
    }