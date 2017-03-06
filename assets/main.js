let version = "1.0";
var entries = 0;
var successfulEntries = 0;

function incrementEntries(success) {
	entries++;
	if (success) successfulEntries++;
	document.getElementById("total-entries").innerHTML = entries;
	document.getElementById('successful-entries').innerHTML = successfulEntries;
}

function log(msg, red) {
	var row = document.createElement("span");
	if (red) row.style = "color: red;";
	var br = document.createElement("br");
	var log = document.getElementById("log");
	row.innerHTML = msg;
	log.insertBefore(br, log.firstChild);
	log.insertBefore(row, log.firstChild);
}

function submit(line) {
	log(line);
	var req = new XMLHttpRequest();
	req.open("GET", "/submit?line=" + encodeURI(line));
	req.onreadystatechange = function() {
		if(req.readyState == 4) {
			if (req.status == 200) {
				incrementEntries(true);
			}
			else {
				log("Failed to submit: " + req.response, true);
				incrementEntries(false);
			}
		}
	}
	req.send();
}

window.onload = function() {
	document.getElementById("version").innerHTML = version;
	navigator.getUserMedia({
		video: true,
		audio: false
	}, (stream) => {
		var video = document.getElementById("webcam");
		video.src = window.URL.createObjectURL(stream);
		// Set height of log to height of video when it shows up
		video.onplaying = () =>	{
			document.getElementById("log").style = "height: " + video.clientHeight + "px";
		}
		video.play();
		var lastTeam = null;
		QCodeDecoder().decodeFromVideo(video, (err, text) => {
			if (text == undefined) return;
			let team = null;
			try {
				team = text.split(",")[0];
			}
			catch (err) {
				log("Scanned code not in correct format - team not found: " + text, true);
				return;
			}
			if (team != lastTeam) {
					lastTeam = team;
					submit(text);
				}
			});
	}, (err) => {
		log("Some garbage happened: " + err, true);
		console.log(err);
	});
}