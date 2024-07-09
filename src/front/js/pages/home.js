import React, { useContext, useState } from "react";
import PropTypes from "prop-types";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const navigate = useNavigate();

	const handleSignUp = async (event) => {
		event.preventDefault();
		const success = await actions.createUser(email, password);
		console.log(success);
		if (success) {
			navigate("/login");
		} 
	}

	return (
		<div className="card text-dark col-10 mx-auto my-5 p-5">
			<form onSubmit={handleSignUp}>
				<fieldset >
					<legend className="d-flex justify-content-center fs-1 "> SIGN UP </legend>
					<div className="mb-3">
						<label htmlFor="emailInput" className="form-label">User</label>
						<input 
						type="Email" 
						id="EmailInput" 
						className="form-control" 
						placeholder="Email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						required
						/>
					</div>
					<div className="mb-3">
						<label htmlFor="passwordInput" className="form-label">Password</label>
						<input 
						type="password" 
						id="PasswordInput" 
						className="form-control" 
						placeholder=" Password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						required
						/>
							<option>#seccion_to_add_text_if_needed</option>
					</div>
				
					<button type="submit" className="btn btn-primary">Submit</button>
				</fieldset>
			</form>
		</div>
	);
};

Home.propTypes = {
	match: PropTypes.object
};
