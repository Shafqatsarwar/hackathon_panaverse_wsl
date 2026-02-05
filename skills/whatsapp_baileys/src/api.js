/**
 * REST API for WhatsApp Baileys
 * Your Python code will call these endpoints
 */
import express from 'express';

export function createAPI(whatsapp) {
    const router = express.Router();

    // Health check
    router.get('/health', (req, res) => {
        res.json({
            status: 'ok',
            service: 'whatsapp-baileys',
            timestamp: new Date().toISOString()
        });
    });

    // Get connection status
    router.get('/status', (req, res) => {
        const status = whatsapp.getStatus();
        res.json(status);
    });

    // Get QR code as base64 (for remote scanning)
    router.get('/qr', async (req, res) => {
        const status = whatsapp.getStatus();

        if (status.connected) {
            return res.json({ success: true, connected: true, qr: null });
        }

        if (!status.qrCode) {
            return res.json({ success: false, error: 'No QR code available yet. Wait a moment.' });
        }

        // Return QR as data
        res.json({
            success: true,
            connected: false,
            qr: status.qrCode
        });
    });

    // Send message
    router.post('/send', async (req, res) => {
        const { to, message } = req.body;

        if (!to || !message) {
            return res.status(400).json({
                success: false,
                error: 'Missing required fields: to, message'
            });
        }

        const result = await whatsapp.sendMessage(to, message);
        res.json(result);
    });

    // Get chats
    router.get('/chats', async (req, res) => {
        const limit = parseInt(req.query.limit) || 20;
        const result = await whatsapp.getChats(limit);
        res.json(result);
    });

    // Reconnect (if disconnected)
    router.post('/reconnect', async (req, res) => {
        await whatsapp.connect();
        res.json({ success: true, message: 'Reconnection initiated' });
    });

    return router;
}
