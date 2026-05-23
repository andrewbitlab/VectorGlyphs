import React from "react";
import Link from "next/link";

import { buildPreviewSpec, generatePreviewGlyphs, renderPreviewSvg } from "@/lib/glyphPreview";

const spec = buildPreviewSpec({
  seed: "vector-glyph-review-lab-v1",
  style: "premium-ui",
  complexity: "dense",
  count: 50,
  stroke: "#d8caa2",
  background: "transparent",
  format: "zip",
  pngSize: 2048,
});

export default function GlyphLabPage() {
  const glyphs = generatePreviewGlyphs(spec);

  return (
    <main className="min-h-screen bg-[#050506] px-6 py-10 text-[#f7f8f8]">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_18%_0%,rgba(113,112,255,0.20),transparent_30%),radial-gradient(circle_at_82%_12%,rgba(212,184,102,0.14),transparent_28%),linear-gradient(180deg,#08090a_0%,#010102_100%)]" />
      <section className="relative z-10 mx-auto max-w-7xl">
        <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <Link href="/" className="rounded-md border border-white/10 bg-white/[0.035] px-4 py-2 text-sm text-[#d0d6e0] hover:bg-white/[0.07]">
            ← Back to main page
          </Link>
          <p className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs uppercase tracking-[0.18em] text-[#8a8f98]">
            50 glyph review board
          </p>
        </div>

        <div className="mb-10 max-w-4xl">
          <p className="text-sm uppercase tracking-[0.2em] text-[#8a8f98]">Generator test lab</p>
          <h1 className="mt-3 text-5xl font-medium tracking-[-0.06em] md:text-7xl">Glyph review lab</h1>
          <p className="mt-5 text-lg leading-8 text-[#d0d6e0]">
            Podaj mi numerki glyphów, które Ci się nie podobają. Następna iteracja generatora będzie ulepszona o ten feedback.
          </p>
          <p className="mt-3 text-sm leading-6 text-[#8a8f98]">
            Ta plansza miesza nowe broken outer rings, filled line systems, symetryczne rdzenie, orbitujące punkty i warianty geometryczne — każdy glyph ma być wyraźny, estetyczny i gotowy do dalszej selekcji.
          </p>
        </div>

        <div className="mb-8 grid gap-3 md:grid-cols-3">
          <div className="rounded-2xl border border-white/[0.08] bg-white/[0.025] p-5">
            <h2 className="text-lg font-medium">broken outer rings</h2>
            <p className="mt-2 text-sm text-[#8a8f98]">Przerywane główne okręgi, ale zawsze z czytelną zawartością wewnątrz.</p>
          </div>
          <div className="rounded-2xl border border-white/[0.08] bg-white/[0.025] p-5">
            <h2 className="text-lg font-medium">filled line systems</h2>
            <p className="mt-2 text-sm text-[#8a8f98]">Wypełnienia kreskami, rytmami i kapsułami bez przypadkowego chaosu.</p>
          </div>
          <div className="rounded-2xl border border-white/[0.08] bg-white/[0.025] p-5">
            <h2 className="text-lg font-medium">feedback loop</h2>
            <p className="mt-2 text-sm text-[#8a8f98]">Wyślij np. “nie podobają mi się 04, 17, 31” i dopracujemy reguły.</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
          {glyphs.map((glyph, index) => (
            <article
              key={glyph.id}
              aria-label={`Review glyph ${index + 1}`}
              className="rounded-3xl border border-white/[0.08] bg-white/[0.025] p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.035)] transition hover:-translate-y-1 hover:border-[#7170ff]/50 hover:bg-white/[0.045]"
            >
              <div className="flex items-center justify-between gap-2">
                <span className="font-mono text-sm text-[#d8caa2]">{String(index + 1).padStart(2, "0")}</span>
                <span className="truncate rounded-full border border-white/[0.08] px-2 py-1 text-[10px] text-[#8a8f98]">
                  {glyph.tags.includes("segmented-ring") ? "broken" : glyph.tags.includes("filled-lines") ? "filled" : "core"}
                </span>
              </div>
              <div className="mt-4 grid aspect-square place-items-center rounded-3xl border border-white/[0.07] bg-[radial-gradient(circle_at_50%_20%,rgba(255,255,255,0.08),transparent_36%),#0d1210]">
                <div
                  className="size-28 text-[#d8caa2]"
                  dangerouslySetInnerHTML={{ __html: renderPreviewSvg(glyph, spec) }}
                />
              </div>
              <h2 className="mt-4 truncate text-sm font-medium text-white">{glyph.name}</h2>
              <p className="mt-1 truncate text-xs text-[#8a8f98]">{glyph.tags.join(" · ")}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
