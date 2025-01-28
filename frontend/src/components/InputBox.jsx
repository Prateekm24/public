import React, { useState } from "react";
import { sendMessageToBackend } from "../utils/api";

const InputBox = () => {
	const [input, setInput] = useState("");
	const [messages, setMessages] = useState([]);

	const handleSendMessage = async () => {
		if (!input.trim()) return;

		setMessages([...messages, { text: input, sender: "user" }]);
		setInput("");

		const response = await sendMessageToBackend(input);
		setMessages([...messages, { text: response, sender: "bot" }]);
	};

	return (
		<div className="mt-4 flex">
			<input
				type="text"
				value={input}
				onChange={(e) => setInput(e.target.value)}
				placeholder="Ask a question..."
				className="flex-grow p-2 border rounded-l"
			/>
			<button
				onClick={handleSendMessage}
				className="bg-red-600 text-white px-4 py-2 rounded-r hover:bg-red-700"
			>
				Send
			</button>
		</div>
	);
};

export default InputBox;
