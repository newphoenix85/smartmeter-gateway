"use client"
import { addToast, Alert, Button, DatePicker, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, useDisclosure } from "@heroui/react";
import { ChangeEvent, useState } from "react";
import { getLocalTimeZone, today } from "@internationalized/date";
import { updateReadingDatas } from "@/app/actions";
import { Form } from "@heroui/form";
import { Zap } from "lucide-react";
import { z } from "zod";
import { ElectricityFormDatas } from "@/types/form";
import { electricityFormSchema } from "./validate";
import { ISmartlandSMGWRow } from "@/types";

// Importiere das Schema

export const SmartlandForm = ({ setNewValue, lastData }: { setNewValue: (el: boolean) => void , lastData: ISmartlandSMGWRow | undefined }) => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  const handleSubmit = async (formdatas: ElectricityFormDatas) => {
    console.log('handleSubmit')
    try {
      const parsedData = electricityFormSchema.safeParse(formdatas);
      
      if (!parsedData.success) {
        // Wenn die Validierung fehlschlägt, setze die Fehlernachrichten und breche ab
        const errors = parsedData.error.issues;
        addToast({
            title: "Error",
            description: `Fehler: ${errors}`,
            color: "danger",
            promise: new Promise((resolve) => setTimeout(resolve, 3000)),
          });
        return;
      }

      // Wenn es bereits einen letzten Zählerstand gibt
    if (lastData) {
        // Überprüfen, ob das neue Datum nach dem letzten Datum liegt
        const newDate = new Date(formdatas.updateDate);
        if (newDate <= lastData.ts) {
          addToast({
            title: "Error",
            description: `Das neue Datum muss nach dem letzten Zählerstand liegen.`,
            color: "danger",
            promise: new Promise((resolve) => setTimeout(resolve, 3000)),
          });
          return;
        }
  
        // Überprüfen, ob der neue Zählerstand größer als der letzte Wert ist
        const newMeterReading = parseFloat(formdatas.meterReading);
        if (newMeterReading <= lastData.value) {
          addToast({
            title: "Error",
            description: `Der neue Zählerstand muss größer als der letzte Wert sein.`,
            color: "danger",
            promise: new Promise((resolve) => setTimeout(resolve, 3000)),
          });
          return;
        }
      }

      // API-Call
      const [status, datas, result_message] = await updateReadingDatas(formdatas.updateDate, formdatas.meterReading, formdatas.meterNumber);

      if (status === 200) {
        setNewValue(true);
        addToast({
            title: "Success",
            description: `Zählerstand wurde erfolgreich übermittelt`,
            color: "success",
            promise: new Promise((resolve) => setTimeout(resolve, 3000)),
          });
      } else {
        addToast({
            title: "Error",
            description: `Fehler: ${result_message}`,
            color: "danger",
            promise: new Promise((resolve) => setTimeout(resolve, 3000)),
          });
      }
    } catch (error) {
      addToast({
        title: "Error",
        description: "Ein Fehler ist aufgetreten",
        color: "danger",
        promise: new Promise((resolve) => setTimeout(resolve, 3000)),
      });
      console.error(error);
    }
  };

  return (
    <>

        <Button
            className="w-full"
            color="success"
            startContent={<Zap />}
            variant="bordered"
            onPress={onOpen}
        >
            Neuen Zählerstand erfassen
        </Button>

      <Modal isOpen={isOpen} placement="top-center" onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="w-full flex flex-col gap-1">
                Zählerstand erfassen
              </ModalHeader>
              <Form
                className="w-full flex flex-col gap-4"
                validationBehavior="native"
                onSubmit={async (e) => {
                  e.preventDefault();
                  const formdatas = Object.fromEntries(new FormData(e.currentTarget));
                  await handleSubmit(formdatas as unknown as ElectricityFormDatas);
                  onClose(); // Optional: Modal schließen nach Submit
                }}
              >
                <ModalBody className="w-full">
                  <DatePicker
                    isRequired
                    label={"Datum"}
                    name="updateDate"
                    maxValue={today(getLocalTimeZone())}
                    size="md"
                    selectorButtonPlacement="start"
                    labelPlacement={"outside"}
                  />
                  <Input
                    isRequired
                    type="text"
                    label={"Zählerstand"}
                    name="meterReading"
                    size="md"
                    placeholder="Eingeben kWh"
                    labelPlacement={"outside"}
                  />
                  <Input
                    isRequired
                    type="text"
                    label={"Zählernummer"}
                    name="meterNumber"
                    placeholder="12345678"
                    size="md"
                    labelPlacement={"outside"}
                  />
                </ModalBody>
                <ModalFooter className="w-full flex justify-between">
                  <Button color="danger" variant="flat" onPress={onClose}>
                    Close
                  </Button>
                  <Button
                    color="primary"
                    type="submit"
                  >
                    Send
                  </Button>
                </ModalFooter>
              </Form>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
};
