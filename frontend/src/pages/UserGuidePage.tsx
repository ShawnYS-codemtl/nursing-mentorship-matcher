import React from "react";
import DashboardLayout from "../components/layout/DashboardLayout";
import type { Page } from "../App";

interface Props {
  onNavigate: (page: Page) => void;
}

interface SectionProps {
  step: number;
  title: string;
  children: React.ReactNode;
}

const Section: React.FC<SectionProps> = ({ step, title, children }) => (
  <section className="bg-white border border-gray-300 rounded-lg shadow-sm p-10">
    <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">
      Step {step < 10 ? `0${step}` : step}
    </p>
    <h2 className="text-lg font-semibold text-gray-900 mb-6">{title}</h2>
    <div className="space-y-5 text-sm text-gray-600 leading-7">
      {children}
    </div>
  </section>
);

const Callout: React.FC<{ type: "info" | "warning"; children: React.ReactNode }> = ({ type, children }) => {
  const styles =
    type === "warning"
      ? "border-l-amber-400 bg-amber-50 text-amber-800"
      : "border-l-blue-400 bg-blue-50 text-blue-800";
  return (
    <div className={`border-l-4 px-5 py-4 rounded-r-md text-sm leading-7 ${styles}`}>
      {children}
    </div>
  );
};

const Steps: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ol className="space-y-3">
    {React.Children.map(children, (child, i) => (
      <li className="flex items-start gap-3">
        <span className="flex-shrink-0 w-5 h-5 rounded-full bg-gray-100 text-gray-500 text-xs font-semibold flex items-center justify-center mt-1">
          {i + 1}
        </span>
        <span className="text-sm text-gray-600 leading-7">{child}</span>
      </li>
    ))}
  </ol>
);

const Step: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <>{children}</>
);

