import { Item, Source } from './search-api-return-types';
import { SearchScope } from './search-scope';

export async function search(queryString: string, scope: SearchScope, abortSignal: AbortSignal): Promise<Item[]> {
  const response = await fetch(searchUrl(queryString, scope), { signal: abortSignal });
  const data = await response.json();

  return data.map(mapItem);
}

function mapItem(item: any): Item {
  return {
    name: item.name,
    state: item.state,
    description: item.description,
    sources: (item.sources as any[]).map(mapSource),
    alternativeNames: item.alternative_names,
    eNumber: item.e_number,
    veganAlternatives: item.vegan_alternatives,
    slug: item.slug,
  }
}

function mapSource(source: any): Source {
  return {
    type: source.type,
    value: source.value,
    lastChecked: source.last_checked,
  }
}

function searchUrl(queryString: string, scope: SearchScope): string {
  return `/api/search?query=${encodeURIComponent(queryString)}&scope=${searchScopeToString(scope)}`;
}

function searchScopeToString(scope: SearchScope): string {
  switch (scope) {
    case SearchScope.Names:
      return 'names';
    case SearchScope.ENumbers:
      return 'eNumber';
  }
}