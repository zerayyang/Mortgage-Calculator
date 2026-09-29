const express = require("express");
const multer = require("multer");
const { execFile, spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;


// --------------------------------------------------
// Middleware
// --------------------------------------------------

app.use(express.json({ limit: "10mb" }));

app.use(express.static("public"));


// --------------------------------------------------
// PDF Upload Storage
// --------------------------------------------------

const storage = multer.diskStorage({

    destination: function (req, file, cb) {
        cb(null, "uploads/");
    },

    filename: function (req, file, cb) {

        const extension = path.extname(file.originalname);

        const uniqueName =
            Date.now() +
            "-" +
            Math.round(Math.random() * 1E9) +
            extension;

        cb(null, uniqueName);
    }
});


const upload = multer({
    storage: storage,
    limits: {
        fileSize: 15 * 1024 * 1024
    }
});


// --------------------------------------------------
// Upload + Extract Mortgage PDF
// --------------------------------------------------

app.post(
    "/upload",
    upload.single("mortgagePdf"),
    (req, res) => {

        if (!req.file) {

            return res.status(400).json({
                error: "No PDF was uploaded."
            });
        }


        const pdfPath = req.file.path;


        execFile(
            "python3",
            ["web_processor.py", pdfPath],
            {
                maxBuffer: 1024 * 1024 * 10
            },
            (error, stdout, stderr) => {

                // Remove temporary uploaded PDF
                fs.unlink(pdfPath, () => {});


                if (error) {

                    console.error(stderr);

                    // If Python intentionally rejected the document,
                    // send its error message to the browser.
                    const pythonError =
                        stderr.trim();

                    return res.status(400).json({
                        error:
                            pythonError ||
                            "Mortgage document processing failed."
                    });
                }


                try {

                    const mortgageData =
                        JSON.parse(stdout);


                    res.json({
                        message:
                            "Mortgage document processed successfully.",

                        mortgageData:
                            mortgageData
                    });

                } catch (parseError) {

                    console.error(
                        "Python output:",
                        stdout
                    );

                    console.error(
                        parseError
                    );


                    res.status(500).json({
                        error:
                            "Could not read the mortgage extraction results."
                    });
                }
            }
        );
    }
);


// --------------------------------------------------
// Calculate Mortgage
// --------------------------------------------------

app.post("/calculate", (req, res) => {

    const python = spawn(
        "python3",
        ["web_calculator.py"]
    );


    let output = "";
    let errorOutput = "";


    python.stdout.on(
        "data",
        (data) => {

            output +=
                data.toString();
        }
    );


    python.stderr.on(
        "data",
        (data) => {

            errorOutput +=
                data.toString();
        }
    );


    python.on(
        "close",
        (code) => {

            if (code !== 0) {

                console.error(
                    errorOutput
                );


                return res.status(500).json({
                    error:
                        "Mortgage calculation failed."
                });
            }


            try {

                const calculationResults =
                    JSON.parse(output);


                res.json({
                    message:
                        "Mortgage calculated successfully.",

                    calculationResults:
                        calculationResults
                });

            } catch (error) {

                console.error(
                    "Python output:",
                    output
                );

                console.error(
                    error
                );


                res.status(500).json({
                    error:
                        "Could not read mortgage calculation results."
                });
            }
        }
    );


    python.stdin.write(
        JSON.stringify(
            req.body
        )
    );


    python.stdin.end();
});


// --------------------------------------------------
// Mortgage Analysis
// --------------------------------------------------

app.post("/analyze", (req, res) => {

    const python = spawn(
        "python3",
        ["web_analyst.py"]
    );


    let output = "";
    let errorOutput = "";


    python.stdout.on(
        "data",
        (data) => {

            output +=
                data.toString();
        }
    );


    python.stderr.on(
        "data",
        (data) => {

            errorOutput +=
                data.toString();
        }
    );


    python.on(
        "close",
        (code) => {

            if (code !== 0) {

                console.error(
                    errorOutput
                );


                return res.status(500).json({
                    error:
                        "Mortgage analysis failed."
                });
            }


            try {

                const analysis =
                    JSON.parse(output);


                res.json({
                    message:
                        "Mortgage analysis completed.",

                    analysis:
                        analysis
                });

            } catch (error) {

                console.error(
                    "Python output:",
                    output
                );

                console.error(
                    error
                );


                res.status(500).json({
                    error:
                        "Could not read the mortgage analysis."
                });
            }
        }
    );


    python.stdin.write(
        JSON.stringify(
            req.body
        )
    );


    python.stdin.end();
});


// --------------------------------------------------
// Start Server
// --------------------------------------------------

app.listen(PORT, () => {

    console.log(
        `Server running on port ${PORT}`
    );
});