const UserGuidePage: React.FC<Props> = ({ onNavigate }) => {
  return (
    <DashboardLayout activePage="guide" onNavigate={onNavigate}>
      <div className="max-w-2xl space-y-6">

        {/* Page header */}
        <div className="mb-2">
          <h1 className="text-2xl font-bold text-gray-900 mb-1">User Guide</h1>
          <p className="text-sm text-gray-500">
            A walkthrough for admins running the McGill Nursing mentorship matching cycle.
          </p>
        </div>

        {/* Overview card */}
        <div className="bg-white border border-gray-300 rounded-lg shadow-sm p-10">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Overview</p>
          <h2 className="text-lg font-semibold text-gray-900 mb-6">How this tool works</h2>
          <p className="text-sm text-gray-600 leading-7">
            This tool takes mentor and mentee sign-up data exported from Google Forms and produces
            optimal pairings automatically. The workflow has three phases:{" "}
            <strong className="text-gray-800">import</strong> your CSVs,{" "}
            <strong className="text-gray-800">run</strong> the matching algorithm, then{" "}
            <strong className="text-gray-800">review</strong> and adjust the results before exporting.
            You can re-run matching as many times as needed — locked matches are always preserved.
          </p>
        </div>

        {/* Step 1 */}
        <Section step={1} title="Importing Data">
          <p>
            Download mentor and mentee responses from Google Sheets as separate CSV files
            (File → Download → CSV), then upload them using the{" "}
            <strong className="text-gray-800">Import</strong> section at the bottom of the Dashboard.
          </p>
          <Steps>
            <Step>Click <strong className="text-gray-800">Choose mentor CSV</strong> and select the mentors file.</Step>
            <Step>Click <strong className="text-gray-800">Choose mentee CSV</strong> and select the mentees file.</Step>
            <Step>Click <strong className="text-gray-800">Preview Import</strong>. The tool will auto-detect how your form columns map to the fields it needs.</Step>
          </Steps>
          <Callout type="info">
            If a participant submits the form more than once, only their most recent entry is kept.
            Deduplication is done by email address.
          </Callout>
        </Section>

        {/* Step 2 */}
        <Section step={2} title="Reviewing Column Mappings">
          <p>
            After previewing, a mapping table appears showing how each column in your CSV was matched
            to a field the algorithm uses (e.g. "What is your program?" → <em>program</em>).
          </p>
          <Steps>
            <Step>Check that each row looks correct. Most will be auto-detected accurately.</Step>
            <Step>
              If a column is mapped incorrectly, use the dropdown to select the right field. If a
              column is irrelevant, leave it unmapped.
            </Step>
            <Step>Click <strong className="text-gray-800">Confirm Import</strong> when the mappings look right. The data is now loaded into the database.</Step>
          </Steps>
          <Callout type="warning">
            Confirming the import does not overwrite existing matches — it only adds or updates
            participant records. You can safely re-import after a new registration deadline.
          </Callout>
        </Section>

        {/* Step 3 */}
        <Section step={3} title="Running the Algorithm">
          <p>
            Click <strong className="text-gray-800">Run Matching</strong> in the control panel. The algorithm runs in three phases:
          </p>
          <Steps>
            <Step><strong className="text-gray-800">Locked matches</strong> are pulled out first and kept as-is.</Step>
            <Step><strong className="text-gray-800">Explicit preferences</strong> are honoured next — mutual requests first, then one-sided.</Step>
            <Step>Remaining participants are matched to maximise total compatibility across all pairs simultaneously.</Step>
          </Steps>
          <p>
            The algorithm respects mentor capacity and two hard constraints: mentors must be at a
            higher year of study than their mentee, and must speak at least one language the mentee
            requires.
          </p>
        </Section>

        {/* Step 4 */}
        <Section step={4} title="Reading the Match Table">
          <p>
            Every match shows a <strong className="text-gray-800">score out of 100</strong> representing
            compatibility. Click any row to expand the breakdown:
          </p>
          <Steps>
            <Step><strong className="text-gray-800">Program alignment</strong> (up to 35 pts) — full points for the same program; partial for related programs (e.g. BSc(N) ↔ BNI).</Step>
            <Step><strong className="text-gray-800">Specialty alignment</strong> (up to 35 pts) — points for shared clinical interests; a small penalty if both have specialties with no overlap.</Step>
            <Step><strong className="text-gray-800">Identity &amp; extracurricular</strong> (up to 30 pts) — shared heritage languages, race/ethnicity, LGBTQ+ identity, and extracurricular interests.</Step>
          </Steps>
          <p>
            The <strong className="text-gray-800">Reasons</strong> section in the breakdown lists exactly
            which factors contributed to the score in plain language.
          </p>
        </Section>

        {/* Step 5 */}
        <Section step={5} title="Locking Matches">
          <p>
            Locking a match protects it from being overwritten the next time you run the algorithm.
            Use this for pairs you have manually confirmed or that involve special circumstances.
          </p>
          <Steps>
            <Step>Expand a match row and click the <strong className="text-gray-800">Lock</strong> button. An amber lock badge will appear on the row.</Step>
            <Step>To unlock, expand the row and click <strong className="text-gray-800">Unlock</strong>.</Step>
          </Steps>
          <Callout type="info">
            Lock matches before re-running the algorithm if you want to keep specific pairings. Any
            unlocked match may be reassigned on the next run.
          </Callout>
        </Section>

        {/* Step 6 */}
        <Section step={6} title="Manual Matching">
          <p>
            The <strong className="text-gray-800">Manual Matching</strong> panel lists mentees the algorithm
            could not place (e.g. no compatible mentor had remaining capacity). You can assign them
            by hand:
          </p>
          <Steps>
            <Step>Click the <strong className="text-gray-800">Selected Mentee</strong> card and pick a mentee from the list.</Step>
            <Step>Click the <strong className="text-gray-800">Selected Mentor</strong> card and pick an available mentor.</Step>
            <Step>
              A match score preview appears instantly. If the pair violates a hard constraint,
              a red warning shows the score they <em>would</em> have if eligible — you can still
              assign the pair if needed.
            </Step>
            <Step>Click <strong className="text-gray-800">Match Selected Pair</strong> to confirm.</Step>
          </Steps>
        </Section>

        {/* Step 7 */}
        <Section step={7} title="Exporting Results">
          <p>
            Click <strong className="text-gray-800">Export CSV</strong> to download all current matches as a
            spreadsheet. The file includes mentor and mentee names, emails, programs, match score,
            and the reason breakdown.
          </p>
          <p>
            You can export at any point and re-export after making adjustments.
          </p>
        </Section>

        {/* Step 8 */}
        <Section step={8} title="Resetting the Database">
          <Callout type="warning">
            <strong>Reset DB wipes all data permanently</strong> — all mentors, mentees, and matches
            are deleted. Only use this at the start of a new matching cycle when you want a clean
            slate. There is no undo.
          </Callout>
          <p>
            The button is in the control panel at the bottom of the Dashboard. A confirmation
            dialog will appear before anything is deleted.
          </p>
        </Section>

      </div>
    </DashboardLayout>
  );
};

export default UserGuidePage;
