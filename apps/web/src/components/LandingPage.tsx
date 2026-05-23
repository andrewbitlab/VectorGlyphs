"use client";

import React, { useMemo, useState } from "react";

import {
  COMPLEXITY_PRESETS,
  PNG_SIZES,
  STYLE_PRESETS,
  buildPreviewSpec,
  generatePreviewGlyphs,
  renderPreviewSvg,
  type BackgroundMode,
  type ExportFormat,
} from "@/lib/glyphPreview";
import { FAQ_ITEMS, HERO_COPY, USE_CASES } from "@/lib/landingContent";

const palettes = ["#9d9788", "#d4b866", "#828fff", "#10b981", "#f7f1df"];

export function LandingPage() {
  const [seed, setSeed] = useState("phase-2-demo");
  const [style, setStyle] = useState("premium-ui");
  const [complexity, setComplexity] = useState("balanced");
  const [stroke, setStroke] = useState("#9d9788");
  const [background, setBackground] = useState<BackgroundMode>("transparent");
  const [pngSize, setPngSize] = useState(2048);
  const [format, setFormat] = useState<ExportFormat>("svg");
  const [generation, setGeneration] = useState(1);

  const spec = useMemo(
    () => buildPreviewSpec({ seed: `${seed}-${generation}`, style, complexity, stroke, background, pngSize, format, count: 12 }),
    [background, complexity, format, generation, pngSize, seed, stroke, style],
  );
  const glyphs = useMemo(() => generatePreviewGlyphs(spec), [spec]);
  const selectedGlyph = glyphs[0];
  const selectedSvg = renderPreviewSvg(selectedGlyph, spec);

  return (
    <main className="min-h-screen overflow-hidden bg-canvas text-[#f7f8f8]">
      <div className="pointer-events-none fixed inset-0 -z-0 bg-[radial-gradient(circle_at_20%_0%,rgba(113,112,255,0.18),transparent_32%),radial-gradient(circle_at_78%_18%,rgba(212,184,102,0.13),transparent_28%),linear-gradient(180deg,#08090a_0%,#010102_100%)]" />
      <header className="sticky top-0 z-20 border-b border-white/5 bg-[#08090a]/80 backdrop-blur-xl">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <a href="#hero-generator" className="flex items-center gap-3 font-medium tracking-[-0.02em]">
            <span className="grid size-8 place-items-center rounded-full border border-white/10 bg-white/[0.03] text-glyph">◌</span>
            VectorGlyphs
          </a>
          <div className="hidden items-center gap-6 text-sm text-[#d0d6e0] md:flex">
            <a href="#examples" className="hover:text-white">Examples</a>
            <a href="#use-cases" className="hover:text-white">Use cases</a>
            <a href="#pricing" className="hover:text-white">Pricing</a>
            <a href="#feedback" className="rounded-md border border-white/10 bg-white/[0.03] px-3 py-2 hover:bg-white/[0.06]">Request a style</a>
          </div>
        </nav>
      </header>

      <section id="hero-generator" className="relative z-10 mx-auto grid max-w-7xl gap-10 px-6 pb-16 pt-14 lg:grid-cols-[0.92fr_1.08fr] lg:pb-24 lg:pt-24">
        <div className="flex flex-col justify-center">
          <div className="mb-5 w-fit rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-xs font-medium text-[#d0d6e0]">
            Procedural SVG marks for product teams
          </div>
          <h1 className="max-w-4xl text-5xl font-medium leading-[0.95] tracking-[-0.055em] text-[#f7f8f8] md:text-7xl">
            {HERO_COPY.title}
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-[#d0d6e0]">{HERO_COPY.description}</p>
          <p className="mt-4 text-sm text-[#8a8f98]">{HERO_COPY.microcopy}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a href="#generator-panel" className="rounded-md bg-brand px-5 py-3 text-sm font-medium text-white shadow-glow transition hover:bg-[#828fff]">
              Generate glyphs
            </a>
            <a href="#exports" className="rounded-md border border-white/10 bg-white/[0.03] px-5 py-3 text-sm font-medium text-[#d0d6e0] transition hover:bg-white/[0.06]">
              See export formats
            </a>
          </div>
        </div>

        <div id="generator-panel" className="rounded-[28px] border border-white/10 bg-white/[0.035] p-4 shadow-2xl backdrop-blur">
          <div className="rounded-[22px] border border-white/10 bg-[#0f1011] p-5">
            <div className="mb-4 flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-white">Live generator preview</p>
                <p className="text-xs text-[#8a8f98]">Client-side Phase 2 preview. Paid export backend comes later.</p>
              </div>
              <button
                type="button"
                onClick={() => setGeneration((value) => value + 1)}
                className="rounded-md bg-brand px-4 py-2 text-sm font-medium text-white transition hover:bg-[#828fff]"
              >
                Generate glyphs
              </button>
            </div>

            <div className="grid gap-5 lg:grid-cols-[1fr_0.92fr]">
              <div className="grid grid-cols-3 gap-3 rounded-2xl border border-white/10 bg-black/20 p-4">
                {glyphs.map((glyph) => (
                  <button
                    type="button"
                    key={glyph.id}
                    className="group rounded-2xl border border-white/10 bg-white/[0.025] p-3 transition hover:border-[#7170ff]/60 hover:bg-white/[0.05]"
                    aria-label={`Preview ${glyph.name}`}
                  >
                    <div
                      className="mx-auto size-20 text-glyph transition group-hover:scale-105"
                      style={{ color: stroke }}
                      dangerouslySetInnerHTML={{ __html: renderPreviewSvg(glyph, spec) }}
                    />
                    <p className="mt-2 truncate text-center text-[10px] text-[#8a8f98]">{glyph.name}</p>
                  </button>
                ))}
              </div>

              <div className="space-y-4 rounded-2xl border border-white/10 bg-white/[0.025] p-4">
                <div className="grid place-items-center rounded-2xl border border-white/10 bg-[#050a08] p-8">
                  <div className="size-44 text-glyph" style={{ color: stroke }} dangerouslySetInnerHTML={{ __html: selectedSvg }} />
                </div>

                <div className="grid gap-3 text-sm">
                  <label className="grid gap-1 text-[#d0d6e0]">
                    Seed
                    <input value={seed} onChange={(event) => setSeed(event.target.value)} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 text-white outline-none focus:border-[#7170ff]" />
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <label className="grid gap-1 text-[#d0d6e0]">
                      Style
                      <select value={style} onChange={(event) => setStyle(event.target.value)} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 text-white outline-none focus:border-[#7170ff]">
                        {STYLE_PRESETS.map((preset) => <option key={preset.value} value={preset.value}>{preset.label}</option>)}
                      </select>
                    </label>
                    <label className="grid gap-1 text-[#d0d6e0]">
                      Complexity
                      <select value={complexity} onChange={(event) => setComplexity(event.target.value)} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 text-white outline-none focus:border-[#7170ff]">
                        {COMPLEXITY_PRESETS.map((preset) => <option key={preset.value} value={preset.value}>{preset.label}</option>)}
                      </select>
                    </label>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <label className="grid gap-1 text-[#d0d6e0]">
                      Stroke color
                      <input value={stroke} onChange={(event) => setStroke(event.target.value)} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 font-mono text-white outline-none focus:border-[#7170ff]" />
                    </label>
                    <label className="grid gap-1 text-[#d0d6e0]">
                      PNG size
                      <select value={pngSize} onChange={(event) => setPngSize(Number(event.target.value))} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 text-white outline-none focus:border-[#7170ff]">
                        {PNG_SIZES.map((size) => <option key={size} value={size}>{size}px</option>)}
                      </select>
                    </label>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <label className="grid gap-1 text-[#d0d6e0]">
                      Background
                      <select value={background} onChange={(event) => setBackground(event.target.value as BackgroundMode)} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 text-white outline-none focus:border-[#7170ff]">
                        <option value="transparent">Transparent</option>
                        <option value="dark">Dark</option>
                        <option value="light">Light</option>
                      </select>
                    </label>
                    <label className="grid gap-1 text-[#d0d6e0]">
                      Format
                      <select value={format} onChange={(event) => setFormat(event.target.value as ExportFormat)} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 text-white outline-none focus:border-[#7170ff]">
                        <option value="svg">SVG</option>
                        <option value="png">PNG</option>
                        <option value="zip">ZIP pack</option>
                      </select>
                    </label>
                  </div>
                  <div className="flex flex-wrap gap-2 pt-1" aria-label="Quick palettes">
                    {palettes.map((color) => (
                      <button key={color} type="button" onClick={() => setStroke(color)} className="size-7 rounded-full border border-white/20" style={{ background: color }} aria-label={`Use ${color}`} />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="examples" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <SectionHeader eyebrow="Generated examples" title="A consistent circular glyph language for modern product surfaces." />
        <div className="grid gap-4 md:grid-cols-3">
          {glyphs.slice(0, 6).map((glyph) => (
            <div key={glyph.id} className="rounded-2xl border border-white/10 bg-white/[0.025] p-5">
              <div className="mb-4 grid aspect-square place-items-center rounded-2xl bg-[#101713]">
                <div className="size-28" style={{ color: stroke }} dangerouslySetInnerHTML={{ __html: renderPreviewSvg(glyph, spec) }} />
              </div>
              <h3 className="font-medium text-white">{glyph.name}</h3>
              <p className="mt-1 text-sm text-[#8a8f98]">Seeded, scalable, and clean enough for UI use.</p>
            </div>
          ))}
        </div>
      </section>

      <section id="use-cases" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <SectionHeader eyebrow="Use cases" title="Built for real product design jobs, not throwaway AI images." />
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          {USE_CASES.map((useCase) => <div key={useCase} className="rounded-xl border border-white/10 bg-white/[0.025] p-4 text-sm text-[#d0d6e0]">{useCase}</div>)}
        </div>
      </section>

      <section id="exports" className="relative z-10 mx-auto grid max-w-7xl gap-5 px-6 py-14 md:grid-cols-3">
        <InfoCard title="SVG export" body="Clean vector output with scalable geometry, currentColor styling and no scripts or external resources." />
        <InfoCard title="Transparent PNG" body="Planned server-side PNG export at 512, 1024, 2048 and 4096 pixels for production UI assets." />
        <InfoCard title="ZIP packs" body="Future paid packs will include SVG, PNG sizes, manifest.json and license.txt in one download." />
      </section>

      <section id="license" className="relative z-10 mx-auto grid max-w-7xl gap-5 px-6 py-14 md:grid-cols-2">
        <div className="rounded-3xl border border-white/10 bg-white/[0.025] p-8">
          <h2 className="text-3xl font-medium tracking-[-0.04em]">Commercial license included</h2>
          <p className="mt-4 text-[#d0d6e0]">Every purchased glyph can be used in personal and commercial projects, including apps, websites, presentations, marketing assets, UI kits and digital products.</p>
        </div>
        <div className="rounded-3xl border border-white/10 bg-white/[0.025] p-8">
          <h2 className="text-3xl font-medium tracking-[-0.04em]">Logo use with care</h2>
          <p className="mt-4 text-[#d0d6e0]">You may use purchased glyphs as brand elements, but VectorGlyphs does not guarantee trademark uniqueness or legal registrability.</p>
        </div>
      </section>

      <section id="how-it-works" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <SectionHeader eyebrow="How it works" title="Free previews now, paid production exports later." />
        <div className="grid gap-4 md:grid-cols-4">
          {[
            ["01", "Generate", "Pick a seed or generate fresh glyphs."],
            ["02", "Tune", "Adjust style, complexity, color and export settings."],
            ["03", "Preview", "Inspect a clean SVG preview in the browser."],
            ["04", "Export", "Stripe checkout will be enabled in Phase 4 after backend exports."],
          ].map(([step, title, body]) => <InfoCard key={step} eyebrow={step} title={title} body={body} />)}
        </div>
      </section>

      <section id="pricing" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <div className="rounded-[28px] border border-white/10 bg-gradient-to-br from-white/[0.06] to-white/[0.02] p-8 md:p-10">
          <p className="text-sm uppercase tracking-[0.2em] text-[#8a8f98]">Pricing hypothesis</p>
          <h2 className="mt-3 text-4xl font-medium tracking-[-0.05em]">Preview for free. Download production files for $1.</h2>
          <p className="mt-4 max-w-3xl text-[#d0d6e0]">Stripe checkout will be enabled in Phase 4. This Phase 2 MVP intentionally avoids payment and only demonstrates the purchase path.</p>
        </div>
      </section>

      <section id="faq" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <SectionHeader eyebrow="FAQ" title="Frequently asked questions" />
        <div className="grid gap-3 md:grid-cols-2">
          {FAQ_ITEMS.map((item) => (
            <details key={item.question} className="rounded-2xl border border-white/10 bg-white/[0.025] p-5">
              <summary className="cursor-pointer font-medium text-white">{item.question}</summary>
              <p className="mt-3 text-sm leading-6 text-[#8a8f98]">{item.answer}</p>
            </details>
          ))}
        </div>
      </section>

      <section id="feedback" className="relative z-10 mx-auto max-w-7xl px-6 py-14 pb-24">
        <div className="grid gap-6 rounded-[28px] border border-white/10 bg-white/[0.025] p-8 md:grid-cols-[0.8fr_1.2fr]">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-[#8a8f98]">Feedback stub</p>
            <h2 className="mt-3 text-3xl font-medium tracking-[-0.04em]">Request styles before the backend is live.</h2>
            <p className="mt-4 text-[#d0d6e0]">Telegram forwarding is planned but not configured in Phase 2.</p>
          </div>
          <form className="grid gap-3" onSubmit={(event) => event.preventDefault()}>
            <label className="grid gap-1 text-sm text-[#d0d6e0]">
              Use case
              <input placeholder="e.g. fintech dashboard cards" className="rounded-md border border-white/10 bg-black/30 px-3 py-3 text-white outline-none focus:border-[#7170ff]" />
            </label>
            <label className="grid gap-1 text-sm text-[#d0d6e0]">
              Feedback message
              <textarea rows={4} placeholder="Tell us which glyph styles would help your product." className="rounded-md border border-white/10 bg-black/30 px-3 py-3 text-white outline-none focus:border-[#7170ff]" />
            </label>
            <button type="submit" className="w-fit rounded-md border border-white/10 bg-white/[0.04] px-5 py-3 text-sm font-medium text-white">Save feedback draft</button>
          </form>
        </div>
      </section>
    </main>
  );
}

function SectionHeader({ eyebrow, title }: { eyebrow: string; title: string }) {
  return (
    <div className="mb-8 max-w-3xl">
      <p className="text-sm uppercase tracking-[0.2em] text-[#8a8f98]">{eyebrow}</p>
      <h2 className="mt-3 text-3xl font-medium tracking-[-0.04em] text-white md:text-5xl">{title}</h2>
    </div>
  );
}

function InfoCard({ eyebrow, title, body }: { eyebrow?: string; title: string; body: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.025] p-6">
      {eyebrow ? <p className="mb-4 font-mono text-xs text-[#7170ff]">{eyebrow}</p> : null}
      <h3 className="text-xl font-medium tracking-[-0.02em] text-white">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-[#8a8f98]">{body}</p>
    </div>
  );
}
