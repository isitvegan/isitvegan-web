const cssnano = require('cssnano');

const plugins = [
  cssnano({
    preset: 'default',
  })
];

module.exports = { plugins };
