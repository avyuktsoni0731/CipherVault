import React, { useEffect, useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Checkbox,
  Input,
  Link,
} from "@nextui-org/react";
import { LockIcon } from "./LockIcon.jsx";

export default function PasswordModal({
  filename,
  isOpen,
  onClose,
  setPasswordChecked,
}) {
  const [inputValue, setInputValue] = useState("");

  // useEffect(() => {
  //   console.log("Filename: ", filename);
  //   console.log("Enetered Password: ", inputValue);
  //   [inputValue, filename];
  // });

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    const data = {
      filename: filename,
      password: inputValue,
    };
    try {
      const response = await fetch("http://127.0.0.1:8080/check-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        throw new Error("Password verification failed");
      }
      setPasswordChecked(true);
      onClose();
      console.log("Password checked successfully");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  return (
    <>
      <Modal isOpen={isOpen} onOpenChange={onClose} placement="top-center">
        <ModalContent>
          <form onSubmit={handleFormSubmit}>
            <ModalHeader className="flex flex-col gap-1">
              Enter Your Key
            </ModalHeader>
            <ModalBody>
              <Input
                value={inputValue}
                onChange={handleInputChange}
                endContent={
                  <LockIcon className="text-2xl text-default-400 pointer-events-none flex-shrink-0" />
                }
                label="Key"
                placeholder="Enter your key"
                type="password"
                variant="bordered"
              />
            </ModalBody>
            <ModalFooter>
              <Button color="danger" variant="flat" onPress={onClose}>
                Close
              </Button>
              <Button color="primary" type="submit">
                Verify Key
              </Button>
            </ModalFooter>
          </form>
        </ModalContent>
      </Modal>
    </>
  );
}
