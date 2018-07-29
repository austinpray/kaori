const path = require('path');
const webpack = require("webpack");

module.exports = {
    entry: [
        'whatwg-fetch',
        './kizuna_js/index.js'
    ],
    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: 'kizuna.bundle.js',
        publicPath: "/static/dist/"
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.css$/,
                use: [
                    { loader: "style-loader" },
                    { loader: "css-loader" }
                ]
            }
        ]
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                'NODE_ENV': JSON.stringify(process.env.NODE_ENV)
            }
        }),
    ]
};
