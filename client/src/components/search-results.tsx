import { Component, h } from 'preact';
import { Item, State, Source } from '../search-api-return-types';
import { search } from '../search-api-proxy';

type OnSearchTermClick = (searchTerm: string) => void;

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
      {items.map((item) => <SearchResultItem item={item} onSearchTermClick={onSearchTermClick} />)}
    </div>
  );
}

function SearchResultItem({ item, onSearchTermClick }: { item: Item, onSearchTermClick: OnSearchTermClick }) {
  const headerClass = `header ${colorClassForState(item.state)}`;

  return (
    <article class='item search-result-item'>
      <header class={headerClass}>
          <h2 class='title'>{item.name}</h2>
          <div class='status search-result-item-status'>
              <div class='text'>{labelForState(item.state)}</div>
              <StateIcon state={item.state} />
          </div>
          {item.eNumber ? <span class='enumber'>{item.eNumber}</span> : null}
      </header>
      <div class="section">
        <p class="content">{item.description}</p>
      </div>
      <AlternativeNames names={item.alternativeNames} />
      <VeganAlternatives alternatives={item.veganAlternatives} onSearchTermClick={onSearchTermClick} />
      <Sources sources={item.sources} />
    </article>
  );
}

function StateIcon({ state }: { state: State }) {
  const icon = `${iconForState(state)}#icon`;
  return (
    <svg class='icon'>
        <use xlinkHref={icon} href={icon} />
    </svg>
  )
}

function VeganAlternatives({ alternatives, onSearchTermClick }: { alternatives: string[], onSearchTermClick: OnSearchTermClick }) {
  if (alternatives.length === 0) {
    return null;
  } else {
    return (
      <div class='section'>
        <h3 class='title'>Vegan alternatives</h3>
        <p class='content'>
          {alternatives.map((alternative, i) => <VeganAlternative alternative={alternative} onSearchTermClick={onSearchTermClick} isLast={i === alternatives.length - 1} />)}
        </p>
      </div>
    )
  }
}

function VeganAlternative(
  { alternative, onSearchTermClick, isLast }: { alternative: string, onSearchTermClick: OnSearchTermClick, isLast: boolean }) {
  return (
    <span>
      <a href='#' onClick={() => onSearchTermClick(alternative)}>{alternative}</a>
      {isLast ? null : ', '}
    </span>
  );
}


function AlternativeNames({ names }: { names: string[] }) {
  if (names.length === 0) {
    return null;
  } else {
    return (
      <div class='section'>
        <h3 class='title'>Also known as</h3>
        <p class='content'>{names.join(', ')}</p>
      </div>
    )
  }
}

function Sources({ sources }: { sources: Source[] }) {
  if (sources.length === 0) {
    return null;
  } else {
    return (
      <details class='section'>
        <summary class='title'>Sources</summary>
        <ul class='content links-list'>
          {sources.map((source) => <Source source={source} />)}
        </ul>
      </details>
    )
  }
}

function Source({ source }: { source: Source }) {
  switch (source.type) {
    case 'url':
      return (
        <li class='item'>
          <a href={source.value} class='link'>
            <svg class='icon'>
              <use xlinkHref='/icons/external-link.svg#icon' href='/icons/external-link.svg#icon' />
            </svg>
            <span class='text'>{source.value}</span>
          </a>
        </li>
      );
  }
}

function labelForState(state: State): string {
  switch (state) {
    case 'vegan':
      return 'Vegan';
    case 'carnist':
      return 'Carnist';
    case 'itDepends':
      return 'It Depends';
  }
}

function colorClassForState(state: State): string {
  switch (state) {
    case 'vegan':
      return '-green';
    case 'carnist':
      return '-red';
    case 'itDepends':
      return '-orange';
  }
}

function iconForState(state: State): string {
  switch (state) {
    case 'vegan':
      return '/icons/vegan.svg';
    case 'carnist':
      return '/icons/carnist.svg';
    case 'itDepends':
      return '/icons/it-depends.svg';
  }
}
