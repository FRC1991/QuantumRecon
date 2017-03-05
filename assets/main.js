let version = "1.0";

function submit(line) {
	document.getElementById("log").value += line + "\n";
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
				alert("Scanned code not in correct format - team not found: " + text);
				return;
			}
			if (team != lastTeam) {
					lastTeam = team;
					submit(text);
				}
			});
	}, (err) => {
		alert("Some garbage happened: " + err);
		console.log(err);
	});
}