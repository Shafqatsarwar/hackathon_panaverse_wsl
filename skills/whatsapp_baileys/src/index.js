/**
 * WhatsApp Baileys Microservice Entry Point
 * Runs as a separate service, Python calls via REST API
 * 
 * Usage:
 *   npm start
 *   
 * Then from Python:
 *   requests.post('http://localhost:3001/api/send', json={'to': '+123...', 'message': 'Hello'})
 */
import express from 'express';
import WhatsAppBaileys from './whatsapp.js';
import { createAPI } from './api.js';

const PORT = process.env.WHATSAPP_PORT || 3001;
const SESSION_DIR = process.env.SESSION_DIR || './sessions';

// Initialize Express
const app = express();
app.use(express.json());

// CORS for local development
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    if (req.method === 'OPTIONS') return res.sendStatus(200);
    next();
});

// Initialize WhatsApp
console.log('🚀 Starting WhatsApp Baileys Microservice...');
console.log(`📁 Session directory: ${SESSION_DIR}`);

const whatsapp = new WhatsAppBaileys(SESSION_DIR);

// Mount API routes
app.use('/api', createAPI(whatsapp));

// Root endpoint
app.get('/', (req, res) => {
    res.json({
        service: 'WhatsApp Baileys Microservice',
        version: '1.0.0',
        endpoints: {
            status: 'GET /api/status',
            qr: 'GET /api/qr',
            send: 'POST /api/send { to, message }',
            chats: 'GET /api/chats?limit=20',
            health: 'GET /api/health'
        }
    });
});

// Start server
app.listen(PORT, async () => {
    console.log(`\n🌐 API Server running on http://localhost:${PORT}`);
    console.log('📡 Endpoints:');
    console.log(`   GET  http://localhost:${PORT}/api/status`);
    console.log(`   GET  http://localhost:${PORT}/api/qr`);
    console.log(`   POST http://localhost:${PORT}/api/send`);
    console.log(`   GET  http://localhost:${PORT}/api/chats`);
    console.log('');

    // Connect to WhatsApp
    await whatsapp.connect();
});

// Graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n🛑 Shutting down...');
    await whatsapp.disconnect();
    process.exit(0);
});
