'use client';
import { subtitle, title } from "@/components/primitives";

export default function Home() {
  return (
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <div className="inline-block max-w-xl text-center justify-center">
          <span className={title({ color: "violet" })}>Welcome&nbsp;</span>
          <br />
          
          <div className={subtitle({ class: "mt-4" })}>
            Here is a place where you can upload your values to the producer.
          </div>
        </div>
      </section>
  );
}
