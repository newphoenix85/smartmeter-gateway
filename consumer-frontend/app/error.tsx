"use client";
import { subtitle, title } from "@/components/primitives";
import { useEffect } from "react";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    /* eslint-disable no-console */
    console.error(error);
  }, [error]);

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
    <div className="inline-block max-w-xl text-center justify-center">
      <span className={title({ color: "violet" })}>Error!&nbsp;</span>
      <br />
      
      <div className={subtitle({ class: "mt-4" })}>
        Somthing went wrong!
      </div>
    </div>
    
    <div>
      <button
        onClick={
          // Attempt to recover by trying to re-render the segment
          () => reset()
        }
      >
        Try again
      </button>
    </div>
  </section>
    
  );
}
