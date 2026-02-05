"use client";

export default function PaymentsPage() {
    return (
        <div className="space-y-6 animate-[fadeInUp_0.5s_ease-out]">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white">Payments</h1>
                    <p className="text-gray-400">Recent transactions and payouts</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="glass-panel p-6 rounded-2xl border border-white/10">
                    <p className="text-gray-400 text-sm uppercase font-bold">Total Balance</p>
                    <h2 className="text-4xl font-bold text-white mt-2">$24,500.00</h2>
                    <div className="mt-4 h-16 bg-blue-500/10 rounded-lg flex items-center justify-center text-blue-400 text-xs">Chart Area</div>
                </div>
                <div className="glass-panel p-6 rounded-2xl border border-white/10">
                    <p className="text-gray-400 text-sm uppercase font-bold">Incoming</p>
                    <h2 className="text-4xl font-bold text-green-400 mt-2">+$5,200</h2>
                    <p className="text-xs text-gray-500 mt-1">Last 30 days</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl border border-white/10">
                    <p className="text-gray-400 text-sm uppercase font-bold">Outgoing</p>
                    <h2 className="text-4xl font-bold text-red-400 mt-2">-$1,150</h2>
                    <p className="text-xs text-gray-500 mt-1">Last 30 days</p>
                </div>
            </div>

            <h3 className="text-xl font-bold text-white mt-8 mb-4">Recent Transactions</h3>
            <div className="glass-panel rounded-2xl p-6 border border-white/10 text-center text-gray-500">
                No recent transactions found.
            </div>
        </div>
    );
}
