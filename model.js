const tmPose = require("@teachablemachine/pose");
const posenet = require("@tensorflow-models/posenet")
const tf = require("@tensorflow/tfjs");
const fs = require('fs');
const nf = require('node-fetch')

let model, webcam, ctx, labelContainer, maxPredictions;

async function init() {
  // load the model and metadata
  // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
  // Note: the pose library adds a tmPose object to your window (window.tmPose)

  // load Files (model.json , weigths.bin , metadata.json)
  const metadataJSON = JSON.parse(fs.readFileSync('metadata.json').toString());
  const modelJSON = JSON.parse(fs.readFileSync('model.json').toString())
  modelJSON.weightData = fs.readFileSync('./weights.bin', 'binary')

  const poseNetModel = await posenet.load(metadataJSON.modelSettings.posenet)
  const model = await tf.loadLayersModel("we're using a hacky way here", {
    fetchFunc: () => Promise.resolve(new nf.Response(JSON.stringify(modelJSON)))
  })
  const customPoseNet = new tmPose.CustomPoseNet(model, poseNetModel, metadataJSON);

  maxPredictions = customPoseNet.getTotalClasses()

  // at this point the model is created successfully I think




  // Convenience function to setup a webcam
  const size = 200;
  const flip = true; // whether to flip the webcam
  webcam = new tmPose.Webcam(size, size, flip); // width, height, flip
  await webcam.setup(); // request access to the webcam
  await webcam.play();
  window.requestAnimationFrame(loop);

  // append/get elements to the DOM
  const canvas = document.getElementById("canvas");
  canvas.width = size;
  canvas.height = size;
  ctx = canvas.getContext("2d");
  labelContainer = document.getElementById("label-container");
  for (let i = 0; i < maxPredictions; i++) { // and class labels
    labelContainer.appendChild(document.createElement("div"));
  }
}

async function loop(timestamp) {
  webcam.update(); // update the webcam frame
  await predict();
  window.requestAnimationFrame(loop);
}

async function predict() {
  // Prediction #1: run input through posenet
  // estimatePose can take in an image, video or canvas html element
  const { pose, posenetOutput } = await model.estimatePose(webcam.canvas);
  // Prediction 2: run input through teachable machine classification model
  const prediction = await model.predict(posenetOutput);

  for (let i = 0; i < maxPredictions; i++) {
    labelContainer.childNodes[i].innerHTML = prediction[i].className + ": " + prediction[i].probability.toFixed(2);
  }

  // finally draw the poses
  drawPose(pose);
}

function drawPose(pose) {
  if (webcam.canvas) {
    ctx.drawImage(webcam.canvas, 0, 0);
    // draw the keypoints and skeleton
    if (pose) {
      const minPartConfidence = 0.5;
      tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
      tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
    }
  }
}

init()
