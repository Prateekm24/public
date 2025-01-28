import React from "react";
import Header from "../components/Header";
import HeroSection from "../components/HeroSection";
import FileUpload from "../components/FileUpload";
import ChatWindow from "../components/ChatWindow";
import InputBox from "../components/InputBox";

const Home = () => {
	return (
		<div className="min-h-screen bg-red-50 flex flex-col items-center p-4">
			<Header />
			<HeroSection />
			<div className="w-full max-w-lg bg-white shadow-lg rounded-lg p-4 mt-4">
				<FileUpload />
				<ChatWindow />
				<InputBox />
			</div>
		</div>
	);
};

export default Home;
