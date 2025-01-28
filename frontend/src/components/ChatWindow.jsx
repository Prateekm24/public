import React, { useState } from "react";

const ChatWindow = () => {
	const [messages, setMessages] = useState([]);

	return (
		<div className="h-64 overflow-y-auto border p-2 bg-white rounded shadow">
			{messages.map((msg, index) => (
				<div
					key={index}
					className={`p-2 my-1 rounded ${
						msg.sender === "user" ? "bg-red-200" : "bg-gray-200"
					}`}
				>
					{msg.text}
				</div>
			))}
		</div>
	);
};

export default ChatWindow;
