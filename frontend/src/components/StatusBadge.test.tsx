import { render, screen } from "@testing-library/react";
import { StatusBadge } from "./StatusBadge";

test("renders green styles for ONLINE status", () => {
    render(<StatusBadge status="ONLINE" />);
    const el = screen.getByText("ONLINE");
    expect(el).toHaveClass("bg-green-100");
});

test("renders red styles for OFFLINE status", () => {
    render(<StatusBadge status="OFFLINE"/>);
    const el = screen.getByText("OFFLINE");
    expect(el).toHaveClass("bg-red-100");
})

test("renders yellow styles for MAINTENANCE status", () => {
    render(<StatusBadge status="MAINTENANCE"/>);
    const el = screen.getByText("MAINTENANCE");
    expect(el).toHaveClass("bg-yellow-100");
})

test("renders yellow styles for DEGRADED status", () => {
    render(<StatusBadge status="DEGRADED"/>);
    const el = screen.getByText("DEGRADED");
    expect(el).toHaveClass("bg-yellow-100");
})