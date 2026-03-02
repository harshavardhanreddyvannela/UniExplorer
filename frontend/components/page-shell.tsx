import type { ReactNode } from "react";

type PageShellProps = {
  title: string;
  description: string;
  children?: ReactNode;
};

export function PageShell({ title, description, children }: PageShellProps) {
  return (
    <main>
      <h1>{title}</h1>
      <p>{description}</p>
      {children}
    </main>
  );
}
