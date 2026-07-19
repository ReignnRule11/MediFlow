// components/patient/UploadProgress.tsx - Enhanced upload with extraction feedback

'use client';

import { useState, FormEvent } from 'react';
import { useDocumentUpload } from '@/lib/use-data';
import { DocumentType, ExtractedData } from '@/lib/types';

interface UploadProgressProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

interface ExtractionSummary {
  medications: number;
  labs: number;
  diagnoses: number;
  appointments: number;
}

export function UploadProgress({ onSuccess, onError }: UploadProgressProps) {
  const [documentType, setDocumentType] = useState<DocumentType>('prescription');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [extractionSummary, setExtractionSummary] = useState<ExtractionSummary | null>(null);
  const [showPreview, setShowPreview] = useState(false);
  const { uploadDocument, isLoading, uploadProgress, uploadedDocument, error } = useDocumentUpload();

  const handleFileSelect = (file: File) => {
    if (file.size > 50 * 1024 * 1024) {
      onError?.('File size exceeds 50MB limit');
      return;
    }

    if (!['application/pdf', 'image/jpeg', 'image/png'].includes(file.type)) {
      onError?.('Please upload a PDF or image file');
      return;
    }

    setSelectedFile(file);
    setExtractionSummary(null);
    setShowPreview(false);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.add('border-blue-500', 'bg-blue-50');
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!selectedFile) {
      onError?.('Please select a file');
      return;
    }

    const patientId = 'current-patient'; // In real app, get from auth context
    const document = await uploadDocument(selectedFile, patientId, documentType);

    if (document && document.extracted_data) {
      const summary: ExtractionSummary = {
        medications: document.extracted_data.medications?.length || 0,
        labs: document.extracted_data.labs?.length || 0,
        diagnoses: document.extracted_data.diagnoses?.length || 0,
        appointments: document.extracted_data.appointments?.length || 0,
      };

      setExtractionSummary(summary);
      setShowPreview(true);
      onSuccess?.();
    } else if (error) {
      onError?.(error);
    }
  };

  return (
    <div className="space-y-6">
      {/* Document Type Selector */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Document Type
        </label>
        <select
          value={documentType}
          onChange={(e) => setDocumentType(e.target.value as DocumentType)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="prescription">Prescription</option>
          <option value="lab_report">Lab Report</option>
          <option value="discharge_summary">Discharge Summary</option>
          <option value="imaging">Imaging Report</option>
          <option value="procedure_note">Procedure Note</option>
        </select>
      </div>

      {/* Upload Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          selectedFile ? 'border-green-400 bg-green-50' : 'border-gray-300 hover:border-blue-400'
        }`}
      >
        {!isLoading && !selectedFile && (
          <>
            <div className="text-4xl mb-4">📄</div>
            <p className="text-lg font-semibold text-gray-900 mb-2">Drag & Drop Your Document</p>
            <p className="text-sm text-gray-600 mb-4">or</p>
            <label className="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer font-semibold">
              Select File
              <input
                type="file"
                hidden
                accept=".pdf, .jpg, .jpeg, .png"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleFileSelect(file);
                }}
              />
            </label>
            <p className="text-xs text-gray-500 mt-4">PDF or image, up to 50MB</p>
          </>
        )}

        {selectedFile && !isLoading && !showPreview && (
          <>
            <p className="text-lg font-semibold text-green-900 mb-4">✓ {selectedFile.name}</p>
            <button
              type="button"
              onClick={handleSubmit}
              className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold"
            >
              Upload & Extract
            </button>
          </>
        )}

        {isLoading && (
          <div className="space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="text-lg font-semibold text-gray-900">Processing Document...</p>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600">{uploadProgress}% complete</p>
          </div>
        )}

        {showPreview && extractionSummary && (
          <div className="space-y-4">
            <div className="text-5xl mb-4">✨</div>
            <p className="text-xl font-bold text-green-900 mb-6">Extraction Complete!</p>

            {/* Extraction Summary Grid */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              {extractionSummary.medications > 0 && (
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-2xl font-bold text-blue-600">{extractionSummary.medications}</p>
                  <p className="text-sm text-blue-900">Medication{extractionSummary.medications !== 1 ? 's' : ''}</p>
                </div>
              )}
              {extractionSummary.labs > 0 && (
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-2xl font-bold text-green-600">{extractionSummary.labs}</p>
                  <p className="text-sm text-green-900">Lab Value{extractionSummary.labs !== 1 ? 's' : ''}</p>
                </div>
              )}
              {extractionSummary.diagnoses > 0 && (
                <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                  <p className="text-2xl font-bold text-purple-600">{extractionSummary.diagnoses}</p>
                  <p className="text-sm text-purple-900">Diagnosis</p>
                </div>
              )}
              {extractionSummary.appointments > 0 && (
                <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                  <p className="text-2xl font-bold text-orange-600">{extractionSummary.appointments}</p>
                  <p className="text-sm text-orange-900">Appointment</p>
                </div>
              )}
            </div>

            <button
              onClick={() => {
                setSelectedFile(null);
                setExtractionSummary(null);
                setShowPreview(false);
              }}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
            >
              Upload Another Document
            </button>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm font-semibold text-red-900">Upload Failed</p>
          <p className="text-sm text-red-800 mt-1">{error}</p>
        </div>
      )}
    </div>
  );
}
