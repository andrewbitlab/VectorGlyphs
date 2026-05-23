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
  type PreviewGlyph,
} from "@/lib/glyphPreview";
import { FAQ_ITEMS, HERO_COPY, IN_CONTEXT_SHOWCASES, RETENTION_FEATURES, USE_CASES } from "@/lib/landingContent";

const palettes = ["#9d9788", "#d4b866", "#828fff", "#10b981", "#f7f1df"];
const metrics = [
  ["12", "instant glyph candidates"],
  ["4K", "transparent PNG target"],
  ["No", "stock icon packs"],
];

export function LandingPage() {
  const [seed, setSeed] = useState("premium-interface-kit");
  const [style, setStyle] = useState("premium-ui");
  const [complexity, setComplexity] = useState("balanced");
  const [stroke, setStroke] = useState("#9d9788");
  const [background, setBackground] = useState<BackgroundMode>("transparent");
  const [pngSize, setPngSize] = useState(2048);
  const [format, setFormat] = useState<ExportFormat>("zip");
  const [generation, setGeneration] = useState(1);

  const spec = useMemo(
    () => buildPreviewSpec({ seed: `${seed}-${generation}`, style, complexity, stroke, background, pngSize, format, count: 12 }),
    [background, complexity, format, generation, pngSize, seed, stroke, style],
  );
  const glyphs = useMemo(() => generatePreviewGlyphs(spec), [spec]);
  const selectedGlyph = glyphs[0];
  const supportingGlyphs = glyphs.slice(1, 4);
  const selectedSvg = renderPreviewSvg(selectedGlyph, spec);

  return (
    <main className="min-h-screen overflow-hidden bg-[#050506] text-[#f7f8f8]">
      <div className="pointer-events-none fixed inset-0 z-0 bg-[radial-gradient(circle_at_18%_0%,rgba(113,112,255,0.24),transparent_32%),radial-gradient(circle_at_82%_12%,rgba(212,184,102,0.16),transparent_30%),radial-gradient(circle_at_50%_75%,rgba(16,185,129,0.10),transparent_30%),linear-gradient(180deg,#08090a_0%,#010102_100%)]" />
      <div className="pointer-events-none fixed inset-0 z-0 opacity-[0.18] [background-image:linear-gradient(rgba(255,255,255,0.08)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:72px_72px]" />

      <header className="sticky top-0 z-30 border-b border-white/[0.06] bg-[#08090a]/75 backdrop-blur-2xl">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <a href="#hero-generator" className="flex items-center gap-3 font-medium tracking-[-0.02em]">
            <span className="grid size-9 place-items-center rounded-full border border-white/10 bg-white/[0.04] text-glyph shadow-[inset_0_0_20px_rgba(255,255,255,0.04)]">◌</span>
            <span>VectorGlyphs</span>
          </a>
          <div className="hidden items-center gap-6 text-sm text-[#d0d6e0] md:flex">
            <a href="#studio" className="hover:text-white">Studio</a>
            <a href="#in-context" className="hover:text-white">In context</a>
            <a href="#exports" className="hover:text-white">Exports</a>
            <a href="#pricing" className="hover:text-white">Pricing</a>
            <a href="#feedback" className="rounded-md border border-white/10 bg-white/[0.035] px-3 py-2 hover:bg-white/[0.07]">Request a style</a>
          </div>
        </nav>
      </header>

      <section id="hero-generator" className="relative z-10 mx-auto grid max-w-7xl gap-10 px-6 pb-16 pt-14 lg:grid-cols-[0.88fr_1.12fr] lg:pb-24 lg:pt-24">
        <div className="flex flex-col justify-center">
          <div className="mb-5 flex w-fit items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-xs font-medium text-[#d0d6e0]">
            <span className="size-1.5 rounded-full bg-[#10b981] shadow-[0_0_18px_rgba(16,185,129,0.9)]" />
            Premium UX & Retention Layer
          </div>
          <h1 className="max-w-4xl text-5xl font-medium leading-[0.92] tracking-[-0.065em] text-[#f7f8f8] md:text-7xl lg:text-8xl">
            {HERO_COPY.title}
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-[#d0d6e0] md:text-xl">{HERO_COPY.description}</p>
          <p className="mt-4 text-sm text-[#8a8f98]">{HERO_COPY.microcopy}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a href="#generator-panel" className="rounded-md bg-brand px-5 py-3 text-sm font-medium text-white shadow-glow transition hover:bg-[#828fff]">
              Generate glyphs
            </a>
            <a href="#in-context" className="rounded-md border border-white/10 bg-white/[0.035] px-5 py-3 text-sm font-medium text-[#d0d6e0] transition hover:bg-white/[0.07]">
              See glyphs in UI
            </a>
          </div>
          <div className="mt-10 grid max-w-xl grid-cols-3 gap-3">
            {metrics.map(([value, label]) => (
              <div key={label} className="rounded-2xl border border-white/[0.07] bg-white/[0.025] p-4">
                <p className="text-2xl font-medium tracking-[-0.04em] text-white">{value}</p>
                <p className="mt-1 text-xs leading-5 text-[#8a8f98]">{label}</p>
              </div>
            ))}
          </div>
        </div>

        <div id="generator-panel" className="rounded-[32px] border border-white/10 bg-white/[0.045] p-3 shadow-[0_30px_120px_rgba(0,0,0,0.55)] backdrop-blur">
          <div className="overflow-hidden rounded-[26px] border border-white/10 bg-[#0b0c0f]">
            <div className="flex items-center justify-between border-b border-white/[0.07] px-5 py-4">
              <div>
                <p className="text-sm font-medium text-white">Live premium glyph studio</p>
                <p className="text-xs text-[#8a8f98]">Generate, compare, preview, then unlock payment-confirmed exports.</p>
              </div>
              <button
                type="button"
                onClick={() => setGeneration((value) => value + 1)}
                className="rounded-md bg-brand px-4 py-2 text-sm font-medium text-white transition hover:bg-[#828fff]"
              >
                Generate glyphs
              </button>
            </div>

            <div className="grid gap-0 lg:grid-cols-[1.05fr_0.95fr]">
              <div className="border-b border-white/[0.07] p-5 lg:border-b-0 lg:border-r">
                <div className="grid grid-cols-3 gap-3">
                  {glyphs.map((glyph, index) => (
                    <GlyphTile key={glyph.id} glyph={glyph} spec={spec} stroke={stroke} featured={index === 0} />
                  ))}
                </div>
                <div className="mt-4 flex items-center justify-between rounded-2xl border border-white/[0.07] bg-black/20 px-4 py-3 text-xs text-[#8a8f98]">
                  <span>Recently generated</span>
                  <span>{selectedGlyph.name}</span>
                </div>
              </div>

              <div className="space-y-4 p-5">
                <div className="relative overflow-hidden rounded-3xl border border-white/[0.08] bg-[radial-gradient(circle_at_50%_18%,rgba(113,112,255,0.18),transparent_34%),#050a08] p-7">
                  <div className="absolute inset-x-8 top-6 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />
                  <div className="mx-auto grid size-52 place-items-center rounded-full border border-white/[0.08] bg-white/[0.03] shadow-[inset_0_0_60px_rgba(255,255,255,0.04)]">
                    <div className="size-36 text-glyph" style={{ color: stroke }} dangerouslySetInnerHTML={{ __html: selectedSvg }} />
                  </div>
                  <p className="mt-5 text-center text-sm font-medium text-white">{selectedGlyph.name}</p>
                  <p className="mt-1 text-center text-xs text-[#8a8f98]">Copy-ready SVG · transparent PNG · ZIP pack</p>
                  <div className="mt-5 grid grid-cols-2 gap-2">
                    <div className="rounded-2xl border border-white/[0.07] bg-black/20 p-3">
                      <p className="text-[10px] uppercase tracking-[0.18em] text-[#8a8f98]">Onboarding</p>
                      <div className="mt-3 flex items-center gap-2">
                        <div className="grid size-9 place-items-center rounded-xl bg-white/[0.04]">
                          <div className="size-6" style={{ color: stroke }} dangerouslySetInnerHTML={{ __html: renderPreviewSvg(supportingGlyphs[0], spec) }} />
                        </div>
                        <span className="text-xs text-[#d0d6e0]">Step hero</span>
                      </div>
                    </div>
                    <div className="rounded-2xl border border-white/[0.07] bg-black/20 p-3">
                      <p className="text-[10px] uppercase tracking-[0.18em] text-[#8a8f98]">Dashboard</p>
                      <div className="mt-3 flex items-center gap-2">
                        <div className="grid size-9 place-items-center rounded-xl bg-white/[0.04]">
                          <div className="size-6" style={{ color: stroke }} dangerouslySetInnerHTML={{ __html: renderPreviewSvg(supportingGlyphs[1], spec) }} />
                        </div>
                        <span className="text-xs text-[#d0d6e0]">Metric card</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="grid gap-3 text-sm">
                  <label className="grid gap-1 text-[#d0d6e0]">
                    Seed
                    <input value={seed} onChange={(event) => setSeed(event.target.value)} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 text-white outline-none focus:border-[#7170ff]" />
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <SelectField label="Style" value={style} onChange={setStyle} options={STYLE_PRESETS} />
                    <SelectField label="Complexity" value={complexity} onChange={setComplexity} options={COMPLEXITY_PRESETS} />
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
                      <button key={color} type="button" onClick={() => setStroke(color)} className="size-7 rounded-full border border-white/20 shadow-[inset_0_0_10px_rgba(255,255,255,0.2)]" style={{ background: color }} aria-label={`Use ${color}`} />
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
          {glyphs.slice(0, 6).map((glyph, index) => (
            <div key={glyph.id} className="group rounded-3xl border border-white/[0.08] bg-white/[0.025] p-5 transition hover:-translate-y-1 hover:bg-white/[0.045]">
              <div className="mb-4 grid aspect-square place-items-center rounded-3xl border border-white/[0.07] bg-[radial-gradient(circle_at_50%_20%,rgba(255,255,255,0.08),transparent_34%),#101713]">
                <div className="size-28 transition group-hover:scale-105" style={{ color: palettes[index % palettes.length] }} dangerouslySetInnerHTML={{ __html: renderPreviewSvg(glyph, { ...spec, stroke: palettes[index % palettes.length] }) }} />
              </div>
              <h3 className="font-medium text-white">{glyph.name}</h3>
              <p className="mt-1 text-sm text-[#8a8f98]">Seeded, scalable, and clean enough for UI use.</p>
            </div>
          ))}
        </div>
      </section>

      <section id="studio" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <SectionHeader eyebrow="Premium UX & Retention Layer" title="Turn glyphs into interface moments users want to keep exploring." />
        <div className="grid gap-4 md:grid-cols-4">
          {RETENTION_FEATURES.map((feature, index) => (
            <InfoCard key={feature.title} eyebrow={`0${index + 1}`} title={feature.title} body={feature.body} />
          ))}
        </div>
      </section>

      <section id="in-context" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <SectionHeader eyebrow="Use glyphs, don’t just view them" title="See the same glyph language across product surfaces." />
        <div className="grid gap-5 lg:grid-cols-3">
          <OnboardingMockup glyph={selectedGlyph} svg={selectedSvg} stroke={stroke} title={IN_CONTEXT_SHOWCASES[0].title} body={IN_CONTEXT_SHOWCASES[0].body} />
          <DashboardMockup glyphs={supportingGlyphs} spec={spec} stroke={stroke} title={IN_CONTEXT_SHOWCASES[1].title} body={IN_CONTEXT_SHOWCASES[1].body} />
          <BrandTilesMockup glyphs={glyphs.slice(4, 8)} spec={spec} title={IN_CONTEXT_SHOWCASES[2].title} body={IN_CONTEXT_SHOWCASES[2].body} />
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
        <InfoCard title="Transparent PNG" body="Server-side PNG export at 512, 1024, 2048 and 4096 pixels for production UI assets." />
        <InfoCard title="ZIP packs" body="Paid packs include SVG, PNG sizes, manifest.json and license material in one download." />
      </section>

      <section id="license" className="relative z-10 mx-auto grid max-w-7xl gap-5 px-6 py-14 md:grid-cols-2">
        <div className="rounded-3xl border border-white/10 bg-white/[0.025] p-8">
          <h2 className="text-3xl font-medium tracking-[-0.04em]">Commercial license included</h2>
          <p className="mt-4 text-[#d0d6e0]">Every purchased glyph can be used in personal and commercial projects, including apps, websites, presentations, marketing assets, UI kits and digital products.</p>
        </div>
        <div className="rounded-3xl border border-white/10 bg-white/[0.025] p-8">
          <h2 className="text-3xl font-medium tracking-[-0.04em]">Payment-confirmed downloads</h2>
          <p className="mt-4 text-[#d0d6e0]">Browser redirects never unlock paid files. Stripe webhook confirmation creates the short-lived tokenized ZIP download.</p>
        </div>
      </section>

      <section id="how-it-works" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <SectionHeader eyebrow="How it works" title="A premium loop: generate, compare, imagine, export." />
        <div className="grid gap-4 md:grid-cols-4">
          {[
            ["01", "Generate", "Pick a seed or generate fresh glyph sets."],
            ["02", "Tune", "Adjust style, complexity, color and export settings."],
            ["03", "Preview", "See glyphs inside real UI contexts before committing."],
            ["04", "Export", "Unlock production files only after verified payment confirmation."],
          ].map(([step, title, body]) => <InfoCard key={step} eyebrow={step} title={title} body={body} />)}
        </div>
      </section>

      <section id="pricing" className="relative z-10 mx-auto max-w-7xl px-6 py-14">
        <div className="rounded-[32px] border border-white/10 bg-[radial-gradient(circle_at_10%_20%,rgba(113,112,255,0.20),transparent_26%),linear-gradient(135deg,rgba(255,255,255,0.07),rgba(255,255,255,0.02))] p-8 md:p-10">
          <p className="text-sm uppercase tracking-[0.2em] text-[#8a8f98]">Pricing hypothesis</p>
          <h2 className="mt-3 max-w-4xl text-4xl font-medium tracking-[-0.05em] md:text-5xl">Preview for free. Download production-ready icon assets for $1.</h2>
          <p className="mt-4 max-w-3xl text-[#d0d6e0]">Phase 4 now uses a safe local/test-mode payment flow: pending orders, signed webhooks, idempotent fulfillment and tokenized downloads.</p>
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
            <h2 className="mt-3 text-3xl font-medium tracking-[-0.04em]">Request the next premium glyph style pack.</h2>
            <p className="mt-4 text-[#d0d6e0]">Tell us what visual language would make VectorGlyphs more useful for your product.</p>
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

function GlyphTile({ glyph, spec, stroke, featured }: { glyph: PreviewGlyph; spec: ReturnType<typeof buildPreviewSpec>; stroke: string; featured: boolean }) {
  return (
    <button
      type="button"
      className={`group rounded-2xl border p-3 transition hover:border-[#7170ff]/60 hover:bg-white/[0.055] ${featured ? "border-[#7170ff]/50 bg-[#7170ff]/10" : "border-white/[0.08] bg-white/[0.025]"}`}
      aria-label={`Preview ${glyph.name}`}
    >
      <div className="mx-auto size-20 text-glyph transition group-hover:scale-105" style={{ color: stroke }} dangerouslySetInnerHTML={{ __html: renderPreviewSvg(glyph, spec) }} />
      <p className="mt-2 truncate text-center text-[10px] text-[#8a8f98]">{glyph.name}</p>
    </button>
  );
}

function SelectField({ label, value, onChange, options }: { label: string; value: string; onChange: (value: string) => void; options: readonly { value: string; label: string }[] }) {
  return (
    <label className="grid gap-1 text-[#d0d6e0]">
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)} className="rounded-md border border-white/10 bg-black/30 px-3 py-2 text-white outline-none focus:border-[#7170ff]">
        {options.map((preset) => <option key={preset.value} value={preset.value}>{preset.label}</option>)}
      </select>
    </label>
  );
}

function SectionHeader({ eyebrow, title }: { eyebrow: string; title: string }) {
  return (
    <div className="mb-8 max-w-4xl">
      <p className="text-sm uppercase tracking-[0.2em] text-[#8a8f98]">{eyebrow}</p>
      <h2 className="mt-3 text-3xl font-medium tracking-[-0.05em] text-white md:text-5xl">{title}</h2>
    </div>
  );
}

function InfoCard({ eyebrow, title, body }: { eyebrow?: string; title: string; body: string }) {
  return (
    <div className="rounded-2xl border border-white/[0.08] bg-white/[0.025] p-6 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
      {eyebrow ? <p className="mb-4 font-mono text-xs text-[#7170ff]">{eyebrow}</p> : null}
      <h3 className="text-xl font-medium tracking-[-0.02em] text-white">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-[#8a8f98]">{body}</p>
    </div>
  );
}

function OnboardingMockup({ glyph, svg, stroke, title, body }: { glyph: PreviewGlyph; svg: string; stroke: string; title: string; body: string }) {
  return (
    <article className="rounded-[28px] border border-white/[0.08] bg-[#0f1011] p-5">
      <div className="rounded-3xl border border-white/[0.08] bg-[linear-gradient(160deg,rgba(113,112,255,0.18),rgba(255,255,255,0.02))] p-5">
        <div className="grid size-24 place-items-center rounded-3xl border border-white/10 bg-black/20">
          <div className="size-16" style={{ color: stroke }} dangerouslySetInnerHTML={{ __html: svg }} />
        </div>
        <h3 className="mt-8 text-2xl font-medium tracking-[-0.04em] text-white">{title}</h3>
        <p className="mt-3 text-sm leading-6 text-[#d0d6e0]">{body}</p>
        <p className="mt-5 rounded-full border border-white/10 bg-white/[0.04] px-3 py-2 text-xs text-[#8a8f98]">Featured glyph: {glyph.name}</p>
      </div>
    </article>
  );
}

function DashboardMockup({ glyphs, spec, stroke, title, body }: { glyphs: PreviewGlyph[]; spec: ReturnType<typeof buildPreviewSpec>; stroke: string; title: string; body: string }) {
  return (
    <article className="rounded-[28px] border border-white/[0.08] bg-[#0f1011] p-5">
      <div className="grid gap-3">
        {glyphs.map((glyph, index) => (
          <div key={glyph.id} className="flex items-center gap-3 rounded-2xl border border-white/[0.07] bg-white/[0.025] p-3">
            <div className="grid size-12 place-items-center rounded-xl bg-black/30">
              <div className="size-8" style={{ color: stroke }} dangerouslySetInnerHTML={{ __html: renderPreviewSvg(glyph, spec) }} />
            </div>
            <div>
              <p className="text-sm font-medium text-white">Signal layer {index + 1}</p>
              <p className="text-xs text-[#8a8f98]">{glyph.name}</p>
            </div>
          </div>
        ))}
      </div>
      <h3 className="mt-6 text-2xl font-medium tracking-[-0.04em] text-white">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-[#d0d6e0]">{body}</p>
    </article>
  );
}

function BrandTilesMockup({ glyphs, spec, title, body }: { glyphs: PreviewGlyph[]; spec: ReturnType<typeof buildPreviewSpec>; title: string; body: string }) {
  return (
    <article className="rounded-[28px] border border-white/[0.08] bg-[#0f1011] p-5">
      <div className="grid grid-cols-2 gap-3">
        {glyphs.map((glyph, index) => (
          <div key={glyph.id} className="grid aspect-square place-items-center rounded-3xl border border-white/[0.07] bg-white/[0.025]">
            <div className="size-16" style={{ color: palettes[index % palettes.length] }} dangerouslySetInnerHTML={{ __html: renderPreviewSvg(glyph, { ...spec, stroke: palettes[index % palettes.length] }) }} />
          </div>
        ))}
      </div>
      <h3 className="mt-6 text-2xl font-medium tracking-[-0.04em] text-white">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-[#d0d6e0]">{body}</p>
    </article>
  );
}
