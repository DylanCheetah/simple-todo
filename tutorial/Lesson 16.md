# Lesson 16: Create Navbar

The next thing we will create is a simple navigation bar. Our todo list app will designed so that it will automatically redirect to the login page if the current user isn't logged in. Therefore, we will only need 2 links in our navbar. The first link will be to the homepage of our app and the second will be to the logout page. The branding item can serve as the link to the homepage and then we just need to add the logout link separately. Open `simple-todo-frontend/src/components/NavBar.js` and modify it like this:
```js
import React from "react";
import {Link} from "react-router-dom";


export default function NavBar() {
    return (
        <div className="navbar navbar-expand-lg bg-body-tertiary">
            <div className="container-fluid">
                <a className="navbar-brand" href="/">Simple Todo</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent" aria-controls="navbarContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                            <a className="nav-link" href="/accounts/logout/">Logout</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
```

When you visit the homepage now, it should look like this:
![image](https://github.com/user-attachments/assets/91231521-6894-43b8-83fe-1b9ecdfdd7f4)
