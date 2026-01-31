/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://nutrioffshore-veridisambiental-0ea3f22c.koyeb.app',
  },
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://nutrioffshore-veridisambiental-0ea3f22c.koyeb.app';
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
