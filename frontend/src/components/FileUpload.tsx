import React, { useCallback, useState } from 'react';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { clsx } from 'clsx';

interface FileUploadProps {
  onUpload: (file: File) => Promise<void>;
  isUploading: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUpload, isUploading }) => {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0]);
    }
  }, [onUpload]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  }, [onUpload]);

  return (
    <div
      className={clsx(
        "relative w-full h-64 border-2 border-dashed rounded-lg flex flex-col items-center justify-center transition-colors",
        dragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400",
        isUploading && "opacity-50 cursor-not-allowed"
      )}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        onChange={handleChange}
        disabled={isUploading}
        accept=".pdf,.jpg,.jpeg,.png,.docx,.txt"
      />
      
      {isUploading ? (
        <div className="flex flex-col items-center text-blue-600">
          <Loader2 className="w-12 h-12 animate-spin mb-2" />
          <p className="font-medium">Processing document...</p>
        </div>
      ) : (
        <div className="flex flex-col items-center text-gray-500">
          <Upload className="w-12 h-12 mb-2" />
          <p className="font-medium text-lg">Drag & Drop your medical record here</p>
          <p className="text-sm mt-1">or click to browse</p>
          <div className="flex gap-2 mt-4 text-xs text-gray-400">
            <span className="flex items-center"><FileText className="w-3 h-3 mr-1" /> PDF</span>
            <span className="flex items-center"><FileText className="w-3 h-3 mr-1" /> Images</span>
            <span className="flex items-center"><FileText className="w-3 h-3 mr-1" /> Word</span>
          </div>
        </div>
      )}
    </div>
  );
};
