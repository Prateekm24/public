import React from "react";

const Header = () => {
	return (
		<header className="w-full bg-red-600 text-white py-4 text-center shadow-md">
			<h1 className="text-2xl font-bold">CSII Chatbot</h1>
			<p className="text-sm opacity-80">
				Upload a PDF and ask questions based on its content
			</p>
		</header>
	);
};

export default Header;
