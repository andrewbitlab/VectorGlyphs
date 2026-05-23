import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import GlyphLabPage from "./page";

describe("GlyphLabPage", () => {
  it("renders a 50-glyph numbered feedback board for visual iteration", () => {
    render(<GlyphLabPage />);

    expect(screen.getByRole("heading", { level: 1, name: /Glyph review lab/i })).toBeInTheDocument();
    expect(screen.getByText(/Podaj mi numerki/i)).toBeInTheDocument();
    expect(screen.getAllByLabelText(/Review glyph/i)).toHaveLength(50);
    expect(screen.getByText("01")).toBeInTheDocument();
    expect(screen.getByText("50")).toBeInTheDocument();
    expect(screen.getAllByText(/broken outer rings/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText(/filled line systems/i).length).toBeGreaterThanOrEqual(1);
  });
});
