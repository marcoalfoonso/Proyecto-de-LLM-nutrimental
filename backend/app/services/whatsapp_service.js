const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

// ─── CONFIGURACIÓN ───────────────────────────────────────────────
const BACKEND_URL = 'http://127.0.0.1:8000';

// Tiempo de arranque — ignorar mensajes anteriores a este momento
const BOT_START_TIME = Date.now();

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        executablePath: 'C:\\Users\\A224765\\.cache\\puppeteer\\chrome\\win64-149.0.7827.54\\chrome-win64\\chrome.exe',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// ─── QR ──────────────────────────────────────────────────────────
client.on('qr', (qr) => {
    console.log('\n📱 Escanea este QR con WhatsApp:\n');
    qrcode.generate(qr, { small: true });
});

// ─── CONEXIÓN ────────────────────────────────────────────────────
client.on('ready', () => {
    console.log('\n✅ Bot conectado a WhatsApp\n');
    console.log('Esperando mensajes...\n');
});

// ─── MENSAJES ────────────────────────────────────────────────────
client.on('message', async (msg) => {
    if (msg.from === 'status@broadcast') return;
    if (msg.from.includes('@g.us')) return;
    if (!msg.body || msg.body.trim() === '') return;

    // Ignorar mensajes que llegaron antes de que el bot arrancara
    if (msg.timestamp * 1000 < BOT_START_TIME) return;

    console.log(`\n📩 Mensaje de ${msg.from}: ${msg.body}`);

    try {
        const response = await axios.post(`${BACKEND_URL}/chat`, {
            numero: msg.from,
            mensaje: msg.body
        }, { timeout: 120000 });

        const respuesta = response.data.respuesta;
        console.log(`✅ Respuesta: ${respuesta}`);
        await msg.reply(respuesta);

    } catch (error) {
        console.error('❌ Error:', error.message);
        await msg.reply('❌ Error al procesar tu mensaje. Intenta de nuevo.');
    }
});

// ─── INICIO ──────────────────────────────────────────────────────
console.log('🚀 Iniciando bot de alacena inteligente...');
console.log('⏳ Cargando WhatsApp Web...\n');
client.initialize();