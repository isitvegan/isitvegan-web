import { Item, Source } from './search-api-return-types';

export async function search(queryString: string): Promise<Item[]> {
  const query = normalize(queryString);
  if (query == '') return [];
  return (await fetchItems())
    .map(item => [item, normalize(item.eNumber).indexOf(query)] as [Item, number])
    .filter(([_, match]) => match != -1)
    .toSorted(([_, left], [__, right]) => left - right)
    .map(([item, _]) => item);
}

function normalize(query: string): string {
  return query
    .replace(/^E|e/, '')
    .replace(/[\s]+/, '')
    .toLowerCase();
}

let cachedItems
async function fetchItems(): Promise<Item[]> {
  cachedItems ??= (await fetch('/build/items.json').then(r => r.json())).map(mapItem);
  return cachedItems;
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
