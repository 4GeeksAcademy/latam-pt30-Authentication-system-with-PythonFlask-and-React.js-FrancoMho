import React, { useContext } from "react";
import { Link } from "react-router-dom";
import logo from "/src/front/img/logo4.png"
import { Context } from "../store/appContext.js";


export const Navbar = () => {
	const { store } = useContext(Context);
	return (
		<nav className="navbar navbar-dark bg-dark text-light">
			<div className="container">
				<Link to="/">
					<img 
					className="navbar-brand mb-0 h1 "
					src={logo}
					style={{ height: '50px' }} 
					alt="FM APP Logo" 
					/>
				</Link>
				{/* <div className="ml-auto">
					<Link to="/login">
						<button className="btn btn-outline-success">LOGIN</button>
					</Link>
				</div> */}
				<div className="ml-auto">
					{ !store.userToken && (
						<Link to="/login">
							<button className="btn btn-outline-success">LOGIN</button>
						</Link>
					)}
				</div>

			</div>
		</nav>
	);
};
