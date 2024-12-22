import { RandomForestClassifier } from 'ml-random-forest';

export function trainRandomForest(
  trainingData: number[][],
  labels: number[],
  nTrees: number = 100
) {
  const rf = new RandomForestClassifier({ nEstimators: nTrees });
  rf.train(trainingData, labels);
  return rf;
}

export function predictRandomForest(model: any, testData: number[][]) {
  return model.predict(testData);
}