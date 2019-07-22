import { h } from 'preact';
import { SearchScope, SEARCH_SCOPES } from '../search-scope';

export type OnSelectSearchScope = (scope: SearchScope) => void;

export interface SearchScopeBarProps {
  selectedScope: SearchScope,
  onSelectScope: OnSelectSearchScope,
}

export const SearchScopeBar = ({ selectedScope, onSelectScope }: SearchScopeBarProps) => {
  return (
    <div class='search-scope-bar'>
      {SEARCH_SCOPES.map((scope) => {
        return <Item scope={scope} onSelect={() => onSelectScope(scope)} selected={scope === selectedScope} />
      })}
    </div>
  )
}

const Item = ({ scope, selected, onSelect }: { scope: SearchScope, selected: boolean, onSelect: () => void }) => {
  return (
    <label class='item'>
      <input type='radio' name='search-scope' class='radio'
             value={scope} onInput={onSelect} checked={selected} />
      <span class='label'>{labelForScope(scope)}</span>
    </label>
  )
}

function labelForScope(scope: SearchScope): string {
  const NO_BREAK_SPACE = '\u{00A0}';
  switch (scope) {
    case SearchScope.Names:
      return 'Search names';
    case SearchScope.ENumbers:
      return `Search E${NO_BREAK_SPACE}numbers`;
  }
}
