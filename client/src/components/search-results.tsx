import { Component, h } from 'preact';
import { Item } from '../search-api-return-types';
import { search } from '../search-api-proxy';
import { SearchResultItem } from './search-result-item';
import { SearchScope } from '../search-scope';

export type OnSearchTermClick = (searchTerm: string) => void;

export interface SearchResultsProps {
  query: string,
  scope: SearchScope,
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
  scope: SearchScope,
}

export class SearchResults extends Component<SearchResultsProps, SearchResultsState> {
  private abortController?: AbortController;

  constructor(props: SearchResultsProps) {
    super(props);

    this.setState({
      inner: { type: SearchResultsStateType.Loaded, items: [] },
      query: '',
      scope: SearchScope.Names,
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
    const propsMatchWithState = this.state.query === nextProps.query &&
                                this.state.scope === nextProps.scope;
    if (!propsMatchWithState) {
      this.fetchItems(nextProps.query, nextProps.scope);
    }
  }

  componentWillMount() {
    this.fetchItems(this.props.query, this.props.scope);
  }

  private fetchItems(query: string, scope: SearchScope) {
    this.abortFetchRequest();
    this.abortController = new AbortController();

    this.setState({ query, scope });

    if (query === '') {
      this.setState({ inner: { type: SearchResultsStateType.Loaded, items: [] }});
    } else {
      search(query, scope, this.abortController.signal)
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
