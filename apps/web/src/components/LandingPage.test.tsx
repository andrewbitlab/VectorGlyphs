import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { LandingPage } from "./LandingPage";

describe("LandingPage", () => {
  it("renders the Phase 2 MVP landing page with generator controls", () => {
    render(<LandingPage />);

    expect(screen.getByRole("heading", { level: 1, name: "Vector Glyph Generator" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /generate glyphs/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/seed/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/style/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/complexity/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/stroke color/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/PNG size/i)).toBeInTheDocument();
  });

  it("renders no-payment MVP sections, FAQ, and feedback stub", () => {
    render(<LandingPage />);

    expect(screen.getAllByText(/Preview for free/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText(/Stripe checkout will be enabled in Phase 4/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole("heading", { level: 2, name: /Commercial license/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 2, name: /Frequently asked questions/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/feedback message/i)).toBeInTheDocument();
  });
});
