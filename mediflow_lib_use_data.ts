// lib/use-data.ts - Data fetching hooks

'use client';

import { useState, useCallback, useEffect } from 'react';
import { Medication, Document, TimelineEvent, PaginatedResponse, ApiResponse } from './types';
import { apiClient } from './api-client';

export function useMedications(patientId: string) {
  const [medications, setMedications] = useState<Medication[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMedications = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<PaginatedResponse<Medication>>(
        `/api/patients/${patientId}/medications`
      );

      if (response.success && response.data) {
        setMedications(response.data.items);
      } else {
        setError(response.error?.message || 'Failed to fetch medications');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  }, [patientId]);

  useEffect(() => {
    if (patientId) {
      fetchMedications();
    }
  }, [patientId, fetchMedications]);

  return { medications, isLoading, error, refetch: fetchMedications };
}

export function useTimeline(patientId: string) {
  const [events, setEvents] = useState<TimelineEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTimeline = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<TimelineEvent[]>(
        `/api/patients/${patientId}/timeline`
      );

      if (response.success && response.data) {
        const sorted = response.data.sort((a, b) =>
          new Date(b.event_date).getTime() - new Date(a.event_date).getTime()
        );
        setEvents(sorted);
      } else {
        setError(response.error?.message || 'Failed to fetch timeline');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  }, [patientId]);

  useEffect(() => {
    if (patientId) {
      fetchTimeline();
    }
  }, [patientId, fetchTimeline]);

  return { events, isLoading, error, refetch: fetchTimeline };
}

export function useDocumentUpload() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedDocument, setUploadedDocument] = useState<Document | null>(null);

  const uploadDocument = useCallback(async (
    file: File,
    patientId: string,
    documentType: string
  ): Promise<Document | null> => {
    setIsLoading(true);
    setError(null);
    setUploadProgress(0);

    try {
      // Validate file size (max 50MB)
      if (file.size > 50 * 1024 * 1024) {
        setError('File size exceeds 50MB limit');
        setIsLoading(false);
        return null;
      }

      const formData = new FormData();
      formData.append('file', file);
      formData.append('document_type', documentType);
      formData.append('patient_id', patientId);

      // Use XMLHttpRequest for progress tracking
      return new Promise((resolve) => {
        const xhr = new XMLHttpRequest();

        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            setUploadProgress(Math.round((e.loaded / e.total) * 100));
          }
        });

        xhr.addEventListener('load', () => {
          if (xhr.status === 202 || xhr.status === 200) {
            try {
              const response = JSON.parse(xhr.responseText);
              setUploadedDocument(response.data);
              setUploadProgress(100);
              resolve(response.data);
            } catch {
              setError('Failed to parse upload response');
              resolve(null);
            }
          } else {
            try {
              const response = JSON.parse(xhr.responseText);
              setError(response.error?.message || 'Upload failed');
            } catch {
              setError('Upload failed');
            }
            resolve(null);
          }
        });

        xhr.addEventListener('error', () => {
          setError('Network error during upload');
          resolve(null);
        });

        xhr.open(
          'POST',
          `${process.env.NEXT_PUBLIC_API_URL}/api/documents/upload`
        );
        const token = localStorage.getItem('access_token');
        if (token) {
          xhr.setRequestHeader('Authorization', `Bearer ${token}`);
        }

        xhr.send(formData);
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    uploadDocument,
    isLoading,
    error,
    uploadProgress,
    uploadedDocument,
  };
}

export function useCheckInteractions(medicationId: string) {
  const [interactions, setInteractions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const checkInteractions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.get<any[]>(
        `/api/medications/${medicationId}/interactions`
      );

      if (response.success && response.data) {
        setInteractions(response.data);
      } else {
        setError(response.error?.message || 'Failed to check interactions');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  }, [medicationId]);

  return { interactions, isLoading, error, checkInteractions };
}
