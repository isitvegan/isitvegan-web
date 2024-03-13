import { h } from 'preact';
import { Item, State, Source } from '../search-api-return-types';
import { OnSearchTermClick } from './search-results';
import { Component, Attributes } from 'preact';

interface SearchResultItemProps extends Attributes {
  item: Item,
  onSearchTermClick: OnSearchTermClick,
}

export function SearchResultItem({ item, onSearchTermClick }: SearchResultItemProps) {
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
      <Description description={item.description} />
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

function Description({ description }: { description: string }) {
  if (description === "") {
    return null;
  } else {
    return (
      <details class='section'>
        <summary class='title'>Details</summary>
        <p class="content">{description}</p>
      </details>
    );
  }
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
    const onClick = (event: MouseEvent, alternative: string) => {
      event.preventDefault();
      onSearchTermClick(alternative);
    };

    return (
    <span>
      <a href='#' onClick={(event: MouseEvent) => onClick(event, alternative)}>{alternative}</a>
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
          <svg class='icon'>
            <use xlinkHref='/icons/external-link.svg#icon' href='/icons/external-link.svg#icon' />
          </svg>
          <a href={source.value} class='text'>
            {simplifySourceUrl(source.value)}
          </a>
          {source.lastChecked != null && <SourceLastChecked date={source.lastChecked} />}
        </li>
      );
  }
}

function SourceLastChecked({ date }: { date: string }) {
  const locales = determineEnglishLocales();
  const dateTimeFormat = new Intl.DateTimeFormat(locales, { year: 'numeric', month: 'long', day: 'numeric' });
  const formattedDate = dateTimeFormat.format(Date.parse(date));
  return <span class='date'>Last checked: {formattedDate}</span>;
}

function determineEnglishLocales(): string[] {
  const FALLBACK_LOCALE = 'en-GB';
  const userChosenLocales = navigator.languages.filter(isEnglishLocale);
  return [...userChosenLocales, FALLBACK_LOCALE];
}

function isEnglishLocale(language: string): boolean {
  return language.startsWith('en-') || language === 'en';
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

function simplifySourceUrl(url: string): string {
  const WWW_PREFIX = 'www.';
  const parsedUrl = new URL(url);
  const hostname = parsedUrl.hostname;
  return withoutPrefix(hostname, WWW_PREFIX);
}

function withoutPrefix(string: string, prefix: string): string {
  return string.startsWith(prefix)
    ? string.substr(prefix.length)
    : string;
}
