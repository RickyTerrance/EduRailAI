export function normalizeData(data: number[][]) {
  const normalized = data.map(row => {
    const sum = row.reduce((acc, val) => acc + val, 0);
    return row.map(val => val / sum);
  });
  return normalized;
}

export function standardizeData(data: number[][]) {
  const means = calculateMeans(data);
  const stds = calculateStds(data, means);
  
  return data.map(row => 
    row.map((val, i) => (val - means[i]) / stds[i])
  );
}

function calculateMeans(data: number[][]) {
  const sums = data.reduce((acc, row) => 
    row.map((val, i) => (acc[i] || 0) + val)
  , new Array(data[0].length).fill(0));
  
  return sums.map(sum => sum / data.length);
}

function calculateStds(data: number[][], means: number[]) {
  const squaredDiffs = data.map(row =>
    row.map((val, i) => Math.pow(val - means[i], 2))
  );
  
  const variances = calculateMeans(squaredDiffs);
  return variances.map(variance => Math.sqrt(variance));
}