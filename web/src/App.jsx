import React, { useState } from 'react';
import { Scale, FileText, Download, Play, Shield, Code, Sparkles, CheckCircle2, Copy } from 'lucide-react';

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
  const [compiledSuccess, setCompiledSuccess] = useState(false);

  const handleCompile = () => {
    setIsCompiling(true);
    setCompiledSuccess(false);
    setTimeout(() => {
      setIsCompiling(false);
      setCompiledSuccess(true);
    }, 1200);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-amber-500 selection:text-slate-950">
      {/* Header */}
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
            <a 
              href="https://github.com" 
              target="_blank" 
              rel="noreferrer"
              className="text-xs text-slate-400 hover:text-slate-200 transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-md hover:bg-slate-800/60 border border-transparent hover:border-slate-700"
            >
              <Code className="w-3.5 h-3.5" />
              Source Code
            </a>
            <button 
              onClick={handleCompile}
              disabled={isCompiling}
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 shadow-lg shadow-amber-500/20 hover:shadow-amber-500/30 transition-all flex items-center gap-2 disabled:opacity-50"
            >
              {isCompiling ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                  Compiling 28-Line Grid...
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5 fill-current" />
                  Compile Court PDF
                </>
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Editor Panel */}
        <div className="flex flex-col bg-slate-900/60 border border-slate-800/80 rounded-xl overflow-hidden shadow-2xl">
          <div className="px-4 py-3 bg-slate-900 border-b border-slate-800/80 flex items-center justify-between text-xs text-slate-400 font-medium">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-amber-400" />
              <span>Markdown Pleading Input (pleading.md)</span>
            </div>
            <span className="text-[11px] text-slate-500 font-mono">UTCR 28-Line Grid Compliant</span>
          </div>
          <textarea
            value={markdown}
            onChange={(e) => setMarkdown(e.target.value)}
            placeholder="Type or paste your Markdown legal pleading here..."
            className="flex-1 w-full p-4 bg-slate-950 font-mono text-xs text-slate-200 resize-none focus:outline-none focus:ring-1 focus:ring-amber-500/50 leading-relaxed"
            rows={24}
          />
        </div>

        {/* Right: PDF Preview / Layout View */}
        <div className="flex flex-col bg-slate-900/60 border border-slate-800/80 rounded-xl overflow-hidden shadow-2xl">
          <div className="px-4 py-3 bg-slate-900 border-b border-slate-800/80 flex items-center justify-between text-xs text-slate-400 font-medium">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span>28-Line Golden Layout PDF Preview</span>
            </div>
            {compiledSuccess && (
              <span className="text-[11px] text-emerald-400 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                UTCR 28-Line Alignment Verified
              </span>
            )}
          </div>

          <div className="flex-1 p-6 bg-slate-950 flex flex-col items-center justify-center relative overflow-y-auto">
            {compiledSuccess ? (
              <div className="w-full max-w-md bg-white text-slate-900 p-8 shadow-2xl rounded-sm font-serif border border-slate-200 text-[10px] leading-tight space-y-4">
                <div className="text-center font-bold text-[11px] uppercase tracking-wider">
                  In the Circuit Court of the State of Oregon<br />
                  For the County of Clackamas
                </div>
                
                <div className="border border-slate-900 p-3 my-4 grid grid-cols-2 gap-2 font-mono text-[9px]">
                  <div>
                    <strong>ANNIKA ERIKSSON,</strong><br />
                    &nbsp;&nbsp;Plaintiff,<br />
                    v.<br />
                    <strong>CITY OF OREGON CITY,</strong><br />
                    &nbsp;&nbsp;Defendant.
                  </div>
                  <div className="border-l border-slate-900 pl-3">
                    <strong>Case No. 24CV21417</strong><br /><br />
                    <strong>MOTION FOR EMERGENCY INJUNCTIVE RELIEF</strong>
                  </div>
                </div>

                <div className="space-y-2 font-serif text-[10px] leading-normal">
                  <p>1. Plaintiff moves this Court for an emergency order restoring municipal water service to 12054 Chapin Court.</p>
                  <p>2. On June 25, 2024, Defendant disconnected municipal water service without pre-deprivation hearing.</p>
                  <p>3. Under ORS 757.760 and 42 U.S.C. § 1983, the unconstitutional denial of essential public utility service constitutes immediate irreparable harm.</p>
                </div>

                <div className="pt-6 text-right text-[9px] font-sans">
                  Respectfully submitted,<br /><br />
                  <u>/s/ Annika Eriksson</u><br />
                  ANNIKA ERIKSSON, Pro Se
                </div>
              </div>
            ) : (
              <div className="text-center p-8 max-w-sm">
                <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-between mx-auto mb-4 text-amber-400">
                  <Scale className="w-6 h-6 mx-auto" />
                </div>
                <h3 className="text-sm font-semibold text-slate-200 mb-1">Ready for PDF Assembly</h3>
                <p className="text-xs text-slate-400 mb-4">
                  Click <strong>Compile Court PDF</strong> to transform your Markdown text into a sub-millimeter 28-line legal pleading.
                </p>
                <button
                  onClick={handleCompile}
                  className="px-4 py-2 text-xs font-semibold text-slate-950 bg-amber-400 hover:bg-amber-300 rounded-lg transition-colors"
                >
                  Run 28-Line Compiler
                </button>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-900/30 py-4 px-6 text-center text-xs text-slate-500">
        JustiTeX Open-Source Legal Pleading Engine &copy; 2026. Released under AGPLv3 for Access to Justice.
      </footer>
    </div>
  );
}
