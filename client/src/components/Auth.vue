<template>
  <button @click="login">Login with Google</button>
</template>

<script>
import { createAuth } from "vue-google-oauth2";

export default {
  name: "AuthPage",
  methods: {
    login() {
      const auth = createAuth({
        clientId: process.env.GOOGLE_CLIENT_ID,
        scope: "https://www.googleapis.com/auth/drive",
        prompt: "consent",
      });
      auth
        .signIn()
        .then((user) => {
          console.log("Logged in as", user);
          // Send user's access token to the backend for further interaction with Google Drive API
        })
        .catch((error) => {
          console.error("Authentication error:", error);
        });
    },
  },
};
</script>
