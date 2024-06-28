"use client";
import Link from "next/link";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import PasswordModal from "./modal/password";
import DeleteModal from "./modal/delete";

export function Files() {
  const [data, setData] = useState([]);
  const [showPassword, setShowPassword] = useState(false);
  const [filename, setFilename] = useState("");
  const [passwordChecked, setPasswordChecked] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

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

  const deleteFileClick = async (item) => {
    console.log("click");
    setFilename(item.name);
    setIsDeleteModalOpen(true);

    // await fetch("http://127.0.0.1:8080/api/delete_file", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({ filename: item.name }),
    // });
  };

  const downloadFileClick = (item) => {
    console.log("click");
    setFilename(item.name);
    setShowPassword(true);
    setPasswordChecked(false);
  };

  const formatFileSize = (bytes) => {
    if (bytes >= 1073741824) {
      return (bytes / 1073741824).toFixed(2) + " GB";
    } else if (bytes >= 1048576) {
      return (bytes / 1048576).toFixed(2) + " MB";
    } else if (bytes >= 1024) {
      return (bytes / 1024).toFixed(2) + " KB";
    } else if (bytes > 1) {
      return bytes + " bytes";
    } else if (bytes === 1) {
      return bytes + " byte";
    } else {
      return "0 bytes";
    }
  };

  const closeModal = () => {
    setShowPassword(false);
  };

  return (
    <>
      <main className="flex-1 p-4 md:p-6">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {data.map((item, index) => (
            <Card className="relative group" key={index}>
              <div className="flex items-center justify-center h-24 bg-muted rounded-t-lg">
                <FileIcon className="w-10 h-10 text-muted-foreground" />
              </div>
              <CardContent className="p-4">
                <h3 className="text-sm font-medium truncate">{item.name}</h3>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>
                    {item.size === "Unknown"
                      ? item.size
                      : formatFileSize(Number(item.size))}
                  </span>
                  <span>
                    {new Date(item.modifiedTime).toLocaleDateString()}
                  </span>
                </div>
              </CardContent>
              <CardFooter className="flex items-center justify-end gap-2 p-2">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => deleteFileClick(item)}
                >
                  <TrashIcon className="w-4 h-4" />
                  <span className="sr-only">Share</span>
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => downloadFileClick(item)}
                >
                  <DownloadIcon className="w-4 h-4" />
                  <span
                    className="sr-only"
                    onClick={() => downloadFileClick(item)}
                  >
                    Download
                  </span>
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </main>
      {showPassword && !passwordChecked && (
        <PasswordModal
          filename={filename}
          isOpen={showPassword}
          onClose={closeModal}
          setPasswordChecked={setPasswordChecked}
        />
      )}
      <DeleteModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
      />
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

function TrashIcon(props) {
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
      <path d="M3 6h18" />
      <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
      <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
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
