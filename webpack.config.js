const HtmlWebPackPlugin = require("html-webpack-plugin");
const path = require('path');

module.exports = {
    entry: {
        index: __dirname + '/owo/static/index.js',
        theme: __dirname + "/owo/static/theme.js",
        user: __dirname + "/owo/static/jsx/components/User.js",
        voting: __dirname + "/owo/static/jsx/components/Voting.js",
        addsong: __dirname + "/owo/static/jsx/components/Addsong.js"
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.html$/,
                use: [
                    {
                        loader: "html-loader"
                    }
                ]
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.(woff|woff2|eot|ttf)$/,
                use: [
                    {
                        loader: 'url-loader?limit=100000',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'fonts/'
                        }
                    }
                ]
            },
            {
                test: /\.(png|jp(e*)g|svg)$/,
                use: [
                    {
                        loader: "url-loader",
                        options: {
                            name: '[name].[ext]',
                            limit: 100000,

                        }
                    }
                ]
            }
        ]
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
    output: {
        path: path.resolve(__dirname + '/owo/static/js'),
        filename: '[name].bundle.js'
    },
    plugins: [
        new HtmlWebPackPlugin({
            template: __dirname + "/owo/templates/index.html",
            filename: "./index.html"
        }),
        new HtmlWebPackPlugin({
            template: __dirname + "/owo/templates/addsong.html",
            filename: "./addsong.html"
        }),
        new HtmlWebPackPlugin({
            template: __dirname + "/owo/templates/themevoting.html",
            filename: "./themevoting.html"
        })
    ],
    devServer: {
        host: "0.0.0.0",
        port: 8080,
        publicPath: "0.0.0.0:8080/owo/static/js",
        contentBase: 'owo/static/js'
    }
};