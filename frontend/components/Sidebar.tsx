"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function Sidebar() {
    const pathname = usePathname();

    const menuItems = [
        { name: "Dashboard", href: "/dashboard", icon: "🏠" },
        { name: "Invoices", href: "/dashboard/invoices", icon: "📄" },
        { name: "Payments", href: "/dashboard/payments", icon: "💰" },
        { name: "CEO Briefings", href: "/dashboard/briefings", icon: "🎯" },
        { name: "Social Media", href: "/dashboard/social", icon: "📱" },
    ];

    const quickActions = [
        { name: "Send Email", action: "email", icon: "📧" },
        { name: "WhatsApp", action: "whatsapp", icon: "💬" },
        { name: "This Week", action: "calendar", icon: "📅" },
    ];

    return (
        <aside className="w-64 glass-panel border-r border-white/10 h-screen flex flex-col p-6 fixed left-0 top-0 z-20">
            <div className="flex items-center gap-3 mb-10">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                    <span className="text-2xl">🤖</span>
                </div>
                <div>
                    <h1 className="font-bold text-lg text-white">AI Employee</h1>
                    <p className="text-xs text-gray-400">Sales & Business Intelligence</p>
                </div>
            </div>

            <nav className="space-y-2 mb-8">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 ml-2">Navigation</p>
                {menuItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${isActive
                                ? "bg-gradient-to-r from-blue-600/20 to-purple-600/20 text-white border border-blue-500/30"
                                : "text-gray-400 hover:text-white hover:bg-white/5"
                                }`}
                        >
                            <span>{item.icon}</span>
                            <span className="font-medium">{item.name}</span>
                            {isActive && (
                                <div className="ml-auto w-1 h-1 rounded-full bg-blue-400 shadow-[0_0_8px_currentColor]" />
                            )}
                        </Link>
                    );
                })}
            </nav>

            <div className="mt-auto space-y-2">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 ml-2">Quick Actions</p>
                {quickActions.map((action) => (
                    <button
                        key={action.name}
                        onClick={async () => {
                            if (action.action === 'email' || action.action === 'whatsapp') {
                                try {
                                    const channel = action.action === 'email' ? 'Email' : 'WhatsApp';
                                    alert(`Sending Summary Report via ${channel}... Please wait.`);
                                    const response = await fetch('http://localhost:8000/api/report/summary', { method: 'POST' });
                                    const data = await response.json();
                                    alert(data.status || "Command Sent!");
                                } catch (e) {
                                    alert("Error contacting backend: " + e);
                                }
                            } else {
                                alert(`Quick Action: ${action.name} (Coming Soon)`);
                            }
                        }}
                        className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 hover:border-white/10 transition-all text-gray-300 text-sm hover:scale-105 active:scale-95"
                    >
                        <span className="text-lg">{action.icon}</span>
                        {action.name}
                    </button>
                ))}
            </div>

            <div className="mt-4">
                <button
                    onClick={() => window.location.reload()}
                    className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-gradient-to-r from-red-500/10 to-pink-500/10 border border-red-500/20 hover:border-red-500/40 text-red-300 text-sm transition-all"
                >
                    <span>🔄</span> Refresh Dashboard
                </button>
            </div>
        </aside>
    );
}
