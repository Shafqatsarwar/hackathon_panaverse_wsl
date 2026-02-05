"use client";

export default function CEOBriefingsPage() {
    return (
        <div className="space-y-6 animate-[fadeInUp_0.5s_ease-out]">
            <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-purple-900 to-indigo-900 p-8 shadow-2xl border border-white/10">
                <div className="relative z-10">
                    <h1 className="text-3xl font-bold text-white mb-2">Monday Morning CEO Briefing</h1>
                    <p className="text-indigo-200 max-w-2xl">Automated weekly reports on your business health, revenue, and bottlenecks.</p>
                    <button className="mt-6 px-6 py-3 bg-white text-purple-900 font-bold rounded-xl hover:bg-gray-100 transition-colors">
                        Generate New Briefing
                    </button>
                </div>
                <div className="absolute right-0 bottom-0 opacity-20 transform translate-x-1/4 translate-y-1/4">
                    <span className="text-9xl">📊</span>
                </div>
            </div>

            <h3 className="text-xl font-bold text-white mt-8 mb-4">Past Briefings</h3>
            <div className="grid gap-4">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="glass-panel p-6 rounded-2xl border border-white/10 flex items-center justify-between hover:bg-white/5 transition-colors cursor-pointer group">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center text-purple-400 group-hover:scale-110 transition-transform">
                                📄
                            </div>
                            <div>
                                <h4 className="font-bold text-white">Briefing: Week {4 - i} of Jan 2026</h4>
                                <p className="text-sm text-gray-400">Generated on Jan {30 - (i * 7)}, 2026</p>
                            </div>
                        </div>
                        <button className="text-sm text-blue-400 hover:underline">View Report</button>
                    </div>
                ))}
            </div>
        </div>
    );
}
