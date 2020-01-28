const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const ENTRY_PATH = './app/frontend/static/app/assets/js/';


module.exports = {
  mode: 'production',
  context: __dirname,
  entry: {
    main: [`${ENTRY_PATH}/index`],
    profile: [`${ENTRY_PATH}/profile`],
    practice: [`${ENTRY_PATH}/practice`],
    dialog_export_practice: [`${ENTRY_PATH}/dialog_export_practices`],
    dashboard: [`${ENTRY_PATH}/dashboard`],
  },
  output: {
      path: path.resolve('./app/frontend/static/app/assets/bundles/'),
      publicPath: '/static/assets/bundles/',
      filename: "[name].js",
      libraryTarget: "global"
  },
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              hmr: process.env.NODE_ENV === 'development',
            },
          },
          'css-loader',
          'sass-loader',
        ],
      },
      {
        test: /\.js?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          presets: ['@babel/preset-env']
        }
      }
    ],
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
    }),
  ]
}
