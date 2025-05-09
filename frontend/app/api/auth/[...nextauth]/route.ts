import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

// Menyediakan NextAuth dengan konfigurasi
const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET, // Digunakan untuk enkripsi cookie sesi
  session: {
    strategy: 'jwt', // Menyimpan sesi sebagai JWT
  },
  callbacks: {
    async jwt({ token, account }) {
      // Menyimpan informasi akun jika login berhasil
      if (account) {
        token.accessToken = account.access_token;
      }
      return token;
    },
    async session({ session, token }) {
      // Menyimpan akses token ke dalam session
      if (token) {
        session.accessToken = token.accessToken;
      }
      return session;
    },
  },
});

// Ekspor handler sebagai GET dan POST
export { handler as GET, handler as POST };
