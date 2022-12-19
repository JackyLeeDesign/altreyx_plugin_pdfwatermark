// vue.config.js
const HtmlWebpackPlugin = require('html-webpack-plugin')
const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin');
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
    publicPath:".",
    outputDir: "PDFWatermark/PDFWatermark",
    filenameHashing: false,
    css: {
        extract: false,
    },
    configureWebpack: {
      optimization: {
        splitChunks: false // makes there only be 1 js file - leftover from earlier attempts but doesn't hurt
      },
      plugins: [
        new HtmlWebpackPlugin({
          filename: 'index.html', // the output file name that will be created
          template: 'public/index.html', // this is important - a template file to use for insertion
          inlineSource: '.(js|css)$' // embed all javascript and css inline
        }),
        new HtmlWebpackInlineSourcePlugin(HtmlWebpackPlugin),
        new CopyPlugin([
            { from: "alteryx_src/*.xml", to: "[name].[ext]" },
            { from: "alteryx_src/*.png", to: "[name].[ext]" },
            { from: "Placeholder", to: "Supporting_Macros/[name].[ext]" }
        ]),
      ]
    }
  }