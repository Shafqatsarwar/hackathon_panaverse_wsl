"use client";

import { useState, useEffect } from "react";

export default function DashboardPage() {
    const [stats, setStats] = useState({
        whatsapp: 8,
        emails: 13,
        leads: 6,
        dealsClosed: 0,
        dealsLost: 0,
        activeTasks: 0,
        totalLeads: 6,
        hotLeads: 1,
        pipelineValue: "145K",
        avgScore: 68
    });

    const [time, setTime] = useState<string>("");
    const [isLoginOpen, setIsLoginOpen] = useState(false);
    const [user, setUser] = useState<any>(null);
    const [email, setEmail] = useState("khansarwar1@hotmail.com");
    const [password, setPassword] = useState("");

    useEffect(() => {
        setTime(new Date().toLocaleTimeString());
        const interval = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000 * 60);
        return () => clearInterval(interval);
    }, []);

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        // Check against hardcoded credentials from GUIDE.md/env
        if (email === "khansarwar1@hotmail.com" && password === "Admin@123") {
            setUser({ name: "Khan Sarwar", role: "Admin" });
            setIsLoginOpen(false);
        } else {
            alert("Invalid credentials! Please use the admin login provided in GUIDE.md");
        }
    };

    return (
        <div className="space-y-8 animate-[fadeInUp_0.5s_ease-out]">
            {/* Header Section */}
            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-gray-800 to-gray-900 border border-white/10 p-8 shadow-2xl">
                <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>

                {/* Login Modal */}
                {isLoginOpen && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
                        <div className="bg-gray-900 border border-white/10 rounded-3xl p-8 w-full max-w-md shadow-2xl">
                            <h2 className="text-2xl font-bold text-white mb-6">Admin Login</h2>
                            <form onSubmit={handleLogin} className="space-y-4">
                                <div>
                                    <label className="block text-sm text-gray-400 mb-1">Email</label>
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm text-gray-400 mb-1">Password</label>
                                    <input
                                        type="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        placeholder="Enter Admin@123"
                                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500"
                                    />
                                </div>
                                <div className="flex gap-3 pt-4">
                                    <button
                                        type="button"
                                        onClick={() => setIsLoginOpen(false)}
                                        className="flex-1 px-4 py-2 rounded-xl border border-white/10 hover:bg-white/5 text-gray-300"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        className="flex-1 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold"
                                    >
                                        Login
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}

                <div className="relative z-10 flex justify-between items-start">
                    <div>
                        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                            <span className="text-4xl">{user ? "👤" : "🎯"}</span>
                            {user ? `Welcome, ${user.name}` : "Sales Command Center"}
                        </h1>
                        <p className="text-gray-400 mt-2 text-lg">
                            {user ? "System Admin Access Granted - Full Control Enabled" : "Digital Sales FTE - Real-time Lead Management Dashboard"}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">Last updated: {time || "Loading..."} | Auto-refresh: 5 min</p>
                    </div>
                    <div className="flex gap-3">
                        {!user ? (
                            <>
                                <button
                                    onClick={() => setIsLoginOpen(true)}
                                    className="px-6 py-2 rounded-xl border border-white/10 hover:bg-white/5 transition-colors font-medium"
                                >
                                    Sign In
                                </button>
                                <button className="px-6 py-2 rounded-xl bg-white text-black hover:bg-gray-200 transition-colors font-bold">Sign Up</button>
                            </>
                        ) : (
                            <button
                                onClick={() => setUser(null)}
                                className="px-6 py-2 rounded-xl bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 transition-colors font-medium"
                            >
                                Sign Out
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Action Banner */}
            <div className="rounded-3xl bg-gradient-to-r from-gray-700 to-gray-600 border border-white/10 p-6 flex items-center justify-between shadow-lg">
                <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center">
                        <span className="text-2xl">👤+</span>
                    </div>
                    <div>
                        <h3 className="text-xl font-bold text-white">Qualify New Lead</h3>
                        <p className="text-gray-300">Start our 7-question assessment to qualify potential customers</p>
                    </div>
                </div>
                <button
                    onClick={() => alert("🚀 Launching Lead Qualification Wizard...\n\nThis will open the 7-step interactive form.")}
                    className="px-6 py-3 rounded-lg bg-white/10 hover:bg-white/20 hover:scale-105 active:scale-95 transition-all font-medium flex items-center gap-2"
                >
                    Start Now <span>›</span>
                </button>
            </div>

            {/* Top Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <StatCard
                    title="WhatsApp Messages"
                    value={stats.whatsapp}
                    subtitle="Sent this week"
                    icon="💬"
                    color="border-l-4 border-blue-500"
                    onClick={() => alert("Opening WhatsApp analytics...")}
                />
                <StatCard
                    title="Emails Sent"
                    value={stats.emails}
                    subtitle="Delivered"
                    icon="📧"
                    color="border-l-4 border-green-500"
                    onClick={() => alert("Opening Email campaign stats...")}
                />
                <StatCard
                    title="New Leads"
                    value={stats.leads}
                    subtitle="Added this week"
                    icon="📨"
                    color="border-l-4 border-purple-500"
                    onClick={() => alert("Filtering for New Leads...")}
                />
                <StatCard
                    title="Deals Closed"
                    value={stats.dealsClosed}
                    subtitle="Success"
                    icon="✅"
                    color="border-l-4 border-emerald-500"
                    onClick={() => alert("Showing Closed Won Deals...")}
                />
                <StatCard
                    title="Deal Lost"
                    value={stats.dealsLost}
                    subtitle="This week"
                    icon="❌"
                    color="border-l-4 border-red-500"
                    onClick={() => alert("Showing Lost Deals analysis...")}
                />
                <StatCard
                    title="Active Tasks"
                    value={stats.activeTasks}
                    subtitle="Pending"
                    icon="📋"
                    color="border-l-4 border-yellow-500"
                    onClick={() => alert("Opening Task Manager...")}
                />
            </div>

            {/* Main Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                    label="TOTAL LEADS"
                    value={stats.totalLeads}
                    trend="+6 this week"
                    icon="📊"
                    chartColor="bg-blue-500"
                    onClick={() => alert("Drilling down into Total Leads report...")}
                />
                <MetricCard
                    label="HOT LEADS"
                    value={stats.hotLeads}
                    trend="Requires immediate attention"
                    icon="🔥"
                    chartColor="bg-orange-500"
                    alert
                    onClick={() => alert("Filtering High Priority Leads...")}
                />
                <MetricCard
                    label="PIPELINE VALUE"
                    value={`$${stats.pipelineValue}`}
                    trend="Based on lead classifications"
                    icon="💰"
                    chartColor="bg-green-500"
                    onClick={() => alert("Opening Revenue Forecast...")}
                />
                <MetricCard
                    label="AVG SCORE"
                    value={`${stats.avgScore}%`}
                    trend="Good potential"
                    icon="🎯"
                    chartColor="bg-pink-500"
                    onClick={() => alert("Viewing Lead Scoring breakdown...")}
                />
            </div>

            {/* Bottom Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 glass-panel rounded-3xl p-6 border border-white/5">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="font-bold text-lg flex items-center gap-2">
                            <span>📊</span> Qualified Leads
                        </h3>
                        <button
                            onClick={() => {
                                alert("Syncing with Odoo...");
                                setStats(prev => ({ ...prev, leads: prev.leads, whatsapp: prev.whatsapp })); // Dummy state update to trigger render if needed
                            }}
                            className="px-4 py-1.5 rounded-lg bg-blue-500/20 text-blue-400 text-sm hover:bg-blue-500/30 hover:scale-105 active:scale-95 transition-all"
                        >
                            Refresh
                        </button>
                    </div>
                    <div className="h-64 flex items-center justify-center text-gray-500 border border-dashed border-white/10 rounded-xl bg-black/20">
                        <p>Chart Visualization Area</p>
                    </div>
                </div>

                <div className="glass-panel rounded-3xl p-6 border border-white/5 border-l-4 border-l-red-500">
                    <h3 className="font-bold text-lg flex items-center gap-2 mb-4 text-red-400">
                        <span>⚡</span> Urgent Actions
                    </h3>
                    <div className="space-y-4">
                        <div
                            onClick={() => alert("Action: Opening Client A Deal details...")}
                            className="bg-red-500/10 p-4 rounded-xl border border-red-500/20 cursor-pointer hover:bg-red-500/20 transition-all"
                        >
                            <p className="text-sm text-red-200 font-medium">Follow up with Client A</p>
                            <p className="text-xs text-red-300/60 mt-1">High priority deal ($50k)</p>
                        </div>
                        <div
                            onClick={() => alert("Action: Opening Proposal B Review...")}
                            className="bg-yellow-500/10 p-4 rounded-xl border border-yellow-500/20 cursor-pointer hover:bg-yellow-500/20 transition-all"
                        >
                            <p className="text-sm text-yellow-200 font-medium">Review Proposal B</p>
                            <p className="text-xs text-yellow-300/60 mt-1">Due in 2 hours</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ title, value, subtitle, icon, color, onClick }: any) {
    return (
        <div
            onClick={onClick}
            className={`bg-white text-gray-800 rounded-xl p-4 shadow-lg ${color} cursor-pointer transition-transform hover:scale-105 active:scale-95`}
        >
            <div className="flex justify-between items-start mb-2">
                <p className="text-xs font-bold uppercase text-gray-500 tracking-wide">{title}</p>
                <span className="text-lg opacity-80">{icon}</span>
            </div>
            <div className="flex flex-col">
                <span className="text-3xl font-bold text-gray-900">{value}</span>
                <span className="text-xs text-gray-500 mt-1">{subtitle}</span>
            </div>
        </div>
    );
}

function MetricCard({ label, value, trend, icon, chartColor, alert, onClick }: any) {
    return (
        <div
            onClick={onClick}
            className="glass-panel rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all group cursor-pointer hover:scale-105 active:scale-95"
        >
            <div className="flex justify-between items-start mb-4">
                <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">{label}</p>
                <span className="text-2xl group-hover:scale-110 transition-transform">{icon}</span>
            </div>
            <div className="mb-2">
                <h2 className="text-4xl font-bold text-white bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                    {value}
                </h2>
            </div>
            <div className={`text-sm ${alert ? 'text-red-400' : 'text-green-400/80'} flex items-center gap-1`}>
                <span>{alert ? '!' : '↗'}</span>
                {trend}
            </div>
        </div>
    );
}
