"use client";
import Link from "next/link";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import PasswordModal from "./modal/password";

export function Files() {
  const [data, setData] = useState({ name: [] });
  const [showPassword, setShowPassword] = useState(false);
  const [filename, setFilename] = useState("");
  const [passwordChecked, setPasswordChecked] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8080/api/data");

      const jsonData = await response.json();
      console.log(jsonData);
      setData(jsonData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const fileClick = (item) => {
    console.log("click");
    setFilename(item);
    setShowPassword(true);
    setPasswordChecked(false);
  };

  const handleRefresh = () => {
    console.log("refresh");
    fetchData();
  };

  return (
    <>
      <main className="flex-1 p-4 md:p-6">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {data.name.map((item, index) => (
            <Card className="relative group" key={index}>
              {/* <Link href="#" className="absolute inset-0 z-10" prefetch={false}>
                <span className="sr-only">Open file</span>
              </Link> */}
              <div className="flex items-center justify-center h-24 bg-muted rounded-t-lg">
                <FileIcon className="w-10 h-10 text-muted-foreground" />
              </div>
              <CardContent className="p-4">
                <h3 className="text-sm font-medium truncate">
                  Important Document.pdf
                </h3>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>PDF</span>
                  <span>12.3 MB</span>
                  <span>2 days ago</span>
                </div>
              </CardContent>
              <CardFooter className="flex items-center justify-end gap-2 p-2">
                <Button variant="ghost" size="icon">
                  <ShareIcon className="w-4 h-4" />
                  <span className="sr-only">Share</span>
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => fileClick(item)}
                >
                  <DownloadIcon className="w-4 h-4" />
                  <span className="sr-only" onClick={() => fileClick(item)}>
                    Download
                  </span>
                </Button>
              </CardFooter>
            </Card>
          ))}
          {showPassword && !passwordChecked && (
            <PasswordModal
              filename={filename}
              setPasswordChecked={setPasswordChecked}
            />
          )}
        </div>
      </main>
    </>
  );
}

function FileIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" />
      <path d="M14 2v4a2 2 0 0 0 2 2h4" />
    </svg>
  );
}

function ImageIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
      <circle cx="9" cy="9" r="2" />
      <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
    </svg>
  );
}

function DownloadIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" x2="12" y1="15" y2="3" />
    </svg>
  );
}

function ShareIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
      <polyline points="16 6 12 2 8 6" />
      <line x1="12" x2="12" y1="2" y2="15" />
    </svg>
  );
}

function FolderIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z" />
    </svg>
  );
}
