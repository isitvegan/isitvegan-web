export interface SearchResult {
  name: string;
  state: State;
  description: string;
  sources: Source[];
}

export interface Source {
  type: SourceType;
  value: string;
}

export type State = "vegan" | "carnist" | "itDepends";

export type SourceType = "url";
