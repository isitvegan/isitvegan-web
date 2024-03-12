import { h, render, Component, Fragment } from 'preact';
import { SearchInput, SearchInputType } from './components/search-input';
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

    this.state = { query };
  }

  render(_props: {}, { query }: AppState) {
    const placeholderItems = ['E123', '300', '…'];
    const placeholder = placeholderItems.join(', ');

    return (
      <Fragment>
        <div class='search-bar'>
          <div class='inner'>
              <span class='title'>Is it Vegan?</span>
              <SearchInput query={query} className='input' type={SearchInputType.NumbersOnly}
                           placeholder={placeholder} onSearch={this._onSearch} />
          </div>
        </div>
        <SearchResults query={query.trim()} onSearchTermClick={this._onSearch} />
      </Fragment>
    )
  }

  private _onSearch(query: string) {
    this.setState({ query });
    this._updateGlobalAppState({ query });
  }

  private _updateGlobalAppState(updates: Partial<AppState>) {
    setGlobalAppState({ query: this.state.query, ...updates });
  }
}

let content = document.querySelector('#js-main-content') || document.body;
render(<App />, content);
