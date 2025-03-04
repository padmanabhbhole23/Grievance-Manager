let statistic=document.getElementById("floatWindow")
statistic.addEventListener("click",(event)=>{
    event.preventDefault();
   document.getElementById("StatisticsWindow").style="display:block";
})
document.getElementById("StatisticsWindow").addEventListener("click",()=>{
    document.getElementById("StatisticsWindow").style="display:none";
})
function redirectTo(page) {
    window.location.href = `/${page}`;
}
function refreshStatus() {
    fetch(window.location.href) // Reload the same page
        .then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(data, 'text/html');

            let newStatus = doc.getElementById("status-text").innerText;
            let progressBar = document.getElementById("progress-bar");

            document.getElementById("status-text").innerText = newStatus;

            let progressValues = {
                "Raised": "0%",
                "Assigned": "30%",
                "Processing": "70%",
                "Resolved": "100%"
            };

            progressBar.style.width = progressValues[newStatus] || "0%";
        })
        .catch(error => console.error("Error updating status:", error));
}

setInterval(refreshStatus, 5000); // Refresh status every 5 seconds
