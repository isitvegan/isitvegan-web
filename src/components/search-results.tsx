import { Component, h } from 'preact';
import { Item } from '../search-api-return-types';
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
    const propsMatchWithState = this.state.query === nextProps.query;
    if (!propsMatchWithState) {
      this.fetchItems(nextProps.query);
    }
  }

  componentWillMount() {
    this.fetchItems(this.props.query);
  }

  private fetchItems(query: string) {
    this.setState({ query });

    if (query === '') {
      this.setState({ inner: { type: SearchResultsStateType.Loaded, items: [] }});
    } else {
      search(query)
        .then((items) => this.onItems(items))
        .catch(() => this.onError());
    }
  }

  private onItems(items: Item[]) {
    const nextState: SearchResultsStateInner = { type: SearchResultsStateType.Loaded, items };
    this.setState({ inner: nextState });
  }

  private onError() {
    this.setState({ inner: { type: SearchResultsStateType.Error } }); 
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
