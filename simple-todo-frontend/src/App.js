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
