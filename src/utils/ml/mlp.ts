import * as tf from '@tensorflow/tfjs';

export async function trainMLP(
  trainingData: number[][],
  labels: number[][],
  epochs: number = 50
) {
  const model = tf.sequential();
  
  model.add(tf.layers.dense({
    units: 64,
    activation: 'relu',
    inputShape: [trainingData[0].length]
  }));
  
  model.add(tf.layers.dense({
    units: 32,
    activation: 'relu'
  }));
  
  model.add(tf.layers.dense({
    units: labels[0].length,
    activation: 'softmax'
  }));

  model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy']
  });

  const xs = tf.tensor2d(trainingData);
  const ys = tf.tensor2d(labels);

  await model.fit(xs, ys, {
    epochs,
    validationSplit: 0.2
  });

  return model;
}