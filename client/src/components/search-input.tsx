import { h } from "preact";

export interface SearchInputProps {
  className: string,
  query: string,
  placeholder: string,
  onSearch: (query: string) => void,
}

export const SearchInput = ({ query, onSearch, className, placeholder }: SearchInputProps) => {
  const onInput = (event: Event) => {
    const target = event.target as HTMLInputElement;
    onSearch(target.value);
  };

  return <input type='search' value={query} class={className}
                onInput={onInput}
                placeholder={placeholder} />
}
