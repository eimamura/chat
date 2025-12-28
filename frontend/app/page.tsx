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
  const [isSending, setIsSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const messagesContainerRef = useRef<HTMLDivElement>(null)
  const lastMessageIdRef = useRef<string | null>(null)
  const isInitialLoad = useRef(true)
  const userScrolledUp = useRef(false)
  const isUserScrolling = useRef(false)
  const messageFocusTrigger = useRef(0)

  const scrollToBottom = (instant = false) => {
    if (messagesContainerRef.current) {
      const container = messagesContainerRef.current
      if (instant) {
        container.scrollTop = container.scrollHeight
      } else {
        container.scrollTo({
          top: container.scrollHeight,
          behavior: 'smooth'
        })
      }
    } else if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ 
        behavior: instant ? 'auto' : 'smooth',
        block: 'end'
      })
    }
  }

  // Check if user is near bottom (within 150px)
  const isNearBottom = () => {
    if (!messagesContainerRef.current) return true
    const container = messagesContainerRef.current
    const threshold = 150
    const distanceFromBottom = container.scrollHeight - container.scrollTop - container.clientHeight
    return distanceFromBottom < threshold
  }

  // Scroll to bottom only on initial load
  useEffect(() => {
    if (messages.length > 0 && isInitialLoad.current) {
      // Instant scroll on initial load only
      setTimeout(() => {
        scrollToBottom(true)
        isInitialLoad.current = false
        userScrolledUp.current = false
      }, 100)
    }
  }, [messages.length === 0 ? null : messages]) // Only trigger on initial load

  const fetchMessages = async (silent = false) => {
    try {
      if (!silent) {
        setLoading(true)
      }
      setError(null)
      const response = await fetch(`${API_URL}/api/messages`)
      if (!response.ok) {
        throw new Error('Failed to fetch messages')
      }
      const data = await response.json()
      
      // Check if there are new messages
      const lastMessageId = data.length > 0 ? data[data.length - 1].id : null
      if (lastMessageId && lastMessageId !== lastMessageIdRef.current) {
        // New message received
        setMessages(data)
        lastMessageIdRef.current = lastMessageId
        
        // Only auto-scroll if user is near bottom (not scrolled up)
        if (isNearBottom() && !userScrolledUp.current) {
          setTimeout(() => scrollToBottom(), 100)
        }
      } else if (data.length > 0) {
        // Only update if messages changed (for silent updates)
        setMessages(data)
      }
    } catch (err) {
      if (!silent) {
        setError(err instanceof Error ? err.message : 'An error occurred')
      }
      console.error('Error fetching messages:', err)
    } finally {
      if (!silent) {
        setLoading(false)
      }
    }
  }

  useEffect(() => {
    fetchMessages()
    // Poll for new messages every 1 second for real-time feel
    const interval = setInterval(() => fetchMessages(true), 1000)
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

    setIsSending(true)
    userScrolledUp.current = false // Reset when user sends message
    const tempId = `temp-${Date.now()}`
    const optimisticMessage: Message = {
      id: tempId,
      username: username.trim(),
      content: content.trim(),
      created_at: new Date().toISOString(),
    }

    // Optimistic update: add message immediately
    setMessages((prev) => [...prev, optimisticMessage])
    
    // Always scroll when user sends a message
    setTimeout(() => scrollToBottom(true), 50)

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
      const newMessage = await response.json()
      
      // Replace optimistic message with real one
      setMessages((prev) => 
        prev.map((msg) => msg.id === tempId ? newMessage : msg)
      )
      lastMessageIdRef.current = newMessage.id
      
      // Scroll after message is confirmed
      setTimeout(() => scrollToBottom(), 100)
    } catch (err) {
      // Remove optimistic message on error
      setMessages((prev) => prev.filter((msg) => msg.id !== tempId))
      setError(err instanceof Error ? err.message : 'Failed to send message')
      console.error('Error sending message:', err)
    } finally {
      setIsSending(false)
    }
  }

  // Handle Enter key in username input to focus message field
  const handleUsernameKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && username.trim()) {
      e.preventDefault()
      // Trigger focus on message input
      messageFocusTrigger.current += 1
    }
  }

  // Track scroll position to determine if user scrolled up
  useEffect(() => {
    const container = messagesContainerRef.current
    if (!container) return

    let scrollTimeout: NodeJS.Timeout

    const handleScroll = () => {
      // Clear previous timeout
      clearTimeout(scrollTimeout)
      
      // Mark that user is scrolling
      isUserScrolling.current = true
      
      // Check if user scrolled up (away from bottom)
      if (!isNearBottom()) {
        userScrolledUp.current = true
      } else {
        // User scrolled back to bottom
        userScrolledUp.current = false
      }

      // Reset scrolling flag after scroll ends
      scrollTimeout = setTimeout(() => {
        isUserScrolling.current = false
      }, 150)
    }

    container.addEventListener('scroll', handleScroll, { passive: true })
    return () => {
      container.removeEventListener('scroll', handleScroll)
      clearTimeout(scrollTimeout)
    }
  }, [])

  return (
    <main className={styles.main}>
      <div className={styles.container}>
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
            onKeyDown={handleUsernameKeyDown}
            placeholder="Enter your username..."
            className={styles.usernameInput}
            maxLength={50}
          />
        </div>

        {loading && messages.length === 0 ? (
          <div className={styles.loading}>Loading messages...</div>
        ) : (
          <MessageList 
            messages={messages} 
            currentUsername={username}
            containerRef={messagesContainerRef}
          />
        )}

        <div ref={messagesEndRef} />

        <MessageForm 
          onSend={handleSend} 
          disabled={!username.trim() || isSending}
          focusTrigger={messageFocusTrigger.current}
        />
      </div>
    </main>
  )
}
