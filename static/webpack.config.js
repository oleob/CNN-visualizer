const webpack = require('webpack');
const path = require('path');

const config = {
  entry:  __dirname + '/js/index.jsx',
  output: {
      //path: __dirname + '/dist',
      path: path.join(__dirname,'..', 'server', 'static', 'js'),
      filename: 'bundle.js',
  },
  resolve: {
      extensions: ['.js', '.jsx', '.css']
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      }
    ]
  },
  node: {
    fs: 'empty'
  }
};
module.exports = config;
