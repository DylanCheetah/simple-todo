const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
    entry: path.join(__dirname, "src", "index.js"),
    output: {
        filename: "js/[name].bundle.js",
        path: path.resolve(__dirname, "dist")
    },
    devtool: "source-map",
    module: {
        rules: [
            {
                test: /\.(png|jp(e*)g|svg|gif)$/,
                use: {
                    loader: "file-loader",
                    options: {
                        outputPath: "images/"
                    }
                }
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader"]
            },
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env", "@babel/preset-react"]
                    }
                }
            }
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: path.join(__dirname, "src", "index.html")
        })
    ],
    devServer: {
        historyApiFallback: {
            rewrites: [
                {
                    from: /\^\$/, 
                    to: "/index.html"
                },
                {
                    from: /\^\/favicon.ico\$/,
                    to: "/favicon.ico"
                },
                {
                    from: /\/js\/(.+)/,
                    to: (ctx) => {
                        return ctx.match[0];
                    }
                },
                {
                    from: /\/images\/(.+)/, 
                    to: (ctx) => {
                        return ctx.match[0];
                    }
                }
            ]
        }
    }
};
