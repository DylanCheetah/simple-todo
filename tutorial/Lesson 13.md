# Lesson 13: Setup React

Now that we have completed the backend for our todo list app, we need to create the frontend for it. First we need to create a new folder called `simple-todo-frontend` in our main project folder. Your new project structure should look like this:
```
simple_todo/
    accounts/
        static/
            accounts/
                css/
        templates/
            accounts/
    api/
    simple_todo/
simple-todo-frontend/
```

Next, switch to the `simple-todo-frontend` folder in your terminal and execute the following command:
```sh
npm init
```

Follow the prompts. You only need to set the description, author, and license. All other options can be left on their defaults for now.

Now we need to create the following folders:
`simple-todo-frontend/src/`
`simple-todo-frontend/src/assets/`
`simple-todo-frontend/src/components/`
`simple-todo-frontend/src/pages/`

Next, open `simple-todo-frontend/package.json` and add the following dependencies:
```json
  "dependencies": {
    "abortcontroller-polyfill": "^1.7.8",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "react-router-dom": "^6.30.0"
  },
  "devDependencies": {
    "@babel/core": "^7.27.1",
    "@babel/preset-env": "^7.27.2",
    "@babel/preset-react": "^7.27.1",
    "babel-loader": "^10.0.0",
    "css-loader": "^7.1.2",
    "file-loader": "^6.2.0",
    "html-webpack-plugin": "^5.6.3",
    "style-loader": "^4.0.0",
    "webpack": "^5.99.8",
    "webpack-cli": "^6.0.1",
    "webpack-dev-server": "^5.2.1"
  }
```

Add the following scripts to `package.json` as well:
```json
  "scripts": {
    "build": "webpack --mode development",
    "deploy": "webpack",
    "start": "webpack-dev-server --mode development",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
```

Now you can execute `npm install` to install the dependencies.

Next, create `simple-todo-frontend/webpack.config.js` with the following content:
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
        }
    }
};
```

Create `simple-todo-frontend/src/index.html` with the following content:
```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Hello</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div id="root"></div>
    </body>
</html>
```

Create `simple-todo-frontend/src/index.js` with the following content:
```js
import "abortcontroller-polyfill";

import React from "react";
import {createRoot} from "react-dom/client";
import {createBrowserRouter, RouterProvider} from "react-router-dom";

// Import CSS files here


// Create browser router
const router = createBrowserRouter([
    {
        path: "/",
        lazy: () => import("./App"),
        children: [
            {
                path: "/",
                lazy: () => import("./pages/Home")
            }
        ]
    }
]);

// Create root
const root = createRoot(document.querySelector("#root"));
root.render(
    <React.StrictMode>
        <RouterProvider router={router}/>
    </React.StrictMode>
);
```

Create `simple-todo-frontend/src/App.js` with the following content:
```js
import React from "react";
import {Outlet} from "react-router-dom";
import NavBar from "./components/NavBar";


export function Component() {
    return (
        <div>
            <NavBar/>
            <Outlet/>
        </div>
    );
}
```

Create `simple-todo-frontend/src/components/NavBar.js` with the following content:
```js
import React from "react";
import {Link} from "react-router-dom";


export default function NavBar() {
    return (
        <div>
		    NavBar content goes here.
		</div>
    );
}
```

Create `simple-todo-frontend/src/pages/Home.js` with the following content:
```js
import React, {useState} from "react";


export function Component() {
    return (
        <div>
            Homepage content here.
        </div>
    );
}
```
