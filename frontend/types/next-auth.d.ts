import NextAuth from 'next-auth';

declare module 'next-auth' {
  interface Session {
    accessToken?: string; // Menambahkan properti accessToken
  }

  interface User {
    accessToken?: string; // Menambahkan properti accessToken
  }
}
