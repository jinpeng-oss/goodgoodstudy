<template>  
  <div>  
    <div v-for="(m, idx) in messages" :key="idx" :style="{margin:'8px 0'}">  
      <div v-if="m.role === 'user'" style="text-align:right;">  
        <div style="display:inline-block;background:#e6f7ff;padding:8px;border-radius:6px;">{{ m.content }}</div>  
      </div>  
      <div v-else>  
        <div style="display:inline-block;background:#f5f5f5;padding:8px;border-radius:6px;">{{ m.content }}</div>  
      </div>  
    </div>  

    <textarea v-model="question" rows="3" style="width:100%;"></textarea>  
    <div style="margin-top:8px;">  
      <button @click="send" :disabled="loading">发送</button>  
      <span v-if="loading">等待回答...</span>  
    </div>  
  </div>  
</template>  

<script setup lang="ts">  
import { ref } from 'vue'  
import axios from 'axios'  

const question = ref('')  
const messages = ref<{role: string, content: string}[]>([])  
const loading = ref(false)  

async function send() {  
  if (!question.value.trim()) return  
  const q = question.value  
  messages.value.push({ role: 'user', content: q })  
  question.value = ''  
  loading.value = true  
  try {  
    const resp = await axios.post('/api/qa/', { question: q })  
    messages.value.push({ role: 'assistant', content: resp.data.answer })  
  } catch (err: any) {  
    messages.value.push({ role: 'assistant', content: '出错了：' + (err?.response?.data?.detail || err.message) })  
  } finally {  
    loading.value = false  
  }  
}  
</script>  
