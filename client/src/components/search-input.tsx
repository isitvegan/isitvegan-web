import { h } from "preact";

export enum SearchInputType {
  Default,
  NumbersOnly,
}

export interface SearchInputProps {
  className: string,
  query: string,
  placeholder: string,
  type: SearchInputType,
  onSearch: (query: string) => void,
}

export const SearchInput = ({ query, onSearch, className, placeholder, type }: SearchInputProps) => {
  const onInput = (event: Event) => {
    const target = event.target as HTMLInputElement;
    onSearch(target.value);
  };

  const inputMode = mapToHtmlInputMode(type);
  return <input type='search' inputMode={inputMode} value={query} class={className}
                onInput={onInput}
                placeholder={placeholder} autofocus={true} />
}

const mapToHtmlInputMode = (type: SearchInputType): string => {
 switch (type) {
   case SearchInputType.Default:
     return 'search';
   case SearchInputType.NumbersOnly:
     return 'numeric';
 }
}