import { Item } from './searchApiReturnTypes';

export async function search(queryString: string, abortSignal: AbortSignal): Promise<Item[]> {
  const response = await fetch(searchUrl(queryString), { signal: abortSignal });
  return response.json();
}

function searchUrl(queryString: string): string {
  return `/search?query=${encodeURIComponent(queryString)}`;
}
