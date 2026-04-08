// firebase-setup.js
// Integração Firebase para análise e push notifications
// Configuração segura com variáveis de ambiente

import { initializeApp } from 'firebase/app';
import { getAnalytics, logEvent } from 'firebase/analytics';
import { getMessaging, getToken, onMessage } from 'firebase/messaging';

// Configuração Firebase (use variáveis de ambiente em produção)
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
};

// Inicializar Firebase
export const app = initializeApp(firebaseConfig);

// Analytics
export const analytics = getAnalytics(app);

// Evento de abertura do app
export const logAppOpen = () => {
  logEvent(analytics, 'app_open', {
    timestamp: new Date().toISOString(),
  });
};

// Push Notifications
export const initMessaging = async () => {
  try {
    const messaging = getMessaging(app);

    // Solicitar permissão para notificações
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      const token = await getToken(messaging, {
        vapidKey: process.env.REACT_APP_FIREBASE_VAPID_KEY,
      });
      console.log('FCM Token:', token);

      // Enviar token para seu servidor
      await fetch('/api/register-fcm-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token }),
      });
    }

    // Listener para mensagens recebidas
    onMessage(messaging, (payload) => {
      console.log('Mensagem recebida:', payload);
      // Mostrar notificação
      new Notification(payload.notification.title, {
        body: payload.notification.body,
        icon: '/icon-192x192.png',
      });
    });
  } catch (error) {
    console.error('Erro ao inicializar messaging:', error);
  }
};

// Rastreamento de eventos customizados
export const trackEvent = (eventName, params = {}) => {
  logEvent(analytics, eventName, {
    ...params,
    timestamp: new Date().toISOString(),
  });
};

// Exemplo de uso
export default {
  app,
  analytics,
  logAppOpen,
  initMessaging,
  trackEvent,
};
