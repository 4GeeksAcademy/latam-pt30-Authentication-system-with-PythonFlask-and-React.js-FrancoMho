const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			isAuthenticated: false,
			userToken: null,
			user: null,
		},
		actions: {
			// Function to handle user signup
			createUser: async (email, password) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/api/user`, {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify({ email, password }),
					});
					const data = await response.json();

					if (response.ok) {
						setStore({ message: "User created successfully" });
						return true
						
					} else if (response.status === 409) {
						// El usuario ya existe
						setStore({ message: "User already exists" });
						alert("User already exists, please try logging in.");

					} else {
						setStore({ message: data.message });
					}
				} catch (error) {
					console.error("Error creating user:", error);
					setStore({ message: "Error creating user" });
				}
			},

			// Function to handle user login
			logIn: async (email, password) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/api/token`, {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify({ email, password }),
					});
					const data = await response.json();

					if (response.ok) {
						setStore({
							isAuthenticated: true,
							userToken: data.token,
							user: data.user,
						});
						return true;
					} else {
						setStore({ message: data.message });
						return false;
					}
				} catch (error) {
					console.error("Error logging in:", error);
					setStore({ message: "Error logging in" });
					return false;
				}
			},

			getUserById: async (id) => {
				try {
					const response = await fetch(`${process.env.BACKEND_URL}/api/user/${id}`)
					const data = await response.json()
					setStore({user: data.user})				
				} catch (error) {
					console.error(error)
				}

			},

			logOut: () => {
                setStore({ user: null });
            }
		}
	};
};

export default getState;
