import { SearchResult } from "./searchApiReturnTypes";

export function search(queryString: string): Promise<SearchResult[]> {
  return fetch(searchUrl(queryString)).then((response) => response.json());
}

function searchUrl(queryString: string): string {
  const url = new URL('/search');
  url.searchParams.append('query', queryString);
  return url.toString();
}
