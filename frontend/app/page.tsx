'use client'

import { useState, useEffect, useRef } from 'react'
import { Message } from '@/types/message'
import { MessageList } from '@/components/MessageList'
import { MessageForm } from '@/components/MessageForm'
import styles from './page.module.css'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [username, setUsername] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const fetchMessages = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`${API_URL}/api/messages`)
      if (!response.ok) {
        throw new Error('Failed to fetch messages')
      }
      const data = await response.json()
      setMessages(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      console.error('Error fetching messages:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMessages()
    // Poll for new messages every 3 seconds
    const interval = setInterval(fetchMessages, 3000)
    return () => clearInterval(interval)
  }, [])

  const handleSend = async (content: string) => {
    if (!username.trim()) {
      setError('Please enter your username first')
      return
    }
    if (!content.trim()) {
      return
    }

    try {
      const response = await fetch(`${API_URL}/api/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username.trim(), content: content.trim() }),
      })
      if (!response.ok) {
        throw new Error('Failed to send message')
      }
      await fetchMessages()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message')
      console.error('Error sending message:', err)
    }
  }

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>Chat MVP</h1>
        <p className={styles.description}>
          A simple chat application demonstrating end-to-end flow
        </p>

        {error && (
          <div className={styles.error}>
            Error: {error}
            <button onClick={() => setError(null)} className={styles.errorClose}>×</button>
          </div>
        )}

        <div className={styles.usernameSection}>
          <label htmlFor="username" className={styles.usernameLabel}>
            Your Username:
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username..."
            className={styles.usernameInput}
            maxLength={50}
          />
        </div>

        {loading && messages.length === 0 ? (
          <div className={styles.loading}>Loading messages...</div>
        ) : (
          <MessageList messages={messages} />
        )}

        <div ref={messagesEndRef} />

        <MessageForm onSend={handleSend} disabled={!username.trim()} />
      </div>
    </main>
  )
}
