const URL = "./model/";

async function init() {

    model = await tmImage.load(
        URL + "model.json",
        URL + "metadata.json"
    );

    // webcam
    webcam = new tmImage.Webcam(400, 400, true);

    await webcam.setup();
    await webcam.play();

    document.getElementById("webcam")
        .srcObject = webcam.webcam;

    window.requestAnimationFrame(loop);
}

async function loop() {

    webcam.update();

    await predict();

    window.requestAnimationFrame(loop);
}

init();