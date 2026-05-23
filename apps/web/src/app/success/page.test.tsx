import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import SuccessPage from "./page";

describe("success page", () => {
  it("explains that webhooks unlock downloads instead of trusting redirects", () => {
    render(<SuccessPage />);

    expect(screen.getByRole("heading", { name: /Payment received/i })).toBeInTheDocument();
    expect(screen.getAllByText(/Stripe webhook/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(/browser redirect never unlocks paid files/i)).toBeInTheDocument();
  });
});
