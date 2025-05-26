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
