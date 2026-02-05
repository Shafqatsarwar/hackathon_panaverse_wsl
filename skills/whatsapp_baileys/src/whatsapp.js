/**
 * WhatsApp Baileys Core - Direct WebSocket connection (no browser!)
 * Much harder for WhatsApp to detect compared to Playwright/Puppeteer
 */
import makeWASocket, {
    DisconnectReason,
    useMultiFileAuthState,
    fetchLatestBaileysVersion,
    makeCacheableSignalKeyStore
} from '@whiskeysockets/baileys';
import pino from 'pino';
import qrcode from 'qrcode-terminal';
import QRCode from 'qrcode';
import fs from 'fs';
import path from 'path';

// Logger with minimal output
const logger = pino({ level: 'warn' });

class WhatsAppBaileys {
    constructor(sessionDir = './sessions') {
        this.sessionDir = sessionDir;
        this.socket = null;
        this.isConnected = false;
        this.qrCode = null;
        this.connectionCallbacks = [];

        // Ensure session directory exists
        if (!fs.existsSync(this.sessionDir)) {
            fs.mkdirSync(this.sessionDir, { recursive: true });
        }
    }

    /**
     * Initialize WhatsApp connection
     */
    async connect() {
        try {
            // Load saved session or create new
            const { state, saveCreds } = await useMultiFileAuthState(this.sessionDir);

            // Get latest Baileys version info
            const { version, isLatest } = await fetchLatestBaileysVersion();
            console.log(`🔌 Using Baileys v${version.join('.')} (latest: ${isLatest})`);

            // Create socket connection
            this.socket = makeWASocket({
                version,
                logger,
                printQRInTerminal: true, // Print QR to terminal for scanning
                auth: {
                    creds: state.creds,
                    keys: makeCacheableSignalKeyStore(state.keys, logger)
                },
                generateHighQualityLinkPreview: true,
                // Browser fingerprint - looks like WhatsApp Web
                browser: ['Panaverse Agent', 'Chrome', '120.0.0']
            });

            // Handle connection updates
            this.socket.ev.on('connection.update', async (update) => {
                const { connection, lastDisconnect, qr } = update;

                if (qr) {
                    // QR Code received - user needs to scan
                    this.qrCode = qr;
                    this.isConnected = false;

                    console.log('\n' + '='.repeat(60));
                    console.log('📱 SCAN THIS QR CODE WITH WHATSAPP MOBILE APP');
                    console.log('='.repeat(60) + '\n');

                    // Print to terminal
                    qrcode.generate(qr, { small: true });

                    // Save as image for remote access
                    try {
                        await QRCode.toFile(path.join(this.sessionDir, 'qr.png'), qr);
                        console.log(`\n📸 QR saved to: ${path.join(this.sessionDir, 'qr.png')}`);
                    } catch (e) {
                        console.error('QR save error:', e.message);
                    }
                }

                if (connection === 'close') {
                    const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;

                    console.log(`❌ Connection closed. Reason: ${lastDisconnect?.error?.message || 'unknown'}`);

                    if (shouldReconnect) {
                        console.log('🔄 Reconnecting in 5 seconds...');
                        setTimeout(() => this.connect(), 5000);
                    } else {
                        console.log('🚪 Logged out. Delete session folder and restart to re-login.');
                        this.isConnected = false;
                    }
                }

                if (connection === 'open') {
                    console.log('\n' + '='.repeat(60));
                    console.log('✅ WHATSAPP CONNECTED SUCCESSFULLY!');
                    console.log('='.repeat(60) + '\n');

                    this.isConnected = true;
                    this.qrCode = null;

                    // Notify callbacks
                    this.connectionCallbacks.forEach(cb => cb(true));
                }
            });

            // Save credentials when updated
            this.socket.ev.on('creds.update', saveCreds);

            // Handle incoming messages
            this.socket.ev.on('messages.upsert', async (msg) => {
                // Store for later retrieval via API
                if (msg.messages && msg.messages.length > 0) {
                    const message = msg.messages[0];
                    if (!message.key.fromMe && message.message) {
                        console.log(`📩 New message from: ${message.key.remoteJid}`);
                    }
                }
            });

            return true;
        } catch (error) {
            console.error('❌ Connection error:', error.message);
            return false;
        }
    }

    /**
     * Send a text message
     * @param {string} jid - WhatsApp JID (phone@s.whatsapp.net or group@g.us)
     * @param {string} text - Message text
     */
    async sendMessage(jid, text) {
        if (!this.isConnected || !this.socket) {
            return { success: false, error: 'Not connected to WhatsApp' };
        }

        try {
            // Format JID if needed
            const formattedJid = this.formatJid(jid);

            // Send message
            const result = await this.socket.sendMessage(formattedJid, { text });

            console.log(`✉️ Message sent to ${formattedJid}`);
            return {
                success: true,
                messageId: result.key.id,
                timestamp: result.messageTimestamp
            };
        } catch (error) {
            console.error('❌ Send error:', error.message);
            return { success: false, error: error.message };
        }
    }

    /**
     * Get recent chats/messages
     */
    async getChats(limit = 20) {
        if (!this.isConnected || !this.socket) {
            return { success: false, error: 'Not connected', chats: [] };
        }

        try {
            // Baileys stores chat data - we can access it
            const chats = await this.socket.groupFetchAllParticipating();
            const chatList = Object.entries(chats).slice(0, limit).map(([jid, data]) => ({
                jid,
                name: data.subject || jid,
                isGroup: jid.endsWith('@g.us')
            }));

            return { success: true, chats: chatList };
        } catch (error) {
            return { success: false, error: error.message, chats: [] };
        }
    }

    /**
     * Format phone number to JID
     */
    formatJid(input) {
        // Already formatted
        if (input.includes('@')) return input;

        // Clean phone number
        const cleaned = input.replace(/[^\d]/g, '');

        // Add WhatsApp suffix
        return `${cleaned}@s.whatsapp.net`;
    }

    /**
     * Get connection status
     */
    getStatus() {
        return {
            connected: this.isConnected,
            hasQR: !!this.qrCode,
            qrCode: this.qrCode
        };
    }

    /**
     * Disconnect
     */
    async disconnect() {
        if (this.socket) {
            await this.socket.logout();
            this.socket = null;
            this.isConnected = false;
        }
    }
}

export default WhatsAppBaileys;
