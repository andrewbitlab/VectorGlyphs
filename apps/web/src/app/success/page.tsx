import React from "react";
import Link from "next/link";

export default function SuccessPage() {
  return (
    <main className="min-h-screen bg-canvas px-6 py-20 text-ink">
      <section className="mx-auto max-w-3xl rounded-[2rem] border border-ink/10 bg-panel/80 p-8 shadow-soft">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-accent">Secure fulfillment</p>
        <h1 className="mt-4 text-4xl font-semibold tracking-tight sm:text-5xl">Payment received</h1>
        <p className="mt-5 text-lg leading-8 text-muted">
          Your checkout redirect has returned successfully. VectorGlyphs still waits for the Stripe webhook before
          unlocking paid files, because a browser redirect never unlocks paid files on its own.
        </p>
        <div className="mt-8 rounded-3xl border border-ink/10 bg-canvas/70 p-5 text-sm leading-7 text-muted">
          <p>
            The backend treats Stripe webhook confirmation as the payment source of truth. Once the webhook marks the
            order as paid, the server creates a short-lived tokenized download link for the generated SVG/PNG ZIP.
          </p>
        </div>
        <Link
          href="/"
          className="mt-8 inline-flex rounded-full bg-ink px-5 py-3 text-sm font-semibold text-canvas transition hover:bg-accent"
        >
          Back to generator
        </Link>
      </section>
    </main>
  );
}
