import { kmeans } from 'ml-kmeans';

export function performKMeans(data: number[][], k: number) {
  const { clusters, centroids } = kmeans(data, k);
  return {
    clusters,
    centroids
  };
}