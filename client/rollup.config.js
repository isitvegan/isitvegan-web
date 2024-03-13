import babel from '@rollup/plugin-babel';
import rollupTypescript from '@rollup/plugin-typescript';
import typescript from 'typescript';
import tslib from 'tslib';
import resolve from '@rollup/plugin-node-resolve';

const isProduction = process.env['BUILD_ENV'] === 'production';

const babelOptions = {
  babelHelpers: 'bundled',
  babelrc: false,
  comments: false,
  presets: [
    [
      '@babel/env',
      {
        'modules': false,
        'targets': {
          'browsers': [
            'last 2 chrome versions',
            'last 2 firefox versions',
            'last 2 safari versions',
            'last 2 ios_saf versions',
            'last 2 edge versions',
          ]
        }
      }
    ]
  ]
}

if (isProduction) {
  babelOptions.presets.push(['minify'])
}

const plugins = [
  rollupTypescript({ typescript, tslib, tsconfig: 'tsconfig.json' }),
  resolve(),
  babel(),
];

export default {
  plugins: plugins,
  input: 'src/main.tsx',
  output: {
    file: 'build/main.js',
    sourcemap: !isProduction,
    format: 'iife',
  },
};
