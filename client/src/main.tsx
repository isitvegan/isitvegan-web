import { h, render } from 'preact';

function Foo(): JSX.Element {
    return <h1>Hello World</h1>;
}

render(<Foo />, document.body);
