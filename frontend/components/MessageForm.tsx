'use client'

import { useState } from 'react'
import styles from './MessageForm.module.css'

interface MessageFormProps {
  onSend: (content: string) => void
  disabled?: boolean
}

export function MessageForm({ onSend, disabled }: MessageFormProps) {
  const [content, setContent] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!content.trim() || disabled) {
      return
    }

    setIsSubmitting(true)
    try {
      await onSend(content.trim())
      setContent('')
    } catch (err) {
      console.error('Error sending message:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.inputGroup}>
        <input
          type="text"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder={disabled ? "Enter your username first..." : "Type your message..."}
          className={styles.input}
          disabled={disabled || isSubmitting}
          maxLength={1000}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={!content.trim() || disabled || isSubmitting}
        >
          {isSubmitting ? 'Sending...' : 'Send'}
        </button>
      </div>
    </form>
  )
}

