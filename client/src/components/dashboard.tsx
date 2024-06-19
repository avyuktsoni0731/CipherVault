"use client";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";

import { useState, useEffect } from "react";
import { signIn, signOut, useSession } from "next-auth/react";
import {
  User,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
} from "@nextui-org/react";

export function Dashboard() {
  const session = useSession();

  const [isSignedIn, setIsSignedIn] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [profilePicture, setProfilePicture] = useState("");
  const [userName, setUserName] = useState("");

  useEffect(() => {
    if (session.status === "unauthenticated") {
      setIsSignedIn(false);

      //   fetch("http://127.0.0.1:5000/api/login", {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify({
      //       sessionStatus: session.status,
      //     }),
      //   });
    }
    if (session.status === "authenticated") {
      setIsSignedIn(true);
      const profilePicture = session.data.user.image;
      const userName = session.data.user.name;
      const emailId = session.data.user.email;
      setProfilePicture(profilePicture);
      setUserName(userName);

      //   fetch("https://vitalwebapp.onrender.com/api/login", {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify({
      //       googleUserId: emailId,
      //       sessionStatus: session.status,
      //     }),
      //   });
    }
  }, [session.status]);

  const login = async () => {
    signIn("google");
  };
  const logout = async () => {
    signOut("google");
  };

  return (
    <div className="flex min-h-screen w-full">
      <div className="hidden border-r bg-muted/40 lg:block">
        <div className="flex h-[60px] items-center px-6">
          <Link
            href="#"
            className="flex items-center gap-2 font-semibold"
            prefetch={false}
          >
            <CloudIcon className="h-6 w-6" />
            <span>CryptoDrive</span>
          </Link>
        </div>
        <nav className="grid items-start px-4 text-sm font-medium">
          <Link
            href="#"
            className="flex items-center gap-3 rounded-lg px-3 py-2 text-primary transition-all hover:bg-accent hover:text-accent-foreground"
            prefetch={false}
          >
            <HomeIcon className="h-4 w-4" />
            My Files
          </Link>
          <Link
            href="#"
            className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:bg-accent hover:text-accent-foreground"
            prefetch={false}
          >
            <FolderIcon className="h-4 w-4" />
            Shared with me
          </Link>
          <Link
            href="#"
            className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:bg-accent hover:text-accent-foreground"
            prefetch={false}
          >
            <TrashIcon className="h-4 w-4" />
            Trash
          </Link>
        </nav>
      </div>
      <div className="flex flex-col w-full">
        <header className="flex h-14 lg:h-[60px] items-center gap-4 border-b bg-muted/40 px-6">
          <div className="flex-1">
            <h1 className="font-semibold text-lg">My Files</h1>
          </div>
          <div className="flex flex-1 items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
            <form className="ml-auto flex-1 sm:flex-initial">
              <div className="relative">
                <SearchIcon className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  type="search"
                  placeholder="Search files..."
                  className="pl-8 sm:w-[300px] md:w-[200px] lg:w-[300px]"
                />
              </div>
            </form>
            <Button variant="outline">
              <UploadIcon className="h-4 w-4 mr-2" />
              Upload
            </Button>
            <Button>
              <FolderPlusIcon className="h-4 w-4 mr-2" />
              New Folder
            </Button>
            {/* <Button onClick={() => login()}>
              Sign In
            </Button> */}
            {!isSignedIn && (
              <Button onClick={() => login()} color="primary">
                <UserIcon className="h-4 w-4 mr-2" />
                Sign In
              </Button>
            )}
            {isSignedIn && (
              <Dropdown placement="bottom-end">
                <DropdownTrigger>
                  <User
                    name={userName}
                    avatarProps={{
                      isBordered: true,
                      color: "secondary",
                      src: profilePicture,
                      size: "sm",
                    }}
                  />
                </DropdownTrigger>
                <DropdownMenu aria-label="Profile Actions" variant="flat">
                  <DropdownItem key="profile" className="h-14 gap-2">
                    <p className="font-semibold">Signed in as</p>
                    <p className="font-semibold">{userName}</p>
                  </DropdownItem>
                  {/* <DropdownItem href="/dashboard" key="dashboard">
                    Dashboard
                  </DropdownItem> */}
                  <DropdownItem
                    key="logout"
                    onClick={logout}
                    className="text-danger"
                  >
                    Log Out
                  </DropdownItem>
                </DropdownMenu>
              </Dropdown>
            )}
          </div>
        </header>
        <main className="flex-1 p-4 md:p-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            <Card className="relative group">
              <Link href="#" className="absolute inset-0 z-10" prefetch={false}>
                <span className="sr-only">Open file</span>
              </Link>
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
                <Button variant="ghost" size="icon">
                  <DownloadIcon className="w-4 h-4" />
                  <span className="sr-only">Download</span>
                </Button>
              </CardFooter>
            </Card>
            <Card className="relative group">
              <Link href="#" className="absolute inset-0 z-10" prefetch={false}>
                <span className="sr-only">Open file</span>
              </Link>
              <div className="flex items-center justify-center h-24 bg-muted rounded-t-lg">
                <FolderIcon className="w-10 h-10 text-muted-foreground" />
              </div>
              <CardContent className="p-4">
                <h3 className="text-sm font-medium truncate">Design Files</h3>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>Folder</span>
                  <span>45.6 MB</span>
                  <span>1 week ago</span>
                </div>
              </CardContent>
              <CardFooter className="flex items-center justify-end gap-2 p-2">
                <Button variant="ghost" size="icon">
                  <ShareIcon className="w-4 h-4" />
                  <span className="sr-only">Share</span>
                </Button>
                <Button variant="ghost" size="icon">
                  <DownloadIcon className="w-4 h-4" />
                  <span className="sr-only">Download</span>
                </Button>
              </CardFooter>
            </Card>
            <Card className="relative group">
              <Link href="#" className="absolute inset-0 z-10" prefetch={false}>
                <span className="sr-only">Open file</span>
              </Link>
              <div className="flex items-center justify-center h-24 bg-muted rounded-t-lg">
                <ImageIcon className="w-10 h-10 text-muted-foreground" />
              </div>
              <CardContent className="p-4">
                <h3 className="text-sm font-medium truncate">
                  Vacation Photos.zip
                </h3>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>ZIP</span>
                  <span>102 MB</span>
                  <span>3 weeks ago</span>
                </div>
              </CardContent>
              <CardFooter className="flex items-center justify-end gap-2 p-2">
                <Button variant="ghost" size="icon">
                  <ShareIcon className="w-4 h-4" />
                  <span className="sr-only">Share</span>
                </Button>
                <Button variant="ghost" size="icon">
                  <DownloadIcon className="w-4 h-4" />
                  <span className="sr-only">Download</span>
                </Button>
              </CardFooter>
            </Card>
            <Card className="relative group">
              <Link href="#" className="absolute inset-0 z-10" prefetch={false}>
                <span className="sr-only">Open file</span>
              </Link>
              <div className="flex items-center justify-center h-24 bg-muted rounded-t-lg">
                <FileIcon className="w-10 h-10 text-muted-foreground" />
              </div>
              <CardContent className="p-4">
                <h3 className="text-sm font-medium truncate">
                  Presentation.pptx
                </h3>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>PPTX</span>
                  <span>25.4 MB</span>
                  <span>1 month ago</span>
                </div>
              </CardContent>
              <CardFooter className="flex items-center justify-end gap-2 p-2">
                <Button variant="ghost" size="icon">
                  <ShareIcon className="w-4 h-4" />
                  <span className="sr-only">Share</span>
                </Button>
                <Button variant="ghost" size="icon">
                  <DownloadIcon className="w-4 h-4" />
                  <span className="sr-only">Download</span>
                </Button>
              </CardFooter>
            </Card>
            <Card className="relative group">
              <Link href="#" className="absolute inset-0 z-10" prefetch={false}>
                <span className="sr-only">Open file</span>
              </Link>
              <div className="flex items-center justify-center h-24 bg-muted rounded-t-lg">
                <FileIcon className="w-10 h-10 text-muted-foreground" />
              </div>
              <CardContent className="p-4">
                <h3 className="text-sm font-medium truncate">
                  Annual Report.docx
                </h3>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>DOCX</span>
                  <span>8.2 MB</span>
                  <span>2 months ago</span>
                </div>
              </CardContent>
              <CardFooter className="flex items-center justify-end gap-2 p-2">
                <Button variant="ghost" size="icon">
                  <ShareIcon className="w-4 h-4" />
                  <span className="sr-only">Share</span>
                </Button>
                <Button variant="ghost" size="icon">
                  <DownloadIcon className="w-4 h-4" />
                  <span className="sr-only">Download</span>
                </Button>
              </CardFooter>
            </Card>
            <Card className="relative group">
              <Link href="#" className="absolute inset-0 z-10" prefetch={false}>
                <span className="sr-only">Open file</span>
              </Link>
              <div className="flex items-center justify-center h-24 bg-muted rounded-t-lg">
                <FileIcon className="w-10 h-10 text-muted-foreground" />
              </div>
              <CardContent className="p-4">
                <h3 className="text-sm font-medium truncate">
                  Spreadsheet.xlsx
                </h3>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>XLSX</span>
                  <span>18.7 MB</span>
                  <span>3 months ago</span>
                </div>
              </CardContent>
              <CardFooter className="flex items-center justify-end gap-2 p-2">
                <Button variant="ghost" size="icon">
                  <ShareIcon className="w-4 h-4" />
                  <span className="sr-only">Share</span>
                </Button>
                <Button variant="ghost" size="icon">
                  <DownloadIcon className="w-4 h-4" />
                  <span className="sr-only">Download</span>
                </Button>
              </CardFooter>
            </Card>
          </div>
        </main>
      </div>
    </div>
  );
}

function CloudIcon(props) {
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
      <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z" />
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

function FolderPlusIcon(props) {
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
      <path d="M12 10v6" />
      <path d="M9 13h6" />
      <path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z" />
    </svg>
  );
}

function HomeIcon(props) {
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
      <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
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

function SearchIcon(props) {
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
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
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

function UploadIcon(props) {
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
      <polyline points="17 8 12 3 7 8" />
      <line x1="12" x2="12" y1="3" y2="15" />
    </svg>
  );
}

function UserIcon(props) {
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
      <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}
