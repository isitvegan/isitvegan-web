import { Item } from './search-api-return-types';

export async function search(queryString: string, abortSignal: AbortSignal): Promise<Item[]> {
  const response = await fetch(searchUrl(queryString), { signal: abortSignal });
  const data = await response.json();

  return data.map(mapItem);
}

function mapItem(item: any): Item {
  return {
    name: item.name,
    state: item.state,
    description: item.description,
    sources: item.sources,
    alternativeNames: item.alternative_names,
    eNumber: item.e_number,
    veganAlternatives: item.vegan_alternatives,
  }
}

function searchUrl(queryString: string): string {
  return `/api/search?query=${encodeURIComponent(queryString)}`;
}
