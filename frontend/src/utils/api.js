const BASE_URL = "http://localhost:5173";

export const sendMessageToBackend = async (question) => {
	try {
		const response = await fetch(`${BASE_URL}/ask`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ question }),
		});

		const data = await response.json();
		return data.response;
	} catch (error) {
		console.error("Error fetching response:", error);
		return "Error communicating with the server.";
	}
};
