import Papa from 'papaparse';

export interface CSVLoadOptions {
  header?: boolean;
  dynamicTyping?: boolean;
  skipEmptyLines?: boolean;
}

export async function loadCSVData(
  file: string,
  options: CSVLoadOptions = {
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true
  }
) {
  try {
    const response = await fetch(file);
    const csv = await response.text();
    
    return new Promise((resolve, reject) => {
      Papa.parse(csv, {
        ...options,
        complete: (results) => resolve(results.data),
        error: (error) => reject(error)
      });
    });
  } catch (error) {
    console.error('Error loading CSV:', error);
    throw error;
  }
}