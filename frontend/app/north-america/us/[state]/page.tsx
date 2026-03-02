import { PageShell } from "../../../../components/page-shell";
import { humanizeSlug } from "../../../../lib/format";

type Props = {
  params: Promise<{ state: string }>;
};

export default async function NorthAmericaUsStatePage({ params }: Props) {
  const { state } = await params;
  const stateLabel = humanizeSlug(state);

  return (
    <PageShell
      title={`US: ${stateLabel}`}
      description="University listing for this US state will be populated from backend data."
    />
  );
}
