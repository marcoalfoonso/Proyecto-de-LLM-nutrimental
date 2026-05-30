const URL = "./model/";

let model
let webcam

async function init() {

    model = await tmImage.load(
        URL + "model.json",
        URL + "metadata.json"
    );

    // webcam
    webcam = new tmImage.Webcam(400, 400, true);

    await webcam.setup();
    await webcam.play();

    document.body.appendChild(webcam.canvas);

    /*document.getElementById("webcam")
        console.log(webcam)
        console.log(webcam.webcam)
        .srcObject = webcam.webcam;*/

    window.requestAnimationFrame(loop);
}

async function loop() {

    webcam.update();

    setInterval(async()=>{
        await predict();
    },1000);

    //window.requestAnimationFrame(loop);
}

init();

async function predict() {

    const prediction = await model.predict(webcam.canvas);

    console.log(prediction);

}