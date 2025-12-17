import React, { useState, useEffect } from 'react';
import { File, Eye, AlignLeft } from 'lucide-react';
import { DocumentResponse } from '../types';

interface DocumentPreviewProps {
  document?: DocumentResponse | null;
  file: File | null;
}

export const DocumentPreview: React.FC<DocumentPreviewProps> = ({ document, file }) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'preview' | 'text'>('preview');

  useEffect(() => {
    if (file) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      return () => URL.revokeObjectURL(url);
    }
  }, [file]);

  const isImage = file?.type.startsWith('image/');
  const isPdf = file?.type === 'application/pdf';

  const filename = document?.filename || file?.name || 'Unknown File';
  const fileSize = document?.file_size || file?.size || 0;
  const fileType = document?.file_type || file?.type.split('/').pop() || 'unknown';

  return (
    <div className="bg-white rounded-lg shadow h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <File className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 truncate max-w-[200px]" title={filename}>
              {filename}
            </h3>
            <p className="text-sm text-gray-500">
              {(fileSize / 1024).toFixed(1)} KB • {fileType.toUpperCase()}
            </p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b">
        <button
          onClick={() => setActiveTab('preview')}
          className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 border-b-2 transition-colors ${
            activeTab === 'preview'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          <Eye className="w-4 h-4" />
          Original Document
        </button>
        <button
          onClick={() => setActiveTab('text')}
          className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 border-b-2 transition-colors ${
            activeTab === 'text'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          <AlignLeft className="w-4 h-4" />
          Extracted Text
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden bg-gray-50 p-4">
        {activeTab === 'preview' ? (
          <div className="h-full w-full flex items-center justify-center bg-gray-200 rounded-lg border border-gray-300 overflow-hidden">
            {previewUrl ? (
              isImage ? (
                <img src={previewUrl} alt="Document Preview" className="max-w-full max-h-full object-contain" />
              ) : isPdf ? (
                <iframe src={previewUrl} className="w-full h-full" title="PDF Preview" />
              ) : (
                <div className="text-center text-gray-500">
                  <File className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Preview not available for this file type</p>
                </div>
              )
            ) : (
              <div className="text-center text-gray-500">
                <p>No file to preview</p>
              </div>
            )}
          </div>
        ) : (
          <div className="h-full w-full bg-white rounded-lg border border-gray-200 p-4 overflow-y-auto font-mono text-sm text-gray-700 whitespace-pre-wrap">
            {document?.extracted_text || "No text extracted from this document."}
          </div>
        )}
      </div>
    </div>
  );
};
