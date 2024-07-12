import React, { Component, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";


export const Footer = () => {
	const { actions } = useContext(Context);
	const navigate = useNavigate();

	const handleLogout = () => {
		actions.logOut();
		navigate("/login");  // Redirect to the login page after logging out
	};

	return (
		<footer className="footer mt-auto py-3 text-center bg-black text-light">
			<p>
				Made with <i className="fa fa-heart text-danger" /> in 4 Geeks Academy
			</p>
			<button onClick={handleLogout} className="btn btn-sm btn-outline-secondary">
				Logout
			</button>
		</footer>
	);
}


