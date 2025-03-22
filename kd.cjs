require('dotenv').config();  // Load environment variables
const nodemailer = require('nodemailer');
const path = require('path');
const express = require('express');
const multer = require('multer'); 
const fs = require('fs'); // To delete files if email fails

const app = express();
const port = 3001;
EMAIL_USER=rohitkamblein2020@gmail.com;
EMAIL_PASS=Rohit@#####;

// Setup Multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'Files/');  
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname); 
  }
});
const upload = multer({ storage: storage });

// Load email credentials from environment variables
let transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
    }
});

// Handle POST request to receive data and send email
app.post('/send-email', upload.fields([{ name: 'image' }, { name: 'audio' }]), (req, res) => {
    const { code, subject, recipients } = req.body;
      

    if (!req.files['image'] || !req.files['audio']) {
        return res.status(400).send('Missing image or audio file.');
    }

    const imagePath = req.files['image'] ? path.resolve(__dirname, 'Files', req.files['image'][0].filename) : null;
    const audioPath = req.files['audio'] ? path.resolve(__dirname, 'Files', req.files['audio'][0].filename) : null;

    let mailOptions = {
        from: process.env.EMAIL_USER,
        to: recipients || process.env.EMAIL_USER,  // Default recipient
        subject: subject || 'Default Subject',
        html: `<h1 style="color: Aqua">Code Received</h1>
               <p>The code sent is: <pre>${code}</pre></p>`,
        attachments: []
    };

    if (imagePath) {
        mailOptions.attachments.push({ filename: req.files['image'][0].originalname, path: imagePath });
    }
    if (audioPath) {
        mailOptions.attachments.push({ filename: req.files['audio'][0].originalname, path: audioPath });
    }

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.log('Error Occurred:', error);
            
            // Delete files if email fails
            if (imagePath) fs.unlinkSync(imagePath);
            if (audioPath) fs.unlinkSync(audioPath);
            
            return res.status(500).send('Failed to send email');
        } else {
            console.log('Email Sent Successfully to', mailOptions.to);
            return res.status(200).send('Email sent successfully');
        }
    });
});

// Start the server with correct console logging
app.listen(port, () => {
    console.log("Server is running on http://localhost:${port}");
});