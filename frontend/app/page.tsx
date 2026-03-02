import Link from "next/link";
import { PageShell } from "../components/page-shell";

export default function HomePage() {
  return (
    <PageShell title="UniExplorer" description="Directory scaffold is ready for data wiring.">
      <Link href="/regions">Go to Regions</Link>
    </PageShell>
  );
}
