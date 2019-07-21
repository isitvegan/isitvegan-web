import { h, render, Component } from 'preact';
import { SearchInput, SearchInputType } from './components/search-input';
import { SearchResults } from './components/search-results';
import { SearchScopeBar } from './components/search-scope-bar';
import { SearchScope } from './search-scope';

interface GlobalAppState {
  query: string,
  selectedScope: SearchScope,
}

interface AppState {
  query: string,
  selectedScope: SearchScope,
}

function getGlobalAppState(): GlobalAppState | null {
  return window.history.state;
}

function setGlobalAppState(state: GlobalAppState) {
  window.history.replaceState(state, '');
}

class App extends Component<{}, AppState> {
  constructor() {
    super()

    this._onSearch = this._onSearch.bind(this);
    this._onSelectScope = this._onSelectScope.bind(this);

    const { query, selectedScope } = getGlobalAppState() || { query: '', selectedScope: SearchScope.Names };

    this.state = { query, selectedScope };
  }

  render(_props: {}, { query, selectedScope }: AppState) {
    const placeholderItems = ['Wool', 'E120', 'Cider', '…'];
    const placeholder = placeholderItems.join(', ');

    return (
      <div>
        <div class='search-bar'>
          <div class='inner'>
              <span class='text -before'>Is</span>
              <SearchInput query={query} className='input' type={mapToSearchInputType(selectedScope)}
                           placeholder={placeholder} onSearch={this._onSearch} />
              <SearchScopeBar selectedScope={selectedScope} onSelectScope={this._onSelectScope} />
              <span class='text -after'>Vegan?</span>
          </div>
        </div>
        <SearchResults query={query.trim()} scope={selectedScope} onSearchTermClick={this._onSearch} />
      </div>
    )
  }

  private _onSelectScope(selectedScope: SearchScope) {
    this.setState({ selectedScope });
    this._updateGlobalAppState({ selectedScope });
  }

  private _onSearch(query: string) {
    this.setState({ query });
    this._updateGlobalAppState({ query });
  }

  private _updateGlobalAppState(updates: Partial<AppState>) {
    setGlobalAppState({ query: this.state.query, selectedScope: this.state.selectedScope, ...updates });
  }
}

const mapToSearchInputType = (scope: SearchScope): SearchInputType => {
  switch (scope) {
    case SearchScope.Names:
      return SearchInputType.Default;
    case SearchScope.ENumbers:
      return SearchInputType.NumbersOnly;
  }
}

render(<App />, document.body);
