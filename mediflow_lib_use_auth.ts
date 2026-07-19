// lib/use-auth.ts - Authentication hook

'use client';

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { User, AuthToken, ApiResponse, LoginRequest, SignupRequest } from './types';
import { apiClient } from './api-client';

interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, full_name: string) => Promise<void>;
  logout: () => Promise<void>;
  error: string | null;
  clearError: () => void;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const verifyAuth = useCallback(async () => {
    try {
      if (!apiClient.isAuthenticated()) {
        setUser(null);
        setIsLoading(false);
        return;
      }

      const response = await apiClient.get<User>('/auth/me');
      if (response.success && response.data) {
        setUser(response.data);
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    verifyAuth();
  }, [verifyAuth]);

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.post<AuthToken>('/auth/login', {
        email,
        password,
      });

      if (response.success && response.data) {
        apiClient.setTokens(response.data);
        await verifyAuth();
        router.push('/dashboard');
      } else {
        setError(response.error?.message || 'Login failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setIsLoading(false);
    }
  }, [router, verifyAuth]);

  const signup = useCallback(async (email: string, password: string, full_name: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.post<AuthToken>('/auth/signup', {
        email,
        password,
        full_name,
      });

      if (response.success && response.data) {
        apiClient.setTokens(response.data);
        await verifyAuth();
        router.push('/dashboard');
      } else {
        setError(response.error?.message || 'Signup failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed');
    } finally {
      setIsLoading(false);
    }
  }, [router, verifyAuth]);

  const logout = useCallback(async () => {
    try {
      await apiClient.post('/auth/logout');
    } catch {
      // Ignore errors
    } finally {
      apiClient.clearTokens();
      setUser(null);
      router.push('/login');
    }
  }, [router]);

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    signup,
    logout,
    error,
    clearError: () => setError(null),
  };
}
