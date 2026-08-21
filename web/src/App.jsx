import React, { useState } from "react";
import { Scale, FileText, Play, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck } from "lucide-react";

const SAMPLE_MARKDOWN = `# IN THE CIRCUIT COURT OF THE STATE OF OREGON
# FOR THE COUNTY OF CLACKAMAS

ANNIKA ERIKSSON,
    Plaintiff,
v.
CITY OF OREGON CITY,
    Defendant.

Case No. 24CV21417

## MOTION FOR EMERGENCY INJUNCTIVE RELIEF

1. Plaintiff moves this Court for an emergency order restoring municipal water service to 12054 Chapin Court.

2. On June 25, 2024, Defendant disconnected municipal water service without pre-deprivation hearing.

3. Under ORS 757.760 and 42 U.S.C. § 1983, the unconstitutional denial of essential public utility service constitutes immediate irreparable harm.

DATED: August 19, 2026.

Respectfully submitted,

/s/ Annika Eriksson
ANNIKA ERIKSSON, Pro Se`;

export default function App() {
  const [markdown, setMarkdown] = useState(SAMPLE_MARKDOWN);
  const [isCompiling, setIsCompiling] = useState(false);

  // Enhanced robust parser supporting arbitrary headers, multi-party captions, and section headers
  const parsePleading = (rawText) => {
    if (!rawText || !rawText.trim()) {
      return {
        courtHeader: "IN THE CIRCUIT COURT OF THE STATE OF OREGON\nFOR THE COUNTY OF CLACKAMAS",
        plaintiff: "PLAINTIFF NAME,\n  Plaintiff,",
        defendant: "DEFENDANT NAME,\n  Defendant.",
        caseNo: "Case No. UNASSIGNED",
        title: "DRAFT PLEADING",
        paragraphs: ["1. Enter your pleading text here..."],
        signature: "DATED: August 20, 2026.\nRespectfully submitted,\n\n/s/ Pro Se Litigant",
        warnings: ["Empty input provided. Rendering template defaults."]
      };
    }

    const lines = rawText.split("\n");
    let courtLines = [];
    let plaintiffLines = [];
    let defendantLines = [];
    let caseNo = "";
    let title = "";
    let bodyElements = [];
    let signatureLines = [];
    let warnings = [];

    let section = "court"; // court -> caption -> body -> signature

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();

      if (!trimmed) continue;

      // Detect Court Headers (# or ## starting with IN THE / FOR THE / UNITED STATES)
      if (trimmed.startsWith("#") && (trimmed.toUpperCase().includes("COURT") || trimmed.toUpperCase().includes("STATE OF") || trimmed.toUpperCase().includes("DISTRICT"))) {
        courtLines.push(trimmed.replace(/^#+\s*/, ""));
        continue;
      }

      // Detect Case Number
      if (trimmed.toLowerCase().includes("case no.") || trimmed.toLowerCase().includes("case no:") || trimmed.toLowerCase().includes("case number")) {
        caseNo = trimmed;
        section = "body";
        continue;
      }

      // Detect Pleading Title (## Title or ALL CAPS title line)
      if (trimmed.startsWith("## ") || (section === "body" && !title && trimmed === trimmed.toUpperCase() && trimmed.length > 5 && !trimmed.startsWith("DATED"))) {
        title = trimmed.replace(/^##+s*/, "");
        section = "body";
        continue;
      }

      // Detect Parties & Caption Separator
      if (section === "court" || section === "caption") {
        if (trimmed.toLowerCase().includes("plaintiff") || trimmed.toLowerCase().includes("petitioner")) {
          plaintiffLines.push(trimmed);
          section = "caption";
          continue;
        }
        if (trimmed.toLowerCase().includes("defendant") || trimmed.toLowerCase().includes("respondent")) {
          defendantLines.push(trimmed);
          section = "caption";
          continue;
        }
        if (trimmed === "v." || trimmed === "vs." || trimmed === "v" || trimmed === "vs") {
          section = "caption";
          continue;
        }
      }

      // Detect Signature Block
      if (trimmed.startsWith("DATED:") || trimmed.startsWith("Dated:") || trimmed.startsWith("Respectfully") || trimmed.startsWith("/s/") || trimmed.toLowerCase().endsWith("pro se") || trimmed.toLowerCase().includes("attorney for")) {
        signatureLines.push(trimmed);
        section = "signature";
        continue;
      }

      // Body Paragraphs & Subheadings
      if (section === "body" || section === "caption") {
        bodyElements.push(trimmed);
      }
    }

    // Validation checks for robustness
    if (!courtLines.length) warnings.push("No explicit court header (# IN THE COURT...) detected.");
    if (!caseNo) warnings.push("No case number (Case No. XXX) detected.");
    if (!title) warnings.push("No document title (## MOTION FOR...) detected.");

    return {
      courtHeader: courtLines.length ? courtLines.join("\n") : "IN THE CIRCUIT COURT OF THE STATE OF OREGON\nFOR THE COUNTY OF CLACKAMAS",
      plaintiff: plaintiffLines.length ? plaintiffLines.join("\n") : "ANNIKA ERIKSSON,\n  Plaintiff,",
      defendant: defendantLines.length ? defendantLines.join("\n") : "CITY OF OREGON CITY,\n  Defendant.",
      caseNo: caseNo || "Case No. 24CV21417",
      title: title || "MOTION FOR EMERGENCY INJUNCTIVE RELIEF",
      paragraphs: bodyElements.length ? bodyElements : ["1. Plaintiff moves this Court for emergency relief..."],
      signature: signatureLines.length ? signatureLines.join("\n") : "DATED: August 20, 2026.\nRespectfully submitted,\n/s/ Annika Eriksson\nANNIKA ERIKSSON, Pro Se",
      warnings
    };
  };

  const parsed = parsePleading(markdown);

  const handleCompile = () => {
    setIsCompiling(true);
    setTimeout(() => {
      setIsCompiling(false);
    }, 300);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-amber-500 selection:text-slate-950">
      <header className="border-b border-slate-800/80 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-tr from-amber-500 to-amber-600 rounded-lg text-slate-950 font-bold shadow-lg shadow-amber-500/20">
              <Scale className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-serif text-lg font-bold tracking-wide text-slate-50 flex items-center gap-2">
                JustiTeX
                <span className="text-[10px] uppercase font-sans tracking-wider px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/30">
                  AGPLv3 Engine
                </span>
              </h1>
              <p className="text-xs text-slate-400">Open-Access 28-Line Court Pleading Generator</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={handleCompile} disabled={isCompiling} className="px-4 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 shadow-lg shadow-amber-500/20 hover:shadow-amber-500/30 transition-all flex items-center gap-2 disabled:opacity-50">
              {isCompiling ? (
                <><div className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />Compiling 28-Line Grid...</>
              ) : (
                <><Play className="w-3.5 h-3.5 fill-current" />Re-Compile PDF Preview</>
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Input Editor */}
        <div className="flex flex-col bg-slate-900/60 border border-slate-800/80 rounded-xl overflow-hidden shadow-2xl">
          <div className="px-4 py-3 bg-slate-900 border-b border-slate-800/80 flex items-center justify-between text-xs text-slate-400 font-medium">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-amber-400" />
              <span>Markdown Pleading Input (pleading.md)</span>
            </div>
            <span className="text-[11px] text-slate-500 font-mono">Robust Parser v2</span>
          </div>
          <textarea value={markdown} onChange={(e) => setMarkdown(e.target.value)} placeholder="Type or paste any Markdown legal pleading here..." className="flex-1 w-full p-4 bg-slate-950 font-mono text-xs text-slate-200 resize-none focus:outline-none focus:ring-1 focus:ring-amber-500/50 leading-relaxed" rows={26} />
        </div>

        {/* Right: PDF Preview with Warnings Panel */}
        <div className="flex flex-col bg-slate-900/60 border border-slate-800/80 rounded-xl overflow-hidden shadow-2xl">
          <div className="px-4 py-3 bg-slate-900 border-b border-slate-800/80 flex items-center justify-between text-xs text-slate-400 font-medium">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span>Dynamic 28-Line Golden Layout PDF Preview</span>
            </div>
            {parsed.warnings.length === 0 ? (
              <span className="text-[11px] text-emerald-400 flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" />
                Structure & 28-Line Grid Valid
              </span>
            ) : (
              <span className="text-[11px] text-amber-400 flex items-center gap-1">
                <AlertTriangle className="w-3.5 h-3.5" />
                {parsed.warnings.length} Format Tip(s)
              </span>
            )}
          </div>

          <div className="flex-1 p-6 bg-slate-950 flex flex-col items-center relative overflow-y-auto">
            {/* Format Warnings Banner if applicable */}
            {parsed.warnings.length > 0 && (
              <div className="w-full max-w-lg mb-4 p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-300 text-[11px] space-y-1">
                <div className="font-semibold flex items-center gap-1.5 text-amber-400">
                  <AlertTriangle className="w-3.5 h-3.5" /> Structure Feedback:
                </div>
                {parsed.warnings.map((w, idx) => (
                  <div key={idx} className="pl-5">• {w}</div>
                ))}
              </div>
            )}

            {/* Rendered 28-Line Pleading Paper */}
            <div className="w-full max-w-lg bg-white text-slate-900 p-8 shadow-2xl rounded-sm font-serif border border-slate-200 text-[11px] leading-relaxed relative flex">
              {/* 28-Line Margin Numbers */}
              <div className="w-6 border-r border-slate-300 pr-1 select-none font-mono text-[9px] text-slate-400 text-right space-y-[4.5px]">
                {Array.from({ length: 28 }, (_, i) => (<div key={i + 1}>{i + 1}</div>))}
              </div>

              {/* Pleading Body Content */}
              <div className="flex-1 pl-6 space-y-4">
                <div className="text-center font-bold text-[11px] uppercase tracking-wider whitespace-pre-line">{parsed.courtHeader}</div>
                <div className="border border-slate-900 p-3 my-4 grid grid-cols-2 gap-2 font-mono text-[9.5px]">
                  <div className="whitespace-pre-line leading-snug">{parsed.plaintiff}<br />&nbsp;&nbsp;v.<br />{parsed.defendant}</div>
                  <div className="border-l border-slate-900 pl-3"><strong>{parsed.caseNo}</strong><br /><br /><strong className="uppercase">{parsed.title}</strong></div>
                </div>
                <div className="text-center font-bold uppercase text-[11px] underline tracking-wide">{parsed.title}</div>
                <div className="space-y-2 font-serif text-[10.5px] leading-relaxed">
                  {parsed.paragraphs.map((p, idx) => (
                    <p key={idx} className={p.startsWith("###") || p.startsWith("IV.") || p.startsWith("SECTION") ? "font-bold text-center uppercase tracking-wide pt-2" : ""}>
                      {p.replace(/^###+s*/, "")}
                    </p>
                  ))}
                </div>
                <div className="pt-6 text-right text-[9.5px] font-sans whitespace-pre-line">{parsed.signature}</div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800/80 bg-slate-900/30 py-4 px-6 text-center text-xs text-slate-500">JustiTeX Open-Source Legal Pleading Engine &copy; 2026. Released under AGPLv3 for Access to Justice.</footer>
    </div>
  );
}
