// next-auth.config.js

const nextAuthConfig = {
  providers: [
    {
      id: "google",
      name: "Google",
      type: "oauth",
      version: "2.0",
      scope: "profile email",
      accessTokenUrl: "https://accounts.google.com/o/oauth2/token",
      authorizationUrl: "https://accounts.google.com/o/oauth2/auth",
      profileUrl: "https://www.googleapis.com/oauth2/v3/userinfo",
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    },
    // Add other authentication providers here
  ],
};

export default nextAuthConfig;
