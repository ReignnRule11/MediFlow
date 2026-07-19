// app/(auth)/login/page.tsx - Login page

import { LoginForm } from '@/mediflow_components_auth_LoginForm';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 flex items-center justify-center p-4">
      <LoginForm />
    </div>
  );
}
