import React, { useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
} from "@nextui-org/react";
import { Input } from "@/components/ui/input";

export default function DeleteModal({ filename, isOpen, onClose }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    const data = {
      filename: filename,
    };

    try {
      const response = await fetch(
        "https://ciphervault-4l9d.onrender.com/api/delete_file",
        {
          // const response = await fetch("http://127.0.0.1:8080/api/delete_file", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      );

      onClose();

      if (!response.ok) {
        throw new Error("File deletion failed");
      }

      console.log("File deleted successfully");
      setFile(null);
      onClose();
      window.location.reload();
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <Modal isOpen={isOpen} onOpenChange={onClose} placement="top-center">
      <ModalContent>
        <form onSubmit={handleFormSubmit}>
          <ModalHeader className="flex flex-col gap-1 cursor-default">
            Are you sure you want to delete this file?
          </ModalHeader>
          {/* <ModalBody>
            <Input
              type="file"
              onChange={handleFileChange}
              label="File"
              accept="*"
            />
          </ModalBody> */}
          <ModalFooter>
            <Button color="danger" variant="flat" onPress={onClose}>
              Close
            </Button>
            <Button color="danger" type="submit">
              Delete
            </Button>
          </ModalFooter>
        </form>
      </ModalContent>
    </Modal>
  );
}
