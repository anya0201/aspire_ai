import type { NextConfig } from "next";
import path from "path";

// ✅ Yahan humne base URL aur API URL dono theek se define kar diye hain
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
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
      "img-src 'self' data: blob:",
      "font-src 'self' data:",
      // CSP mein hum sirf domain (BASE_URL) allow karte hain
      `connect-src 'self' ${BASE_URL} ${process.env.NODE_ENV === "development" ? " http://localhost:* ws://localhost:*" : ""}`,
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
          // ✅ Ab Frontend ka /api/... exact Backend ke /api/... par jayega!
          source: "/api/:path*",
          destination: `${API_URL}/:path*`,
        },
      ],
      afterFiles: [],
      fallback: [],
    };
  },
};

export default nextConfig;
