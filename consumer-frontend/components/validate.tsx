import { z } from "zod";

// Validierungsschema für das Formular
export const electricityFormSchema = z.object({
  updateDate: z
    .string()
    .refine((val) => val !== "", {
      message: "Datum ist erforderlich",
    })
    .refine((val) => new Date(val) <= new Date(), {
      message: "Das Datum kann nicht in der Zukunft liegen",
    }),
  meterReading: z
    .string()
    .regex(/^\d+$/, {
      message: "Nur Zahlen sind erlaubt",
    })
    .min(1, {
      message: "Zählerstand ist erforderlich",
    }),
  meterNumber: z
    .string()
    .regex(/^\d+$/, {
      message: "Nur Zahlen sind erlaubt",
    })
    .min(1, {
      message: "Zählernummer ist erforderlich",
    }),
});
