export interface Item {
  name: string;
  state: State;
  description: string;
  sources: Source[];
  alternativeNames: string[],
  eNumber?: string,
}

export interface Source {
  type: SourceType;
  value: string;
}

export type State = "vegan" | "carnist" | "itDepends";

export type SourceType = "url";
