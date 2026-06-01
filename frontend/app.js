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

    setInterval(() => {
        webcam.update();
    }, 30);

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

    //transformar datos
    const data = prediction.map(item => ({
        className: item.className,
        probability: item.probability
    }));

    console.log(data);

    //enviar a backend
    await fetch("http://localhost:8000/vision/detect",{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            predictions: data
        })
    });

}