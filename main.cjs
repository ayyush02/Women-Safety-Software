  const nodemailer = require('nodemailer');
  const fs = require('fs');
  const path = require('path');

  // Configure the email transport using SMTP
  const transporter = nodemailer.createTransport({
   host: 'smtp.gmail.com', // Replace with your SMTP server
    port: 587,
    secure: false, // true for 465, false for other ports
    auth: {
      user: 'rohitkamblein2020@gmail.com', // Replace with your email
      pass: 'rohit@2020',    // Replace with your email password
    },
  });

  // Directory containing files to attach
  const directoryPath = path.join(__dirname, 'attachment');

  // Read files from the directory
  fs.readdir(directoryPath, (err, files) => {
    if (err) {
      return console.log('Unable to scan directory: ' + err);
    }

    // Create attachment objects for each file
    const attachments = files.map((file) => {
      return {
        filename: file,
        path: path.join(directoryPath, file),
      };
    });

    // Email options
    const mailOptions = {
      from: '"Rohit Kamble" <rohitkamblein2020@gmail.com>', // Sender address
      to: 'carbona11111@gmail.com',                   // List of recipients
      subject: 'hii Atharva Chavhan',               // Subject line
      text: 'Please find the attached files.',       // Plain text body
      attachments: attachments,                      // Attachments array
    };

    // Send email
    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        return console.log('Error while sending email: ' + error);
      }
      console.log('Email sent: ' + info.response);
    });
  });