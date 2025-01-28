import React, { useState } from "react";

const FileUpload = () => {
	const [file, setFile] = useState(null);

	const handleUpload = (event) => {
		setFile(event.target.files[0]);
	};

	return (
		<div className="mb-4">
			<input
				type="file"
				accept="application/pdf"
				onChange={handleUpload}
			/>
			{file && (
				<p className="text-sm text-gray-600 mt-2">
					Uploaded: {file.name}
				</p>
			)}
		</div>
	);
};

export default FileUpload;
