import { h, render, Component } from 'preact';
import { SearchInput } from './components/search-input';
import { SearchResults } from './components/search-results';

interface AppState {
  query: string,
}

class App extends Component<{}, AppState> {
  constructor() {
    super()

    this._onSearch = this._onSearch.bind(this);

    this.state = {
      query: '',
    }
  }

  render(props: {}, { query }: AppState) {
    return (
      <div>
        <div class='search-bar'>
          <div class='inner'>
              <span class='text'>Is</span>
              <SearchInput query={query} className='input' placeholder='Oat Milk' onSearch={this._onSearch} />
              <span class='text'>vegan?</span>
          </div>
        </div>
        <SearchResults query={query.trim()} onSearchTermClick={this._onSearch} />
      </div>
    )
  }

  private _onSearch(query: string) {
    this.setState({ query })
  }
}

const main = document.querySelector('main') as HTMLMainElement;
render(<App />, main);
