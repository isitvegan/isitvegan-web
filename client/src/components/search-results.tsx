import { Component, h } from 'preact';
import { Item, State, Source } from '../search-api-return-types';
import { search } from '../search-api-proxy';
import { SearchResultItem } from './search-result-item';

export type OnSearchTermClick = (searchTerm: string) => void;

export interface SearchResultsProps {
  query: string,
  onSearchTermClick: OnSearchTermClick,
}

enum SearchResultsStateType {
  Initial,
  Loading,
  Loaded,
  Error,
}

type SearchResultsStateInner =  { type: SearchResultsStateType.Loaded, items: Item[] } |
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
      inner: { type: SearchResultsStateType.Loaded, items: [] },
      query: '',
    })
  }

  render(props: SearchResultsProps, state: SearchResultsState) {
    switch (state.inner.type) {
      case SearchResultsStateType.Loaded:
        return <SearchResultItems items={state.inner.items} onSearchTermClick={props.onSearchTermClick} />
      case SearchResultsStateType.Error:
        return <Error />;
    }
  }

  componentWillReceiveProps(nextProps: SearchResultsProps, _: SearchResultsState) {
    if (this.state.query !== nextProps.query) {
      this.fetchItems(nextProps.query);
    }
  }

  componentWillMount() {
    this.fetchItems(this.props.query);
  }

  private fetchItems(query: string) {
    this.abortFetchRequest();
    this.abortController = new AbortController();

    this.setState({ query });

    if (query === '') {
      this.setState({ inner: { type: SearchResultsStateType.Loaded, items: [] }});
    } else {
      search(query, this.abortController.signal)
        .then((items) => this.onItems(items))
        .catch((error) => this.onError(error));
    }
  }

  private onItems(items: Item[]) {
    const nextState: SearchResultsStateInner = { type: SearchResultsStateType.Loaded, items };
    this.setState({ inner: nextState });
  }

  private onError(error: Error) {
    const ABORT_ERROR_NAME = 'AbortError';

    if (error.name !== ABORT_ERROR_NAME) {
      this.setState({ inner: { type: SearchResultsStateType.Error } }); 
    }
  }

  private abortFetchRequest() {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = undefined;
    }
  }
}

function Error() {
  return <div>There was an error processing your request</div>;
}

function SearchResultItems({ items, onSearchTermClick }: { items: Item[], onSearchTermClick: OnSearchTermClick }) {
  return (
    <div class='search-results'>
      {items.map((item) => <SearchResultItem key={item.slug} item={item} onSearchTermClick={onSearchTermClick} />)}
    </div>
  );
}
