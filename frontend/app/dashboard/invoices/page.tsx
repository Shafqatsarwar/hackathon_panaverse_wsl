"use client";

export default function InvoicesPage() {
    const invoices = [
        { id: "INV-2026-001", client: "TechCorp Inc.", amount: "$5,000", status: "Paid", date: "Jan 25, 2026" },
        { id: "INV-2026-002", client: "EduLearn Systems", amount: "$2,500", status: "Pending", date: "Jan 28, 2026" },
        { id: "INV-2026-003", client: "Global Solutions", amount: "$12,000", status: "Overdue", date: "Jan 15, 2026" },
    ];

    return (
        <div className="space-y-6 animate-[fadeInUp_0.5s_ease-out]">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white">Invoices</h1>
                    <p className="text-gray-400">Manage and track your billing</p>
                </div>
                <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-xl text-white font-medium transition-colors">
                    + Create Invoice
                </button>
            </div>

            <div className="glass-panel rounded-2xl overflow-hidden border border-white/10">
                <table className="w-full text-left">
                    <thead className="bg-white/5 text-gray-400">
                        <tr>
                            <th className="p-4">Invoice ID</th>
                            <th className="p-4">Client</th>
                            <th className="p-4">Amount</th>
                            <th className="p-4">Date</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {invoices.map((inv) => (
                            <tr key={inv.id} className="hover:bg-white/5 transition-colors">
                                <td className="p-4 font-mono text-sm text-blue-300">{inv.id}</td>
                                <td className="p-4 font-medium text-white">{inv.client}</td>
                                <td className="p-4 text-gray-300">{inv.amount}</td>
                                <td className="p-4 text-gray-500 text-sm">{inv.date}</td>
                                <td className="p-4">
                                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${inv.status === 'Paid' ? 'bg-green-500/20 text-green-400' :
                                            inv.status === 'Pending' ? 'bg-yellow-500/20 text-yellow-400' :
                                                'bg-red-500/20 text-red-400'
                                        }`}>
                                        {inv.status}
                                    </span>
                                </td>
                                <td className="p-4">
                                    <button className="text-gray-400 hover:text-white transition-colors">...</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
