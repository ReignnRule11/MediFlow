// lib/validators.ts - Form validation utilities

export interface ValidationErrors {
  [key: string]: string;
}

export const validators = {
  email: (email: string): boolean => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
  },

  password: (password: string): { valid: boolean; errors: string[] } => {
    const errors: string[] = [];

    if (password.length < 8) {
      errors.push('Password must be at least 8 characters');
    }
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain uppercase letter');
    }
    if (!/[0-9]/.test(password)) {
      errors.push('Password must contain number');
    }
    if (!/[^A-Za-z0-9]/.test(password)) {
      errors.push('Password must contain special character');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  },

  fullName: (name: string): boolean => {
    return name.trim().length >= 2 && name.trim().length <= 255;
  },

  phone: (phone: string): boolean => {
    const pattern = /^\+?[1-9]\d{1,14}$/;
    return pattern.test(phone.replace(/\s/g, ''));
  },

  medicationName: (name: string): boolean => {
    return name.trim().length > 0 && name.trim().length <= 255;
  },

  medicationStrength: (strength: string): boolean => {
    const pattern = /^\d+(?:\.\d+)?\s*(mg|mcg|ml|units|%)$/i;
    return pattern.test(strength.trim());
  },

  medicationFrequency: (frequency: string): boolean => {
    return frequency.trim().length > 0;
  },
};

export function validateLoginForm(
  email: string,
  password: string
): { valid: boolean; errors: ValidationErrors } {
  const errors: ValidationErrors = {};

  if (!email || !validators.email(email)) {
    errors.email = 'Invalid email address';
  }

  if (!password) {
    errors.password = 'Password is required';
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors,
  };
}

export function validateSignupForm(
  email: string,
  password: string,
  confirmPassword: string,
  fullName: string
): { valid: boolean; errors: ValidationErrors } {
  const errors: ValidationErrors = {};

  if (!email || !validators.email(email)) {
    errors.email = 'Invalid email address';
  }

  const passwordValidation = validators.password(password);
  if (!passwordValidation.valid) {
    errors.password = passwordValidation.errors[0];
  }

  if (password !== confirmPassword) {
    errors.confirmPassword = 'Passwords do not match';
  }

  if (!validators.fullName(fullName)) {
    errors.fullName = 'Full name must be between 2 and 255 characters';
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors,
  };
}

export function validateMedicationForm(
  name: string,
  strength: string,
  frequency: string,
  startDate: string
): { valid: boolean; errors: ValidationErrors } {
  const errors: ValidationErrors = {};

  if (!validators.medicationName(name)) {
    errors.name = 'Medication name is required';
  }

  if (!validators.medicationStrength(strength)) {
    errors.strength = 'Invalid strength format (e.g., 500mg, 10mcg)';
  }

  if (!validators.medicationFrequency(frequency)) {
    errors.frequency = 'Frequency is required';
  }

  if (!startDate) {
    errors.startDate = 'Start date is required';
  } else if (new Date(startDate) > new Date()) {
    errors.startDate = 'Start date cannot be in the future';
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors,
  };
}
