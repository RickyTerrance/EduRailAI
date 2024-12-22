<script setup lang="ts">
import { ref, watch, nextTick, onMounted } from 'vue';
import axios from 'axios';
import { marked } from 'marked';
import 'highlight.js/styles/github.css';

// Define interface for chat message
interface ChatMessage {
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

const isOpen = ref(false);
const message = ref('');
const chatHistory = ref<ChatMessage[]>([]);
const isLoading = ref(false);
const errorMessage = ref('');

const toggleChat = () => {
  isOpen.value = !isOpen.value;
};

const getCurrentTimestamp = () => {
  const now = new Date();
  return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
};

const resetChat = async () => {
  try {
    await axios.post('http://localhost:8000/api/reset_chat');
    chatHistory.value = [];
    errorMessage.value = '';
  } catch (error) {
    console.error('Reset chat error:', error);
    errorMessage.value = '重置對話時發生錯誤';
  }
};

const sendMessage = async () => {
  if (!message.value.trim()) return;

  const userMessage = message.value;
  const currentTimestamp = getCurrentTimestamp();

  // Add user message to chat history
  chatHistory.value.push({ 
    type: 'user', 
    content: userMessage, 
    timestamp: currentTimestamp 
  });

  // Reset input and set loading state
  message.value = '';
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await axios.post('http://localhost:8000/api/chat', { 
      message: userMessage 
    });

    chatHistory.value.push({
      type: 'assistant',
      content: response.data.response,
      timestamp: getCurrentTimestamp(),
    });
  } catch (error) {
    console.error('Chat error:', error);
    errorMessage.value = '無法連接AI服務，請檢查網路連線';
    chatHistory.value.push({
      type: 'assistant',
      content: errorMessage.value,
      timestamp: getCurrentTimestamp(),
    });
  } finally {
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
  }
};

const clearChatHistory = () => {
  chatHistory.value = [];
};

const scrollToBottom = () => {
  const chatMessages = document.querySelector('.chat-messages');
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
};

watch(chatHistory, scrollToBottom);

// Optional: Add keyboard shortcut to open/close chat
onMounted(() => {
  window.addEventListener('keydown', (e) => {
    // Ctrl + M to toggle chat
    if (e.ctrlKey && e.key === 'm') {
      e.preventDefault();
      toggleChat();
    }
  });
});
</script>

<template>
  <div class="chat-container" :class="{ open: isOpen }">
    <button class="chat-toggle" @click="toggleChat">
      <img src="../assets/EduRailLOGO.png" alt="Chat Icon" class="chat-icon" />
    </button>

    <Transition name="slide">
      <div v-if="isOpen" class="chat-window">
        <div class="chat-header">
          <span>EduRail AI</span>
          <button class="reset-btn" @click="resetChat">reset</button>
          <button class="clear-btn" @click="clearChatHistory">clear</button>
          <button class="close-btn" @click="toggleChat">&times;</button>
        </div>
        <div class="chat-messages">
          <div
            v-for="(msg, index) in chatHistory"
            :key="index"
            :class="['message', msg.type]"
          >
            <div v-html="marked(msg.content)"></div>
            <p class="timestamp">{{ msg.timestamp }}</p>
          </div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
          <div v-if="isLoading" class="loading-container">
            <div class="loading-spinner"></div>
            <p class="loading-text">處理中...</p>
          </div>
        </div>
        <div class="chat-input">
          <input
            v-model="message"
            @keyup.enter="sendMessage"
            placeholder="輸入訊息..."
            :disabled="isLoading"
          />
          <button @click="sendMessage" :disabled="isLoading">
            {{ isLoading ? '處理中...' : '送出' }}
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>


<style scoped>
.chat-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-toggle {
  width: 80px; /* 縮小按鈕尺寸 */
  height: 80px;
  border-radius: 50%;
  background-color: var(--primary-color);
  border: none;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-toggle:hover {
  transform: scale(1.1);
}

.chat-icon {
  width: 70px; /* 調整圖標大小 */
  height: 70px;
  object-fit: contain;
}

.chat-window {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 500px;
  height: 750px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  padding: 0.8rem;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.clear-btn {
  background: none;
  border: none;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.2rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #f8f9fa;
}

.timestamp {
  font-size: 0.75rem;
  color: #888;
  margin-bottom: 0.2rem;
}

.message {
  margin-bottom: 1rem;
  padding: 0.1rem 1rem;
  border-radius: 12px;
  max-width: 85%;
  word-wrap: break-word;
}

.message.user {
  background: rgb(86, 24, 105);
  color: white;
  margin-left: auto;;
}

.message.assistant {
  background-color: #ffffff;
  border: 1px solid #ddd;
  margin-right: auto;
}

.chat-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background-color: white;
  border-top: 1px solid #eee;
}

.chat-input input {
  flex: 1;
  padding: 0.5rem 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
}

.chat-input button {
  padding: 0.5rem 1rem; /* 縮小按鈕 */
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.chat-input button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
.error-message {
  color: red;
  text-align: center;
  padding: 10px;
  background-color: #ffeeee;
}

.reset-btn {
  background: none;
  border: none;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.2rem;
  margin-right: 10px;
}
/* 載入動畫的新樣式 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(227, 175, 79, 0.2);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

.loading-text {
  color: var(--primary-color);
  font-size: 0.9rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 與載入相關的狀態 */
.chat-input button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background-color: #ddd;
}

.chat-input input:disabled {
  background-color: #f4f4f4;
  cursor: not-allowed;
}
</style>