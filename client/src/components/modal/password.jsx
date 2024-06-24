import React, { useEffect, useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
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
  //   const { isOpen, onOpen, onOpenChange } = useDisclosure();

  useEffect(() => {
    console.log("Filename: ", filename);
    console.log("Enetered Password: ", inputValue);
    [inputValue, filename];
  });

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    const data = {
      filename: filename,
      input: inputValue,
    };
    try {
      const response = await fetch("http://127.0.0.1:8080/send", {
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
      <Modal
        isOpen={isOpen}
        onOpenChange={onClose}
        placement="top-center"
        onSubmit={handleFormSubmit}
      >
        <ModalContent>
          {/* <form onSubmit={handleFormSubmit}> */}
          <ModalHeader className="flex flex-col gap-1">
            Enter Password
          </ModalHeader>
          <ModalBody>
            <Input
              value={inputValue}
              onChange={handleInputChange}
              endContent={
                <LockIcon className="text-2xl text-default-400 pointer-events-none flex-shrink-0" />
              }
              label="Password"
              placeholder="Enter your password"
              type="password"
              variant="bordered"
            />
            <div className="flex py-2 px-1 justify-between">
              <Checkbox
                classNames={{
                  label: "text-small",
                }}
              >
                Remember me
              </Checkbox>
              <Link color="primary" href="#" size="sm">
                Forgot password?
              </Link>
            </div>
          </ModalBody>
          <ModalFooter>
            <Button color="danger" variant="flat" onPress={onClose}>
              Close
            </Button>
            <Button color="primary" type="submit" onPress={onClose}>
              Sign in
            </Button>
          </ModalFooter>
          {/* </form> */}
        </ModalContent>
      </Modal>
    </>
  );
}
