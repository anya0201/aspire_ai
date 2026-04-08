import type { NextConfig } from "next";
import path from "path";

// 🔥 HARDCODED API URL - Isse Vercel Env Var ka chakkar khatam
const BASE_URL = "https://aspireai-production.up.railway.app";
const API_URL = `${BASE_URL}/api`;

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-XSS-Protection", value: "1; mode=block" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-eval' 'unsafe-inline'",
      "style-src 'self' 'unsafe-inline'",
      "img-src * data: blob:",
      "font-src 'self' data:",
      // 🔥 'connect-src *' allow karta hai browser ko kisi bhi backend se baat karne ke liye
      "connect-src *", 
      "frame-ancestors 'none'",
    ].join("; "),
  },
];

const nextConfig: NextConfig = {
  outputFileTracingRoot: path.join(__dirname, "..", ".."),
  turbopack: {
    root: path.join(__dirname, "..", ".."),
  },
  skipTrailingSlashRedirect: true,
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: securityHeaders,
      },
    ];
  },
  async rewrites() {
    return {
      beforeFiles: [
        {
          source: "/api/chat",
          destination: `${API_URL}/chat/`,
        },
        {
          source: "/api/chat/",
          destination: `${API_URL}/chat/`,
        },
        {
          source: "/api/:path*",
          destination: `${API_URL}/:path*`, // Ye seedha Railway par bhejega!
        },
      ],
      afterFiles: [],
      fallback: [],
    };
  },
};

export default nextConfig;
