"use client";
import React, { useEffect, useState } from "react";

const fetchUserInfo = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8080/api/user_info", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching user info:", error);
    throw error;
  }
};

const UserInfo = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUserInfo()
      .then((data) => setUserInfo(data))
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!userInfo) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>User Info</h1>
      <pre>{JSON.stringify(userInfo, null, 2)}</pre>
    </div>
  );
};

export default UserInfo;
