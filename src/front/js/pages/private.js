import React, { useState, useEffect, useContext } from "react";
import PropTypes from "prop-types";
import { Link, useParams } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/private.css"; // Import the CSS for styling

export const Private = () => {
    const { store, actions } = useContext(Context);
    const { theid } = useParams();
    const [bgColor, setBgColor] = useState("#000000");

    useEffect(() => {
        actions.getUserById(theid)
        const changeColor = () => {
            const color = `#${Math.floor(Math.random()*16777215).toString(16)}`;
            setBgColor(color);
        };

        const intervalId = setInterval(changeColor, 1000); // Change color every second

        return () => clearInterval(intervalId); // Cleanup interval on component unmount
    }, []);

    // Find user by user_id
    //const user = store.user.find(user => user.id === parseInt(theid));

    return (
        <div className="private-view" style={{ backgroundColor: bgColor }}>
            <div className="content">
                <h1>Welcome, {store.user ? store.user.email : "User"}</h1>
            </div>
        </div>
    );
};
