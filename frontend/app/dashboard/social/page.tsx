"use client";

export default function SocialMediaPage() {
    return (
        <div className="space-y-6 animate-[fadeInUp_0.5s_ease-out]">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white">Social Media Manager</h1>
                    <p className="text-gray-400">Auto-post content to LinkedIn, Twitter, and Facebook</p>
                </div>
                <button className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:opacity-90 rounded-xl text-white font-medium transition-opacity">
                    + Schedule Post
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* LinkedIn */}
                <div className="glass-panel p-6 rounded-2xl border-t-4 border-t-[#0077b5]">
                    <div className="flex justify-between items-start mb-4">
                        <span className="text-2xl">🔗</span>
                        <span className="px-2 py-1 rounded text-xs bg-green-500/20 text-green-400 font-bold">CONNECTED</span>
                    </div>
                    <h3 className="font-bold text-white text-lg">LinkedIn</h3>
                    <p className="text-sm text-gray-400 mt-1">Profile: User Name</p>
                    <div className="mt-4 flex gap-4 text-center">
                        <div><span className="block font-bold text-white">12</span><span className="text-xs text-gray-500">Posts</span></div>
                        <div><span className="block font-bold text-white">1.2k</span><span className="text-xs text-gray-500">Views</span></div>
                    </div>
                </div>

                {/* Twitter */}
                <div className="glass-panel p-6 rounded-2xl border-t-4 border-t-white">
                    <div className="flex justify-between items-start mb-4">
                        <span className="text-2xl">✖️</span>
                        <span className="px-2 py-1 rounded text-xs bg-red-500/20 text-red-400 font-bold">DISCONNECTED</span>
                    </div>
                    <h3 className="font-bold text-white text-lg">X (Twitter)</h3>
                    <p className="text-sm text-gray-400 mt-1">Not connected</p>
                    <button className="mt-4 w-full py-2 bg-white/10 hover:bg-white/20 rounded-lg text-sm text-white transition-colors">Connect Account</button>
                </div>

                {/* Facebook */}
                <div className="glass-panel p-6 rounded-2xl border-t-4 border-t-[#1877F2]">
                    <div className="flex justify-between items-start mb-4">
                        <span className="text-2xl">📘</span>
                        <span className="px-2 py-1 rounded text-xs bg-green-500/20 text-green-400 font-bold">CONNECTED</span>
                    </div>
                    <h3 className="font-bold text-white text-lg">Facebook</h3>
                    <p className="text-sm text-gray-400 mt-1">Page: Business Page</p>
                    <div className="mt-4 flex gap-4 text-center">
                        <div><span className="block font-bold text-white">5</span><span className="text-xs text-gray-500">Posts</span></div>
                        <div><span className="block font-bold text-white">340</span><span className="text-xs text-gray-500">Likes</span></div>
                    </div>
                </div>
            </div>
        </div>
    );
}
