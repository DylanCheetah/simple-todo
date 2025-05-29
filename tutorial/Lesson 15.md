# Lesson 15: Configure Proxy

Before we continue developing the frontend for our todo list app, let's configure a proxy that will allow us to access our backend via the same host and port as our frontend. Open `simple-todo-frontend/webpack.config.js` and add a `proxy` section to the `devServer` section:
```js
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
        },
        proxy: [
            {
                context: [
                    "/accounts/",
                    "/api/",
                    "/static/",
                ],
                target: "http://localhost:8000"
            }
        ]
    }
};
```

To test the proxy config, open 2 terminals. In the first terminal, switch to the `simple_todo` folder and execute `python manage.py runserver`. In the second terminal, switch to the `simple-todo-frontend` folder and execute `npm start`. Then visit [http://localhost:8080/api/v1/](http://localhost:8080/api/v1/) in a web browser. You should see the homepage of your REST API.
