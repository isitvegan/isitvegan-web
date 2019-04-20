import { h, render, Component } from 'preact';
import { search } from './searchApiProxy';
import { SearchResult } from './searchApiReturnTypes';

interface AppState {
  items: SearchResult[];
  error?: string;
}

class App extends Component<{}, AppState>{
  constructor() {
    super()

    this.state = {
      items: [],
      error: "",
    }
  }

  render(props: {}, state: AppState) {
    return (
      <div>
        <input type='search' onInput={this._onInput.bind(this)} />
        <SearchResults items={state.items} />
        {state.error ? <div>{state.error}</div> : null}
      </div>
    )
  }

  private _onInput(event: Event) {
    search("milk")
      .then((results) => this.setState({ items: results, error: undefined }))
      .catch(() => this.setState({ error: "No idea" }));
  }
}

const SearchResults = ({ items }: { items: SearchResult[] }) => {
  return (
    <ul>
      {items.map((item) => <li>{item.name}</li>)}
    </ul>
  )
}

render(<App />, document.body);
