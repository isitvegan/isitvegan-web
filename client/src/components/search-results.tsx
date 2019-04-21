import { Component, h } from 'preact';
import { Item } from '../searchApiReturnTypes';
import { search } from '../searchApiProxy';

export interface SearchResultsProps {
  query: string,
}

enum SearchResultsStateType {
  Initial,
  Loading,
  Loaded,
  Error,
}

type SearchResultsStateInner = { type: SearchResultsStateType.Initial } |
                          { type: SearchResultsStateType.Loading } |
                          { type: SearchResultsStateType.Loaded, items: Item[] } |
                          { type: SearchResultsStateType.Error };

interface SearchResultsState {
  inner: SearchResultsStateInner,
  query: string,
}

export class SearchResults extends Component<SearchResultsProps, SearchResultsState> {
  private abortController?: AbortController;

  constructor(props: SearchResultsProps) {
    super(props);

    this.setState({
      inner: { type: SearchResultsStateType.Initial },
      query: '',
    })
  }

  render(_: SearchResultsProps, state: SearchResultsState) {
    switch (state.inner.type) {
      case SearchResultsStateType.Initial:
        return <div />;
      case SearchResultsStateType.Loading:
        return <Loading />;
      case SearchResultsStateType.Loaded:
        return <Items items={state.inner.items} />
      case SearchResultsStateType.Error:
        return <Error />;
    }
  }

  componentWillReceiveProps(nextProps: SearchResultsProps, _: SearchResultsState) {
    if (this.state.query !== nextProps.query) {
      this.fetchItems(nextProps.query);
    }
  }

  private fetchItems(query: string) {
    this.abortFetchRequest()
    this.abortController = new AbortController()

    this.setState({ inner: { type: SearchResultsStateType.Loading }, query });

    search(query, this.abortController.signal)
      .then((items) => this.onItems(items))
      .catch((error) => this.onError(error))
  }

  private onItems(items: Item[]) {
    const nextState: SearchResultsStateInner = { type: SearchResultsStateType.Loaded, items };
    this.setState({ inner: nextState })
  }

  private onError(error: Error) {
    const ABORT_ERROR_NAME = 'AbortError';

    if (error.name !== ABORT_ERROR_NAME) {
      this.setState({ inner: { type: SearchResultsStateType.Error } }); 
    }
  }

  private abortFetchRequest() {
    if (this.abortController) {
      this.abortController.abort()
      this.abortController = undefined
    }
  }
}

function Error() {
  return <div>Oops an error occurred</div>;
}

function Items({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map((item) => <li>{item.name}</li>)}
    </ul>
  );
}

function Loading () {
  return <div>Loading results...</div>;
}
