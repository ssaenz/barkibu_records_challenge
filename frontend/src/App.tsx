import { useState } from 'react';
import axios from 'axios';
import { FileUpload } from './components/FileUpload';
import { DocumentPreview } from './components/DocumentPreview';
import { MedicalRecordEditor } from './components/MedicalRecordEditor';
import { DocumentResponse } from './types';
import { Activity, AlertCircle, Loader2 } from 'lucide-react';

function App() {
  const [isUploading, setIsUploading] = useState(false);
  const [document, setDocument] = useState<DocumentResponse | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setError(null);
    setUploadedFile(file);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post<DocumentResponse>('/api/v1/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setDocument(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to upload document. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center">
          <Activity className="w-8 h-8 text-blue-600 mr-3" />
          <h1 className="text-2xl font-bold text-gray-900">Barkibu Medical Records</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-400 p-4 flex items-center">
            <AlertCircle className="w-5 h-5 text-red-400 mr-2" />
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {!uploadedFile ? (
          <div className="max-w-2xl mx-auto mt-12">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
                Upload Medical Record
              </h2>
              <p className="mt-4 text-lg text-gray-500">
                Upload a PDF, image, or Word document to automatically extract and structure veterinary information.
              </p>
            </div>
            <FileUpload onUpload={handleUpload} isUploading={isUploading} />
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[calc(100vh-12rem)]">
            {/* Left Column: Preview */}
            <div className="h-full overflow-hidden">
              <DocumentPreview document={document} file={uploadedFile} />
            </div>

            {/* Right Column: Editor or Loading */}
            <div className="h-full overflow-hidden">
              {document ? (
                <MedicalRecordEditor 
                  initialData={document.medical_record} 
                  onSave={(newData) => {
                    // In a real app, we would save this back to the server
                    console.log('Updated data:', newData);
                    setDocument(prev => prev ? { ...prev, medical_record: newData } : null);
                  }}
                />
              ) : (
                <div className="h-full flex flex-col items-center justify-center bg-white rounded-lg shadow p-8 text-center">
                  {isUploading ? (
                    <>
                      <Loader2 className="w-12 h-12 text-blue-600 animate-spin mb-4" />
                      <h3 className="text-lg font-medium text-gray-900">Processing Document...</h3>
                      <p className="text-gray-500 mt-2">Extracting information from your file.</p>
                    </>
                  ) : (
                    <div className="text-center">
                       <p className="text-gray-500 mb-4">Upload failed or cancelled.</p>
                       <button 
                         onClick={() => {
                           setUploadedFile(null);
                           setDocument(null);
                           setError(null);
                         }}
                         className="text-blue-600 hover:text-blue-800 font-medium"
                       >
                         Upload another file
                       </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
