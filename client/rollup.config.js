import babel from 'rollup-plugin-babel';
import uglify from 'rollup-plugin-uglify';
import rollupTypescript from 'rollup-plugin-typescript2';
import typescript from 'typescript';
import tslib from 'tslib';
import resolve from 'rollup-plugin-node-resolve';

const isProduction = process.env['BUILD_ENV'] === 'production';

const plugins = [
  rollupTypescript({ typescript, tslib, tsconfig: 'tsconfig.json', allowNonTsExtensions: true }),
  resolve(),
  babel({
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
  }),
];

if (isProduction) {
  plugins.push(uglify);
}

export default {
  plugins: plugins,
  input: 'src/main.tsx',
  output: {
    file: 'build/main.js',
    sourcemap: !isProduction,
    format: 'iife',
  },
};
