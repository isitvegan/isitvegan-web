import { h, render, Component } from 'preact';
import { SearchInput } from './components/search-input';
import { SearchResults } from './components/search-results';

interface GlobalAppState {
  query: string,
}

interface AppState {
  query: string,
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

    const { query } = getGlobalAppState() || { query: '' };

    this.state = { query }
  }

  render(props: {}, { query }: AppState) {
    const placeholderItems = ['Wool', 'E120', 'Cider', '…'];
    const placeholder = placeholderItems.join(', ');

    return (
      <div>
        <div class='search-bar'>
          <div class='inner'>
            <span class='text'>Is</span>
            <SearchInput query={query} className='input' placeholder={placeholder} onSearch={this._onSearch} />
            <span class='text'>Vegan?</span>
          </div>
        </div>
        <SearchResults query={query.trim()} onSearchTermClick={this._onSearch} />
      </div>
    )
  }

  private _onSearch(query: string) {
    this.setState({ query });
    setGlobalAppState({ query });
  }
}

render(<App />, document.body);
