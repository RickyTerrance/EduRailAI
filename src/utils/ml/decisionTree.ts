import { DecisionTreeClassifier } from 'ml-cart';

export function trainDecisionTree(trainingData: number[][], labels: number[]) {
  const dt = new DecisionTreeClassifier();
  dt.train(trainingData, labels);
  return dt;
}

export function predictDecisionTree(model: any, testData: number[][]) {
  return model.predict(testData);
}