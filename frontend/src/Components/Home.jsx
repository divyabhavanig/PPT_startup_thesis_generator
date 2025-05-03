import React, {useState} from 'react'
import { jsPDF } from 'jspdf';
const Home = () => {
  const [email, setEmail] = useState('');
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file || !email) {
      alert('Please enter your email and upload a file.');
      return;
    }

    const formData = new FormData();
    formData.append('email', email);
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      console.log('Extracted Text:', data.text);
      setExtractedText(data.text); // Save to state to display if you want
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleDownloadPDF = () => {
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'pt',
      format: 'a4',
    });
  
    const margin = 40;
    const pageHeight = doc.internal.pageSize.height;
  
    const lines = doc.splitTextToSize(extractedText, doc.internal.pageSize.width - margin * 2);
    let y = margin;
  
    lines.forEach((line) => {
      if (y > pageHeight - margin) {
        doc.addPage();
        y = margin;
      }
      doc.text(line, margin, y);
      y += 20; // line height
    });
  
    doc.save('extracted-text.pdf');
  };
  return (
    <div className=' w-screen h-screen flex justify-center items-center bg-amber-200'>
    <button className='absolute top-4 right-4 px-4 py-2 rounded-md hover:bg-red-600'>Logout</button>
    <div className='flex flex-col gap-2 mt-2 items-center'>
      <h1 className=' font-bold text-3xl'>Hello! firstname lastname</h1>
      <h2>Upload the startup pitch deck in PowerPoint format to get the investment thesis</h2>
      <input type='email' placeholder='Enter your email' value={email} onChange={(e) => setEmail(e.target.value)} className=' px-4 py-2 border outline-1 bg-amber-50  text-amber-600 rounded-md w-80' />
      <input type='file' accept='.ppt,.pptx' onChange={handleFileChange} className='px-4 py-2 border outline-1 bg-amber-50  text-amber-600 rounded-md w-80'/>
      <button onClick={handleSubmit} className='mt-4 px-6 py-2 outline-0  rounded-md hover:bg-amber-800'>Submit</button>
      {extractedText && (
        <>
          <div className='mt-4 p-4 bg-amber-50 text-amber-600 rounded-md w-full max-w-xl overflow-auto max-h-64'>
            <h3 className='font-semibold mb-2'>Extracted Text:</h3>
            <pre className='whitespace-pre-wrap'>{extractedText}</pre>
          </div>
            <button 
              onClick={handleDownloadPDF}
              className='mt-4 px-4 py-2 outline-0 rounded-md hover:bg-amber-800'
            >
              Download as PDF
            </button>
          </>
        )}
    </div>
    </div>
    
  );
};

export default Home