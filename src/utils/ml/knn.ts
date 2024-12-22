import { KNN } from 'ml-knn';

export function trainKNN(trainingData: number[][], labels: number[], k: number = 3) {
  const knn = new KNN(trainingData, labels, { k });
  return knn;
}

export function predictKNN(model: any, testData: number[][]) {
  return model.predict(testData);
}