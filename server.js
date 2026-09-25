const express = require("express");
const multer = require("multer");
const { execFile } = require("child_process");

const app = express();
const PORT = 3000;

// Configure Multer to store uploaded PDFs while keeping the original file extension
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, "uploads/");
    },

    filename: (req, file, cb) => {
        cb(null, Date.now() + "-" + file.originalname);
    }
});

const upload = multer({
    storage: storage
});

// Serve the website files inside the public folder
app.use(express.static("public"));

// Receive a mortgage PDF uploaded from the website
app.post("/upload", upload.single("mortgageFile"), (req, res) => {

    console.log("PDF received:", req.file.originalname);

    // Run the Python mortgage processor and give it the uploaded PDF path
    execFile(
        "python3",
        ["web_processor.py", req.file.path],
        (error, stdout, stderr) => {

            // Check if the Python program failed
            if (error) {
                console.error("Python error:", stderr);

                return res.status(500).json({
                    message: "Mortgage document processing failed."
                });
            }

            // Try converting the JSON returned by Python into a JavaScript object
            let mortgageData;

            try {
                mortgageData = JSON.parse(stdout);
            } catch (error) {
                console.error("Invalid JSON returned by Python:", stdout);

                return res.status(500).json({
                    message: "Could not read the extracted mortgage data."
                });
            }

            // Send the extracted mortgage information back to the website
            res.json({
                message: "Mortgage document processed successfully.",
                mortgageData: mortgageData
            });
        }
    );
});

// Start the Node server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});